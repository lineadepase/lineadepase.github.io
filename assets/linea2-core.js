(function(root,factory){
  'use strict';
  if(typeof module==='object'&&module.exports)module.exports=factory();
  else root.LDP2=factory();
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  function distribution(n,p){
    if(!Number.isInteger(n)||n<0||n>100||!Number.isFinite(p)||p<0||p>1)throw new RangeError('Disparos o probabilidad fuera de rango');
    let values=[1];
    for(let i=0;i<n;i++){
      const next=new Array(values.length+1).fill(0);
      values.forEach((value,k)=>{next[k]+=value*(1-p);next[k+1]+=value*p;});
      values=next;
    }
    return values;
  }
  function variedDistribution(probabilities){
    if(!Array.isArray(probabilities)||probabilities.length<1||probabilities.length>12||Array.from(probabilities).some(p=>!Number.isFinite(p)||p<0||p>1))throw new RangeError('Define entre uno y doce remates con probabilidades válidas');
    let values=[1];
    for(const p of probabilities){
      const next=new Array(values.length+1).fill(0);
      values.forEach((value,k)=>{next[k]+=value*(1-p);next[k+1]+=value*p;});values=next;
    }
    return values;
  }
  function wilson(goals,shots){
    if(!Number.isInteger(shots)||shots<1||!Number.isInteger(goals)||goals<0||goals>shots)throw new RangeError('La muestra debe contener remates y goles válidos');
    const z=1.959963984540054,p=goals/shots,den=1+z*z/shots;
    const center=(p+z*z/(2*shots))/den;
    const margin=z*Math.sqrt(p*(1-p)/shots+z*z/(4*shots*shots))/den;
    return {rate:p,low:Math.max(0,center-margin),high:Math.min(1,center+margin)};
  }
  function filterMatches(matches,venue='Todas',result='Todos',coverage='Todas'){
    return matches.filter(m=>(venue==='Todas'||m.sede===venue)&&(result==='Todos'||outcome(m)===result)&&(coverage==='Todas'||m.completo===true));
  }
  function outcome(m){return m.goles_favor>m.goles_contra?'Victoria':m.goles_favor===m.goles_contra?'Empate':'Derrota';}
  function summarize(matches){
    const full=matches.filter(m=>m.completo===true);
    const validShots=full.filter(m=>Number.isFinite(m.tiros_zaragoza)&&Number.isFinite(m.tiros_rival));
    const validPossession=full.filter(m=>Number.isFinite(m.posesion_pct));
    const sum=(rows,key)=>rows.reduce((a,m)=>a+m[key],0);
    return {games:matches.length,points:matches.reduce((a,m)=>a+(outcome(m)==='Victoria'?3:outcome(m)==='Empate'?1:0),0),gf:sum(matches,'goles_favor'),gc:sum(matches,'goles_contra'),complete:full.length,shotsCount:validShots.length,shots:validShots.length?sum(validShots,'tiros_zaragoza')/validShots.length:null,against:validShots.length?sum(validShots,'tiros_rival')/validShots.length:null,possessionCount:validPossession.length,possession:validPossession.length?sum(validPossession,'posesion_pct')/validPossession.length:null};
  }
  function csv(matches,cutoff){
    function cell(value){let text=value===null||value===undefined?'':String(value);if(/^[\s]*[=+\-@]/.test(text))text="'"+text;return '"'+text.replace(/"/g,'""')+'"';}
    const header=['Corte','Jornada','Fecha','Rival','Sede','Goles Zaragoza','Goles rival','Ficha completa','Tiros Zaragoza','Tiros rival','Posesión Zaragoza','Fuente por jornada'];
    const rows=matches.map(m=>[cutoff,m.jornada,m.fecha,m.rival,m.sede,m.goles_favor,m.goles_contra,m.completo===true?'Sí':'No',m.completo===true?m.tiros_zaragoza:null,m.completo===true?m.tiros_rival:null,m.completo===true?m.posesion_pct:null,'https://lineadepase.com/proyectos/real-zaragoza/jornada-'+m.jornada+'.html']);
    return '\ufeff'+[header,...rows].map(row=>row.map(cell).join(';')).join('\r\n');
  }
  function passport(value,areas){
    if(!value||value.version!==1||!Array.isArray(value.areas)||typeof value.nota!=='string'||value.nota.length>2000||value.areas.some(x=>typeof x!=='string'||!areas.includes(x)))throw new TypeError('El archivo no tiene el formato de pasaporte esperado');
    return {areas:[...new Set(value.areas)],nota:value.nota};
  }
  function readView(search){
    const params=new URLSearchParams(search),state={};
    const numeric=[['n','shots',1,30],['p','probability',0,100],['mn','sampleShots',1,500],['mk','sampleGoals',0,500]];
    numeric.forEach(([key,name,min,max])=>{const text=params.get(key);if(text!==null&&/^\d+$/.test(text)){const value=Number(text);if(value>=min&&value<=max)state[name]=value;}});
    const choices=[['sede','venue',['Todas','Casa','Fuera']],['resultado','result',['Todos','Victoria','Empate','Derrota']],['cobertura','coverage',['Todas','Solo completas']]];
    choices.forEach(([key,name,allowed])=>{if(allowed.includes(params.get(key)))state[name]=params.get(key);});
    return state;
  }
  function viewUrl(base,state,kind){
    const url=new URL(base);url.search='';
    const fields=kind==='season'?[['sede','venue'],['resultado','result'],['cobertura','coverage']]:[['n','shots'],['p','probability'],['mn','sampleShots'],['mk','sampleGoals']];
    fields.forEach(([key,name])=>{if(state[name]!==undefined)url.searchParams.set(key,String(state[name]));});
    url.hash=kind==='season'?'titulo-explorador':'datalab';
    return url.href;
  }
  function comparisonUrl(base,ids){
    if(!Array.isArray(ids)||ids.length!==2||new Set(ids).size!==2||ids.some(id=>typeof id!=='string'||!/^\d{4}\/\d{2}\|[1-9]\d*$/.test(id)))throw new TypeError('Elige dos jornadas válidas y distintas');
    const url=new URL('../archivo-visual/',base);url.searchParams.set('jornada_a',ids[0]);url.searchParams.set('jornada_b',ids[1]);url.hash='titulo-comparar';return url.href;
  }
  function scenario(shots,probability){
    if(shots<1)throw new RangeError('Debe haber al menos un disparo');
    const values=distribution(shots,probability);
    return {expected:shots*probability,atLeastOne:1-values[0]};
  }
  const researchFields={pregunta:300,hipotesis:500,fuentes:1200,metodo:1200,validacion:1200,limites:1000};
  function researchDraft(value){
    if(!value||value.version!==1)throw new TypeError('Borrador de investigación inválido');
    const result={version:1};
    Object.entries(researchFields).forEach(([key,max])=>{if(typeof value[key]!=='string'||value[key].length>max)throw new TypeError('Campo de investigación inválido');result[key]=value[key];});
    return result;
  }
  function researchText(value){
    const draft=researchDraft(value);
    if(!draft.pregunta.trim())throw new TypeError('Define una pregunta de investigación');
    const labels={pregunta:'Pregunta de investigación',hipotesis:'Hipótesis inicial',fuentes:'Datos y fuentes',metodo:'Método',validacion:'Validación',limites:'Límites del análisis'};
    return 'LÍNEA DE PASE · PRO\nFICHA DE INVESTIGACIÓN · BORRADOR\n\n'+Object.entries(labels).map(([key,label])=>label.toUpperCase()+'\n'+(draft[key].trim()||'Pendiente de definir.')).join('\n\n')+'\n\nFicha de trabajo personal. Su contenido no constituye un resultado validado.\n';
  }
  return {distribution,variedDistribution,wilson,filterMatches,summarize,csv,passport,readView,viewUrl,comparisonUrl,scenario,researchDraft,researchText};
});
