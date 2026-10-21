(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.LPGrupo=api;})(typeof window!=='undefined'?window:globalThis,()=>{
  'use strict';
  const official=row=>{try{const h=new URL(row.fuente_xg).hostname;return h==='sofascore.com'||h.endsWith('.sofascore.com');}catch{return false;}};
  function filter(rows,{sede='',periodo='toda',jornada=8}={}){const first=periodo==='ultimas5'?Math.max(1,jornada-4):1;return rows.filter(r=>r.jornada>=first&&r.jornada<=jornada&&(!sede||r.sede===sede));}
  const definitions={
    puntos:{label:'Puntos',key:'points',direction:'Más puntos',description:'Tres puntos por victoria y uno por empate.'},
    gf:{label:'Goles a favor',key:'goles_favor',direction:'Más goles anotados',description:'Goles marcados en los partidos del filtro.'},
    gc:{label:'Goles en contra',key:'goles_contra',direction:'Menos goles recibidos',description:'Goles encajados; una cifra menor representa menos goles recibidos.'},
    xg:{label:'xG a favor',key:'xg',direction:'Más peligro generado',description:'Probabilidad de gol acumulada de los tiros, según el proveedor elegido.'},
    xgc:{label:'xG en contra',key:'xg_rival',direction:'Menos peligro concedido',description:'Calidad acumulada de los tiros rivales; una cifra menor representa menos peligro concedido.'},
    claras:{label:'Ocasiones claras a favor',key:'ocasiones_claras',direction:'Más ocasiones registradas',description:'Recuento de ocasiones claras del proveedor. No equivale a xG.'},
    clarasContra:{label:'Ocasiones claras en contra',key:'ocasiones_claras_rival',direction:'Menos ocasiones concedidas',description:'Ocasiones claras del rival registradas por el proveedor.'},
    tiros:{label:'Tiros',key:'tiros',direction:'Volumen de remates',description:'Número de tiros. El volumen no mide por sí solo la calidad de las ocasiones.'},
    posesion:{label:'Posesión (%)',key:'posesion_pct',direction:'Estilo de juego',description:'Porcentaje medio de posesión. Más posesión no implica necesariamente mayor rendimiento.'}
  };
  function calc(rows,id,{modo='promedio',fuente='sofascore'}={}){
    if(id==='pj')return {value:rows.length,count:rows.length};
    const metric=definitions[id];if(!metric)return {value:null,count:0};
    const valid=rows.filter(r=>(metric.key==='points'?Number.isFinite(r.goles_favor)&&Number.isFinite(r.goles_contra):Number.isFinite(r[metric.key]))&&(!metric.key.startsWith('xg')||fuente==='todas'||official(r)));
    if(!valid.length)return {value:null,count:0};
    const total=valid.reduce((sum,r)=>sum+(metric.key==='points'?(r.goles_favor>r.goles_contra?3:r.goles_favor===r.goles_contra?1:0):r[metric.key]),0);
    return {value:modo==='totales'&&id!=='posesion'?total:total/valid.length,count:valid.length};
  }
  function reference(rows,id,options={}){
    const teams=[...new Set(rows.map(r=>r.equipo))];
    const values=teams.map(team=>calc(rows.filter(r=>r.equipo===team),id,options).value).filter(Number.isFinite);
    if(!values.length)return {value:null,max:0};
    const value=options.modo==='totales'||id==='pj'?values.reduce((a,b)=>a+b,0)/values.length:calc(rows,id,options).value;
    return {value,max:Math.max(...values),teams:values.length};
  }
  function label(id,mode='promedio'){if(id==='pj')return 'Partidos';return definitions[id].label+(id==='posesion'?'':mode==='totales'?' · total':' por partido');}
  return {official,filter,definitions,calc,reference,label};
});
