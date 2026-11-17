const fs=require('fs'),vm=require('vm');const h=fs.readFileSync(require('path').join(__dirname,'..','..','src','taanit.src.html'),'utf8');
const g=n=>{const i=h.indexOf('const '+n+' = {');const j=h.indexOf('\n};',i);return vm.runInNewContext('('+h.slice(i+n.length+9,j+2)+')');};
const P=g('PUNCT'),W=g('WBW');
const B='בראשית|שמות|ויקרא|במדבר|דברים|יהושע|שופטים|שמואל [אב]|מלכים [אב]|ישעיהו?|ירמיהו?|יחזקאל|הושע|יואל|עמוס|עובדיה|יונה|מיכה|נחום|חבקוק|צפניה|חגי|זכריה|מלאכי|תהלים|משלי|איוב|שיר השירים|רות|איכה|קהלת|אסתר|דניאל|עזרא|נחמיה|דברי הימים [אב]';
const re=new RegExp('\\((?:[^()]*?, )?('+B+') ([א-ת״"׳\']{1,4})(?:, ?([א-ת״"׳\'\\-–]{1,7}))?','g');
const norm=b=>b.replace(/ישעיהו/,'ישעיה').replace(/ירמיהו/,'ירמיה');
const out={},ch=new Set();
for(const [k,v] of [...Object.entries(P),...Object.entries(W)]){let m;re.lastIndex=0;while((m=re.exec(v))){const id=norm(m[1])+' '+m[2]+(m[3]?', '+m[3]:'');(out[k]=out[k]||new Set()).add(id);ch.add(norm(m[1])+' '+m[2]);}}
const o={};for(const [k,s] of Object.entries(out))o[k]=[...s];
fs.writeFileSync(require('path').join(__dirname,'refmap.json'),JSON.stringify(o));
console.log(Object.keys(o).length,'beats', ch.size,'chapters');console.log([...ch].sort().join(' | '));
