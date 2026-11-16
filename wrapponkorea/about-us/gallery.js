(() => {
  const gallery = document.querySelector('.company-gallery');
  if (!gallery) return;
  const slides = [...gallery.querySelectorAll(':scope > img')];
  const status = gallery.querySelector('[aria-live]');
  let index = 0;
  gallery.querySelectorAll('[data-step]').forEach(button => {
    button.addEventListener('click', () => {
      slides[index].hidden = true;
      index = (index + Number(button.dataset.step) + slides.length) % slides.length;
      slides[index].hidden = false;
      status.textContent = `${index + 1} / ${slides.length}`;
    });
  });
})();
