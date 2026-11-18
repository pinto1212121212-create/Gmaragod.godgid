// השוואת מילה־במילה: ED_LINES מול PUNCT, לכל שלב
const fs=require('fs'),vm=require('vm');
const src=fs.readFileSync('.claude/src/taanit.src.html','utf8');
const m=src.match(/const ED_LINES = \{[\s\S]*?\n\};/); const ctx={}; vm.createContext(ctx); vm.runInContext(m[0].replace('const ED_LINES','ED_LINES'),ctx);
const EL=ctx.ED_LINES;
const AB={'אר':'אמר רבי','אל':'אמר ליה','מט':'מאי טעמא','שנא':'שנאמר','תח':'תלמיד חכם','רבשע':'רבונו של עולם','הקבה':'הקדוש ברוך הוא','ר':'רבי','אפי':'אפילו','אפה':'אפילו הכי','בב':'בן בתירה','רע':'רבי עקיבא','רמ':'רבי מאיר','מש':'מאי שנא','אכ':'אם כן','יוט':'יום טוב','רל':'ריש לקיש','קאל':'קאמר ליה','ואר':'ואמר רבי','ואל':'ואמר ליה','מד':'מאי דכתיב','שמ':'שמע מינה','וסל':'וסבר לה','דמתני':'דמתניתין','מתני':'מתניתין','תר':'תנו רבנן','תל':'תלמוד לומר','אא':'אי אפשר','ריבל':'רבי יהושע בן לוי','עז':'עבודה זרה','כש':'כל שכן','אעפ':'אף על פי','ואחכ':'ואחר כך','ירמ':'יהי רצון מלפניך','עאכו':'על אחת כמה וכמה','אעפכ':'אף על פי כן','מרה':'מראש השנה','יוהכ':'יום הכפורים','אכ':'אלא אם כן','קאר':'קאמר רבי','למהד':'למה הדבר דומה','גמ':'גמרא','הכי':'הכי'};
const BOOK=/^\((בראשית|שמות|ויקרא|במדבר|דברים|יהושע|שופטים|שמואל|מלכים|ישעי|ירמי|יחזקאל|הושע|יואל|עמוס|מיכה|זכריה|מלאכי|תהלים|תהילים|משלי|איוב|שיר|קהלת|דניאל|עזרא|נחמיה|דברי|ממשיך|ההמשך|רות|איכה|אסתר|חבקוק|צפניה|חגי|נחום|יונה|עובדיה|שלמודו|עשר|וכו)/;
const norm=t=>t.replace(/<[^>]+>/g,' ').replace(/\([^()]*\)/g,x=>BOOK.test(x)?' ':x).replace(/[֑-ׇ]/g,'').replace(/[^א-ת\s״׳"']/g,' ').split(/\s+/).filter(Boolean);
for (const ref of Object.keys(EL).sort()) {
  const c2={PAGE_IN:(r,d)=>c2.P=d}; vm.createContext(c2); vm.runInContext(fs.readFileSync('data/taanit/'+ref+'.js','utf8'),c2);
  const pu=c2.P.punct; const keys=Object.keys(pu).sort((a,b)=>{const x=a.split(':').map(Number),y=b.split(':').map(Number);return x[1]-y[1]||x[2]-y[2]});
  const L=EL[ref]; const all=[L.open||'',...L.narrow,...L.wide,...(L.full||[])].join(' ');
  const segs=all.split('‖');
  const out=[];
  keys.forEach((k,j)=>{ const a=norm(pu[k]).filter(w=>!/^(\.\.\.|כו)$/.test(w)), b=norm(segs[j]||'');
    const cl=w=>w.replace(/[״׳"']/g,''); const sa=new Set(a.map(cl)), sb=new Set(); b.forEach(w=>{const c=cl(w); sb.add(c); const e=AB[c]||AB[c.replace(/^[ודכלשה]/,'')]; if(e) (c[0]!==(AB[c]?'':c[0]) ? (c[0]+e) : e).split(' ').concat(e.split(' ')).forEach(x=>sb.add(x)); if(/^[ודכלשה]/.test(c)&&AB[c.slice(1)]) { const e2=AB[c.slice(1)].split(' '); sb.add(c[0]+e2[0]); e2.forEach(x=>sb.add(x)); } });
    const miss=a.filter(w=>!sb.has(w.replace(/[״׳"']/g,''))&&!/[״׳"']/.test(w)), extra=b.filter(w=>!sa.has(w.replace(/[״׳"']/g,''))&&!/[״׳"']/.test(w));
    if (miss.length>0||extra.length>0) out.push(`  ${k}\n    בטקסט ולא בשורות: ${miss.join(' ')}\n    בשורות ולא בטקסט: ${extra.join(' ')}`); });
  console.log(ref, `שלבים ${keys.length}, קטעים ${segs.length}`); if(out.length) console.log(out.join('\n'));
}
