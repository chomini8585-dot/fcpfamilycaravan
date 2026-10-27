"""중고차 사진 자동 정리 — GitHub Actions에서 실행됩니다 (.github/workflows/used-car-photos.yml).

used-cars/cars/<번호>/ 폴더마다:
  1. 사진(jpg/jpeg/png/webp/heic, 대소문자 무관, 이름 무관)을 1600px 이하 JPEG로 압축하고
     위치정보(EXIF)를 지웁니다. 이미 정리한 사진은 다시 압축하지 않습니다(화질 보존).
  2. 사진 이름을 1.jpg, 2.jpg, … 로 빈 번호 없이 맞춥니다.
     순서: '대표'로 시작하는 사진 → 기존 번호 사진(번호순) → 새 사진(파일 이름순).
  3. info.txt의 '대표사진: N' 줄을 바뀐 번호에 맞춰 고칩니다.
     ('대표…' 사진을 올렸다면 그 사진이 1번이 되고 대표사진도 1이 됩니다.)
  4. used-cars/cars/index.json 에 차량 폴더와 사진 목록을 적습니다(홈페이지가 이 목록을 읽음).

사용: python optimize_used_cars.py used-cars/cars
"""
import io
import json
import os
import re
import sys

from PIL import Image, ImageOps

try:  # 아이폰 HEIC 지원 (없어도 나머지는 동작)
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:  # pragma: no cover
    pass

MAX_SIDE = 1600
QUALITY = 82
MARK = b"fcp-optimized"          # 정리한 사진에 남기는 표시 → 다음 실행 때 건너뜀
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
CAR_DIR = re.compile(r"^\d{2,}$")
COVER_LINE = re.compile(r"^(\s*대표\s*사진\s*[:：]\s*)(\d+)(.*)$", re.M)


def natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def is_optimized(path):
    try:
        with Image.open(path) as im:
            return im.format == "JPEG" and im.info.get("comment") == MARK and max(im.size) <= MAX_SIDE
    except Exception:
        return False


def optimize(src, dst):
    """src 이미지를 dst(JPEG)로 저장. src와 dst가 같아도 됨."""
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            rgba = im.convert("RGBA")
            bg.paste(rgba, mask=rgba.split()[-1])
            im = bg
        elif im.mode == "L":
            im = im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True, comment=MARK)
    with open(dst, "wb") as f:
        f.write(buf.getvalue())


def read_text(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8", "cp949"):       # utf-8은 BOM도 그대로 보존
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8"


def process_car(car_dir):
    names = [n for n in os.listdir(car_dir)
             if os.path.isfile(os.path.join(car_dir, n)) and os.path.splitext(n)[1].lower() in EXTS]
    cover_files, numbered, fresh = [], [], []
    for n in names:
        stem = os.path.splitext(n)[0]
        if stem.startswith("대표"):
            cover_files.append(n)
        elif stem.isdigit():
            numbered.append(n)
        else:
            fresh.append(n)
    numbered.sort(key=lambda n: (int(os.path.splitext(n)[0]), n))
    fresh.sort(key=natural_key)
    cover_files.sort(key=natural_key)
    order = cover_files + numbered + fresh

    old_num_to_new = {}
    plan = []                                         # (원본 이름, 새 번호)
    for i, n in enumerate(order, start=1):
        stem = os.path.splitext(n)[0]
        if stem.isdigit() and int(stem) not in old_num_to_new:
            old_num_to_new[int(stem)] = i
        plan.append((n, i))

    # 1) 압축/변환 → 임시 이름 (이름 충돌 방지)
    temps = []
    for n, i in plan:
        src = os.path.join(car_dir, n)
        tmp = os.path.join(car_dir, f".tmp-{i}.jpg")
        if os.path.splitext(n)[1] == ".jpg" and is_optimized(src):
            os.replace(src, tmp)
        else:
            optimize(src, tmp)
            if os.path.abspath(src) != os.path.abspath(tmp) and os.path.exists(src):
                os.remove(src)
        temps.append((tmp, i))
    # 2) 임시 이름 → 1.jpg, 2.jpg, …
    for tmp, i in temps:
        os.replace(tmp, os.path.join(car_dir, f"{i}.jpg"))

    # 3) info.txt 대표사진 번호 맞추기
    info = os.path.join(car_dir, "info.txt")
    if os.path.exists(info):
        text, enc = read_text(info)
        new_text = text
        if cover_files:
            new_text = COVER_LINE.sub(lambda m: m.group(1) + "1" + m.group(3), text)
        else:
            def remap(m):
                old = int(m.group(2))
                return m.group(1) + str(old_num_to_new.get(old, old)) + m.group(3)
            new_text = COVER_LINE.sub(remap, text)
        if new_text != text:
            with open(info, "wb") as f:
                f.write(new_text.encode(enc))

    return [f"{i}.jpg" for _, i in plan]


def main(root):
    cars = []
    for d in sorted(os.listdir(root), key=natural_key):
        path = os.path.join(root, d)
        if not (os.path.isdir(path) and CAR_DIR.match(d)):
            continue
        if not os.path.exists(os.path.join(path, "info.txt")):
            print(f"[건너뜀] {d}: info.txt 없음")
            continue
        photos = process_car(path)
        cars.append({"dir": d, "photos": photos})
        print(f"[정리] {d}: 사진 {len(photos)}장")
    manifest = json.dumps({"cars": cars}, ensure_ascii=False, indent=1) + "\n"
    out = os.path.join(root, "index.json")
    old = open(out, encoding="utf-8").read() if os.path.exists(out) else None
    if old != manifest:
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)
    print(f"차량 {len(cars)}대 → index.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "used-cars/cars")
