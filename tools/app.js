(function(){
var tl=document.getElementById('tl');if(!tl)return;
var today=new Date();today.setHours(0,0,0,0);
var items=[].slice.call(tl.querySelectorAll('li.ev')),nextLi=null;
items.forEach(function(li){var d=new Date(li.dataset.date+'T00:00:00');
 if(d<today)li.classList.add('past');else if(!nextLi)nextLi=li;});
var nb=document.getElementById('next');
if(nextLi&&nb){var d=new Date(nextLi.dataset.date+'T00:00:00'),n=Math.round((d-today)/864e5);
 nb.querySelector('.s4').textContent='('+(n===0?nb.dataset.today:n===1?nb.dataset.tom:nb.dataset.in.replace('{n}',n))+')';
 nb.querySelector('.s3').textContent=nextLi.querySelector('h4').textContent;
 nb.querySelector('.s2').textContent=nextLi.dataset.dl;nextLi.classList.add('soon');}
var tools=document.getElementById('tools'),f='all',hidePast=true;
function refresh(){
 items.forEach(function(li){var v=!(hidePast&&li.classList.contains('past'))&&(f==='all'||li.classList.contains(f));li.hidden=!v;});
 [].forEach.call(tl.querySelectorAll('.month'),function(m){m.hidden=!m.querySelector('li.ev:not([hidden])');});}
if(tools){tools.hidden=false;
 [].forEach.call(tools.querySelectorAll('[data-f]'),function(b){b.addEventListener('click',function(){
  f=b.dataset.f;[].forEach.call(tools.querySelectorAll('[data-f]'),function(x){x.setAttribute('aria-pressed',x===b)});refresh();});});
 var pb=document.getElementById('pastbtn');
 if(pb){if(!tl.querySelector('li.past'))pb.hidden=true;
  pb.addEventListener('click',function(){hidePast=!hidePast;pb.textContent=hidePast?pb.dataset.show:pb.dataset.hide;refresh();});}
 refresh();}
[].forEach.call(document.querySelectorAll('.copy'),function(b){b.addEventListener('click',function(){
 var t=b.dataset.url;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).catch(function(){
  var r=document.createRange();r.selectNode(b.previousElementSibling);getSelection().removeAllRanges();getSelection().addRange(r);document.execCommand('copy');});
 var o=b.textContent;b.textContent=b.dataset.ok;setTimeout(function(){b.textContent=o},1600);});});
})();

(function(){var now=new Date(),k=now.getFullYear()+'-'+('0'+(now.getMonth()+1)).slice(-2);
[].forEach.call(document.querySelectorAll('.mc'),function(m){if(m.dataset.ym<k)m.classList.add('old');else if(m.dataset.ym===k)m.classList.add('now');});})();
