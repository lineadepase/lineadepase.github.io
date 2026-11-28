(function(){
'use strict';
let restore=null;
window.addEventListener('beforeprint',()=>{if(restore!==null)return;restore=[...document.querySelectorAll('main details:not([open])')];restore.forEach(item=>item.open=true);});
window.addEventListener('afterprint',()=>{if(restore===null)return;restore.forEach(item=>item.open=false);restore=null;});
})();
