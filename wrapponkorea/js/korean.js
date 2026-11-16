/* Limit the original one-page navigation to on-page anchors. */
document.addEventListener('DOMContentLoaded', function () {
  var menuButton = document.querySelector('.navbar-toggle');
  var menu = document.querySelector('#main-menu .navbar-collapse');
  if (menuButton && menu) {
    menuButton.removeAttribute('data-toggle');
    menuButton.removeAttribute('data-target');
    menuButton.setAttribute('aria-expanded', 'false');
    function setMenu(open) {
      menu.classList.remove('collapsing');
      menu.classList.add('collapse');
      menu.classList.toggle('in', open);
      menuButton.classList.toggle('collapsed', !open);
      menuButton.setAttribute('aria-expanded', String(open));
    }
    menuButton.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      setMenu(!menu.classList.contains('in'));
    }, true);
    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function (event) {
        if (menu.classList.contains('in')) {
          setMenu(false);
          var href = link.getAttribute('href');
          if (href && href.startsWith('#') && href.length > 1) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var section = document.querySelector(href);
            if (section) section.scrollIntoView({behavior: 'auto', block: 'start'});
          }
        }
      }, true);
    });
  }
});
