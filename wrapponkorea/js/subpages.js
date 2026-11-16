document.addEventListener('DOMContentLoaded',function(){
  var toggle=document.querySelector('.ko-nav-toggle');
  var nav=document.querySelector('.ko-site-nav');
  if(toggle&&nav){toggle.addEventListener('click',function(){var open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'메뉴 닫기':'메뉴 열기';});}
  var button=document.querySelector('.navbar-toggle');
  var menu=document.querySelector('#main-menu .navbar-collapse')||document.querySelector('.navbar-collapse');
  if(button&&menu){
    button.removeAttribute('data-toggle');button.removeAttribute('data-target');button.setAttribute('aria-label','메뉴 열기 또는 닫기');button.setAttribute('aria-expanded','false');
    function closeMenu(){menu.classList.remove('in','collapsing');menu.classList.add('collapse');button.classList.add('collapsed');button.setAttribute('aria-expanded','false');}
    closeMenu();
    button.addEventListener('click',function(e){e.preventDefault();e.stopImmediatePropagation();var open=!menu.classList.contains('in');menu.classList.toggle('in',open);button.classList.toggle('collapsed',!open);button.setAttribute('aria-expanded',String(open));},true);
    menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){closeMenu();});});
  }
  document.querySelectorAll('[data-toggle="modal"]').forEach(function(a){a.addEventListener('click',function(e){var id=a.getAttribute('data-target')||a.getAttribute('href');if(!id||id[0]!=='#')return;var modal=document.getElementById(id.slice(1));if(!modal)return;e.preventDefault();modal.style.display='block';modal.classList.add('in');modal.setAttribute('role','dialog');modal.setAttribute('aria-modal','true');modal.setAttribute('tabindex','-1');modal.focus();function close(){modal.style.display='none';modal.classList.remove('in');modal.removeAttribute('aria-modal');a.focus();document.removeEventListener('keydown',escape);}function escape(ev){if(ev.key==='Escape')close();}modal.querySelectorAll('[data-dismiss="modal"]').forEach(function(b){b.onclick=close;});modal.onclick=function(ev){if(ev.target===modal)close();};document.addEventListener('keydown',escape);});});
});
