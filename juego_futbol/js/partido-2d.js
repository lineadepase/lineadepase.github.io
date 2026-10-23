/* Ocasiones arcade con balón independiente. La física también se prueba sin DOM. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.Partido2D=api;})(typeof globalThis!=='undefined'?globalThis:this,()=>{
 'use strict';
 const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
 class Ocasion{
  constructor(media=70){this.media=clamp(media,1,100);this.players=[{x:180,y:165},{x:330,y:85}];this.defenders=[{x:370,y:190},{x:440,y:100}];this.selected=0;this.ball={x:194,y:165,vx:0,vy:0,owner:0};this.keeper={x:575,y:165};this.time=0;this.done=false;this.goal=false;this.message='Acércate, pasa y busca un hueco.';this.aimY=0;this.shots=0;this.passes=0;}
  shoot(){if(this.done||this.ball.owner<0)return;const p=this.players[this.selected],angle=Math.atan2(165-p.y+(this.aimY*40),630-p.x),power=320+this.media*2.2;this.ball.x=p.x+14;this.ball.y=p.y;this.ball.vx=Math.cos(angle)*power;this.ball.vy=Math.sin(angle)*power;this.ball.owner=-1;this.shots++;this.message='¡Disparo!';}
  pass(){if(this.done||this.ball.owner<0)return;const next=1-this.selected,p=this.players[next],dx=p.x-this.ball.x,dy=p.y-this.ball.y,len=Math.max(1,Math.hypot(dx,dy));this.ball.vx=dx/len*310;this.ball.vy=dy/len*310;this.ball.owner=-1;this.selected=next;this.passes++;this.message='Pase al compañero. Acércate al balón para recibir.';}
  step(dt,input={}){
   if(this.done)return;dt=clamp(dt,0,.04);this.time+=dt;
   const p=this.players[this.selected],dx=(input.right?1:0)-(input.left?1:0),dy=(input.down?1:0)-(input.up?1:0),len=Math.max(1,Math.hypot(dx,dy)),speed=100+this.media*.7;
   p.x=clamp(p.x+dx/len*speed*dt,25,550);p.y=clamp(p.y+dy/len*speed*dt,25,305);if(dy)this.aimY=dy;
   if(input.shoot)this.shoot();if(input.pass)this.pass();
   const b=this.ball;
   if(b.owner>=0){b.owner=this.selected;b.x=p.x+14;b.y=p.y;}else{
    b.x+=b.vx*dt;b.y+=b.vy*dt;b.vx*=Math.pow(.986,dt*60);b.vy*=Math.pow(.986,dt*60);
    if(b.x>=615){this.done=true;this.goal=b.y>110&&b.y<220;this.message=this.goal?'¡GOL! Tu disparo entra en la portería.':'El balón sale fuera.';return;}
    if(b.x<15||b.y<15||b.y>315){this.done=true;this.message='El balón sale fuera.';return;}
    if(Math.hypot(b.x-p.x,b.y-p.y)<18&&Math.hypot(b.vx,b.vy)<340){b.owner=this.selected;b.vx=0;b.vy=0;}
   }
   const keeperTarget=b.x>480?b.y:165+Math.sin(this.time)*28;
   this.keeper.y=clamp(this.keeper.y+clamp(keeperTarget-this.keeper.y,-1,1)*70*dt,115,215);
   if(b.owner<0&&Math.hypot(b.x-this.keeper.x,b.y-this.keeper.y)<17){b.vx=-Math.abs(b.vx)*.45;b.vy=(b.y-this.keeper.y)*8;this.message='¡Rechaza el portero!';}
   this.defenders.forEach((d,i)=>{
    const tx=b.owner<0?b.x:p.x,ty=b.owner<0?b.y:p.y,dist=Math.max(1,Math.hypot(tx-d.x,ty-d.y));
    d.x=clamp(d.x+(tx-d.x)/dist*(58+i*5)*dt,260,535);d.y=clamp(d.y+(ty-d.y)/dist*(58+i*5)*dt,25,305);
    if(Math.hypot(d.x-b.x,d.y-b.y)<13){if(b.owner>=0){this.done=true;this.message='El defensa recupera el balón.';}else{b.vx=-Math.abs(b.vx)*.35;b.vy+=(i?1:-1)*90;this.message='¡Rebote en el defensa!';}}
   });
   if(this.time>=18){this.done=true;this.message='Se acaba la ocasión.';}
  }
 }
 return {Ocasion};
});

if(typeof document!=='undefined')(()=>{
 const modal=document.createElement('div');modal.id='arcade-modal';modal.className='arcade-backdrop';modal.setAttribute('role','dialog');modal.setAttribute('aria-modal','true');modal.setAttribute('aria-labelledby','arcade-title');modal.setAttribute('aria-hidden','true');
 modal.innerHTML='<div class="arcade-dialog"><h2 id="arcade-title">Tú juegas esta ocasión</h2><p id="arcade-help">Flechas o WASD: mover · Espacio: disparar · X: pasar · Esc: salir</p><canvas id="arcade-pitch" width="640" height="330" tabindex="0" aria-label="Ocasión 2D. Mueve al jugador con las flechas, dispara con Espacio y pasa con X."></canvas><div class="arcade-status"><strong id="arcade-clock">18 s</strong><span id="arcade-message" role="status"></span></div><div class="arcade-controls"><div class="arcade-pad"><button type="button" data-arcade="up" aria-label="Mover arriba">↑</button><button type="button" data-arcade="left" aria-label="Mover izquierda">←</button><button type="button" data-arcade="down" aria-label="Mover abajo">↓</button><button type="button" data-arcade="right" aria-label="Mover derecha">→</button></div><button type="button" id="arcade-pass">Pasar · X</button><button type="button" id="arcade-shoot">Disparar · Espacio</button><button type="button" id="arcade-exit">Terminar ocasión</button></div></div>';
 document.body.append(modal);const $=id=>document.getElementById(id),canvas=$('arcade-pitch'),ctx=canvas.getContext('2d');let active=null,resolveGame=null,frame=0,previous=0,practice=false,focusBefore=null;const keys={};
 function finish(){if(!active||!resolveGame)return;cancelAnimationFrame(frame);const result={success:active.goal,controlledGoal:active.goal,player:active.player,choice:'arcade',shots:active.shots,passes:active.passes};const fn=resolveGame;resolveGame=null;active=null;Object.keys(keys).forEach(k=>delete keys[k]);modal.classList.remove('open');modal.setAttribute('aria-hidden','true');focusBefore?.focus({preventScroll:true});fn(result);}
 function draw(game){
  ctx.fillStyle='#146b37';ctx.fillRect(0,0,640,330);for(let x=20;x<620;x+=80){ctx.fillStyle='#ffffff08';ctx.fillRect(x,15,40,300);}ctx.strokeStyle='#e2e8f0';ctx.lineWidth=2;ctx.strokeRect(15,15,600,300);ctx.strokeRect(515,75,100,180);ctx.strokeRect(615,110,20,110);ctx.beginPath();ctx.arc(320,165,42,0,Math.PI*2);ctx.stroke();
  [...game.players.map((p,i)=>({...p,color:'#38bdf8',n:i+9,selected:i===game.selected})),...game.defenders.map((p,i)=>({...p,color:'#fb7185',n:i+4})),{...game.keeper,color:'#facc15',n:1}].forEach(p=>{ctx.beginPath();ctx.arc(p.x,p.y,p.selected?15:12,0,Math.PI*2);ctx.fillStyle=p.color;ctx.fill();ctx.strokeStyle=p.selected?'#fff':'#0f172a';ctx.lineWidth=p.selected?4:2;ctx.stroke();ctx.fillStyle='#0f172a';ctx.font='bold 12px system-ui';ctx.textAlign='center';ctx.fillText(p.n,p.x,p.y+4);});
  ctx.beginPath();ctx.arc(game.ball.x,game.ball.y,5,0,Math.PI*2);ctx.fillStyle='white';ctx.fill();ctx.strokeStyle='#0f172a';ctx.stroke();
 }
 function tick(now){if(!active)return;const dt=previous?Math.min(.04,(now-previous)/1000):.016;previous=now;active.step(dt,keys);draw(active);$('arcade-clock').textContent=Math.max(0,Math.ceil(18-active.time))+' s';$('arcade-message').textContent=active.message;
  if(active.done){$('arcade-exit').textContent=practice?'Volver al club':'Continuar partido';if(!practice)setTimeout(finish,900);return;}frame=requestAnimationFrame(tick);
 }
 window.jugarOcasion2D=function(entrenamiento=false){if(active)return Promise.resolve({success:false,controlledGoal:false});practice=entrenamiento;focusBefore=document.activeElement;const player=obtenerMiEquipo().plantilla.filter(j=>j.titular&&!j.lesionado).sort((a,b)=>b.atributos.CHI-a.atributos.CHI)[0];active=new Partido2D.Ocasion(player?.media||65);active.player=player;previous=0;$('arcade-title').textContent=practice?'Práctica 2D · sin efecto en la liga':'Ocasión oficial · tus goles cuentan';$('arcade-exit').textContent='Terminar ocasión';modal.classList.add('open');modal.setAttribute('aria-hidden','false');canvas.focus({preventScroll:true});frame=requestAnimationFrame(tick);return new Promise(resolve=>{resolveGame=resolve;});};
 const map={ArrowUp:'up',w:'up',ArrowDown:'down',s:'down',ArrowLeft:'left',a:'left',ArrowRight:'right',d:'right'};
 document.addEventListener('keydown',e=>{if(!active)return;const key=map[e.key]||map[e.key.toLowerCase()];if(key){e.preventDefault();keys[key]=true;}if(e.code==='Space'){e.preventDefault();if(!e.repeat)active.shoot();}if(e.key.toLowerCase()==='x'){e.preventDefault();if(!e.repeat)active.pass();}if(e.key==='Escape'){e.preventDefault();finish();}if(e.key==='Tab'){const controls=[...modal.querySelectorAll('button,canvas')],i=controls.indexOf(document.activeElement);e.preventDefault();controls[(i+(e.shiftKey?-1:1)+controls.length)%controls.length].focus();}});
 document.addEventListener('keyup',e=>{const key=map[e.key]||map[e.key.toLowerCase()];if(key)keys[key]=false;});
 window.addEventListener('blur',()=>Object.keys(keys).forEach(k=>delete keys[k]));
 modal.querySelectorAll('[data-arcade]').forEach(b=>{b.onpointerdown=e=>{e.preventDefault();b.setPointerCapture(e.pointerId);keys[b.dataset.arcade]=true;};b.onpointerup=b.onpointercancel=()=>{keys[b.dataset.arcade]=false;};});
 $('arcade-shoot').onclick=()=>active?.shoot();$('arcade-pass').onclick=()=>active?.pass();$('arcade-exit').onclick=finish;
})();
