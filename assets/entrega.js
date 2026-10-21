(() => {
  'use strict';
  const text=document.getElementById('texto-entrega'),channel=document.getElementById('canal-entrega');
  if(!text||!channel)return;
  const original=text.value,lastBreak=original.lastIndexOf('\n'),prefix=original.slice(0,lastBreak),initial=new URL(original.slice(lastBreak+1));
  channel.addEventListener('change',()=>{
    initial.searchParams.set('utm_source',channel.value);
    text.value=prefix+'\n'+initial.href;
    document.getElementById('estado-entrega').textContent='';
  });
  document.getElementById('copiar-entrega').addEventListener('click',async()=>{
    try{await navigator.clipboard.writeText(text.value);document.getElementById('estado-entrega').textContent='Texto y enlace copiados.';}
    catch{text.focus();text.select();document.getElementById('estado-entrega').textContent='El texto está seleccionado y se puede copiar.';}
  });
})();
