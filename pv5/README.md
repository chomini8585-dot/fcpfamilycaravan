# FCP 패밀리카라반 — PV5 리무진 랜딩페이지

기아 PV5 패신저 / 카고 리무진 특장 마케팅 사이트.
FCP 패밀리카라반 (용인직영점) — https://familycaravankorea-tech.github.io/familycaravan/

## 배포 방법

### GitHub Pages (chomini8585-dot/fcpfamilycaravan)

```bash
# 1. 레포 디렉토리로 이동
cd path/to/fcpfamilycaravan

# 2. 이 패키지의 모든 파일을 레포 루트에 복사
#    (index.html / favicon.* / images/ / robots.txt / sitemap.xml)

# 3. 커밋 + 푸시
git add .
git commit -m "PV5 PBV 랜딩페이지 전면 개편"
git push origin main

# 4. GitHub → Settings → Pages → "Deploy from branch" / main / root
# 5. 1~2분 후 https://familycaravankorea-tech.github.io/familycaravan/ 접속
```

## 파일 구조

```
fcpfamilycaravan/
├── index.html              # 메인 페이지 (127KB, 외부 이미지 참조)
├── favicon.svg             # SVG 파비콘 (모던 브라우저)
├── favicon-32.png          # 32x32 PNG (구형 브라우저 폴백)
├── favicon-180.png         # 180x180 (iOS 홈 화면 아이콘)
├── robots.txt              # 검색엔진 크롤러용
├── sitemap.xml             # 사이트맵
├── README.md               # 이 파일
└── images/                 # 28장 이미지 (JPEG, lazy load)
    ├── 2열-2인-전동-시트.jpeg
    ├── 대리석-플로어-무드-조명.jpeg
    └── ... (총 28개)
```

## 주요 기능

- **반응형**: 모바일 / 태블릿 / 데스크톱 모두 대응
- **변형 탭**: 패신저 / 카고 토글 (각 트림별 고유 콘텐츠)
- **Lazy loading**: 이미지가 화면에 들어올 때만 로드 (`loading="lazy"`)
- **Open Graph**: 카카오톡 / 페이스북 / 트위터 공유 시 미리보기 지원
- **SEO**: 메타 태그, sitemap, robots.txt 완비

## 디자인 시스템

- **포레스트 그린** `#1f4d3a` 메인 컬러 + 화이트 베이스
- **타이포그래피**: Fraunces (디스플레이) + Pretendard (한글 본문)
- **외부 폰트 CDN**: Google Fonts + jsDelivr (Pretendard)

## 콘텐츠 구성

### 패신저 트림
- 시그니처 피처 5개: 전동 시트 → 대리석 플로어 → 센터콘솔 → 조명 패키지 → PV5 팝업루프
- 시트 컬러 3종 (올 브라운 / 베이지+네이비 / 올 네이비)
- 사진 쇼케이스 8장
- 특장 옵션 14개

### 카고 트림
- 시그니처 피처 7개: 전동 시트 → 기본 격벽 제거 → 탁자/의자 → 대리석+스커프 → 트리밍/조명 → 창문 시공 → 팝업루프
- 시트 컬러 3종 (패신저 공통)
- 특장 옵션 17개

### 공통
- YouTube 영상 (휘투어스 리뷰) + 5개 챕터 타임라인
- 가격 밴드 (패신저 380만원~ / 카고 400만원~)
- 매장 위치 / 연락처 / 카카오 · 네이버 · 구글 지도 링크

## 캐시 무효화

배포 후 변경사항이 반영되지 않으면 브라우저 강제 새로고침:
- Windows / Linux: `Ctrl + Shift + R`
- macOS: `Cmd + Shift + R`

## 문의

FCP 패밀리카라반 용인직영점  
경기도 용인시 기흥구 구성로 330  
1877-8262

생성일: 2026-04-28
