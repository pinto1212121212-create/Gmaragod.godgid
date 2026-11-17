// 📦 חלק מ־build.py: מייצר את הנתונים לפי דף, כדי שהאתר יחזיק את כל הש״ס.
// קורא את המקורות (.claude/src/*) ומריץ אותם ב־node, ואז כותב:
//   data/<מסכת>/<ref>.js   — כל מה שהעץ ודף הלימוד צריכים לדף אחד (עץ, אנשים, הקשר, מילה במילה, סימונים...)
//   data/<מסכת>/index.js   — ״מפה״ קטנה של המסכת: אילו דפים בנויים, שמות, כמה קטעים, איפה יש סימונים, גרסאות
//   data/common.js          — מילון (WDICT) ומונחים (KEY_TERMS), משותף לכל הש״ס (גדל לאט: אוצר מילים)
//   data/<מסכת>/words.js    — המאגר של לימוד המילים, מחושב מראש (words.html לא צריך לטעון את כל הדפים)
//   .claude/out/pairs.json  — MISHNA/PAIRS (build.py מחלק אותם לפי דף)
const fs = require('fs'), path = require('path'), vm = require('vm'), crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..'), SRC = path.join(ROOT, '.claude', 'src');
const MAS = 'taanit', MAS_NAME = 'תענית';
const html = fs.readFileSync(path.join(SRC, 'taanit.src.html'), 'utf8');

// מוציא את הביטוי של const NAME = ...; מתוך המקור ומריץ אותו
function constOf(name, src = html) {
  const a = `const ${name} = `, i = src.indexOf(a); if (i < 0) throw new Error('חסר ' + name);
  const j = endOfExpr(src, i + a.length);
  return vm.runInNewContext('(' + src.slice(i + a.length, j - 1) + ')');
}
function blockOf(start, src = html) {   // Object.assign(X, {...});
  const i = src.indexOf(start); if (i < 0) return {};
  const j = endOfExpr(src, i + src.slice(i).indexOf('('));   // מ־( עד ;
  const body = src.slice(i + start.length - 1, j).replace(/\)\s*;\s*$/, '');   // {...}
  return vm.runInNewContext('(' + body + ')');
}
function endOfExpr(s, i) {   // סוף ביטוי JS עד ; בעומק 0 (מחרוזות, תבניות, הערות)
  let d = 0;
  const str = k => { const q = s[k]; k++;
    if (q !== '`') { while (s[k] !== q) k += s[k] === '\\' ? 2 : 1; return k + 1; }
    while (true) { if (s[k] === '\\') { k += 2; continue; } if (s[k] === '`') return k + 1;
      if (s.startsWith('${', k)) { let dd = 1; k += 2; while (dd) { if ('\'"`'.includes(s[k])) { k = str(k); continue; } if ('([{'.includes(s[k])) dd++; else if (')]}'.includes(s[k])) dd--; k++; } continue; }
      k++; } };
  while (i < s.length) {
    const c = s[i];
    if ('\'"`'.includes(c)) { i = str(i); continue; }
    if (s.startsWith('//', i)) { i = s.indexOf('\n', i); continue; }
    if (s.startsWith('/*', i)) { i = s.indexOf('*/', i) + 2; continue; }
    if ('([{'.includes(c)) d++; else if (')]}'.includes(c)) d--; else if (c === ';' && d === 0) return i + 1;
    i++;
  }
  throw new Error('סוף ביטוי לא נמצא');
}
// שורות 'ref:s:b': '...' בתוך const NAME = {...} — נשמרות כמו שהן (המחרוזת כבר ב־JS)
function linesOf(name) {
  const i = html.indexOf(`const ${name} = {`), j = endOfExpr(html, i + `const ${name} = `.length);
  return vm.runInNewContext('(' + html.slice(i + `const ${name} = `.length, j - 1) + ')');
}
function runFile(f, names) {   // מריץ קובץ src ומחזיר את הקבועים שלו
  const code = fs.readFileSync(path.join(SRC, f), 'utf8') + `\n;({${names.join(',')}})`;
  return vm.runInNewContext(code, { window: {} });
}

const T = runFile('tree-data.js', ['TREE', 'SECTION_NAMES', 'SUGYA_TOPIC', 'TREE_CX']);
const { PEOPLE } = runFile('people-data.js', ['PEOPLE']);
const { CONTEXT } = runFile('context-data.js', ['CONTEXT']);
const EX = runFile('explain-data.js', ['EXPLAIN', 'EXPLAIN_TITLE']);
const PS = runFile('psuk-data.js', ['PSUK', 'PSUK_OF']);
const RA = runFile('rashi-data.js', ['RASHI_AT']);
const WBW = linesOf('WBW'), PUNCT = linesOf('PUNCT'), TAKHLES = linesOf('TAKHLES');
const DAF_LINES = constOf('DAF_LINES'), BEAT_SPAN = constOf('BEAT_SPAN'), BEAT_LOC = constOf('BEAT_LOC'), DAF_SRC = constOf('DAF_SRC');
const AMUD_NAME = constOf('AMUD_NAME'), PAGE_BOX = constOf('PAGE_BOX');
const WDICT = constOf('WDICT'), KEY_TERMS = constOf('KEY_TERMS');
const MISHNA = Object.assign(constOf('MISHNA'), blockOf('Object.assign(MISHNA, {'));
const PAIRS = Object.assign(constOf('PAIRS'), blockOf('Object.assign(PAIRS, {'));

const refs = Object.keys(BEAT_LOC).sort((a, b) => parseInt(a) - parseInt(b) || a.localeCompare(b));
const DD = path.join(ROOT, 'data', MAS); fs.mkdirSync(DD, { recursive: true });
const pick = (O, ref) => Object.fromEntries(Object.entries(O).filter(([k]) => k.split(/[:-]/)[0] === ref));
const hash = s => crypto.createHash('md5').update(s).digest('hex').slice(0, 8);
const man = { id: MAS, name: MAS_NAME, refs, names: {}, titles: {}, sums: {}, scenes: {}, marks: {}, box: {}, v: {}, iv: {} };
for (const ref of refs) {
  const pack = {
    tree: T.TREE[ref] || null, sections: T.SECTION_NAMES[ref] || [], topic: T.SUGYA_TOPIC[ref] || [], cx: T.TREE_CX[ref] || [],
    people: PEOPLE[ref] || [], context: pick(CONTEXT, ref), wbw: pick(WBW, ref), punct: pick(PUNCT, ref), takhles: pick(TAKHLES, ref),
    lines: pick(DAF_LINES, ref), span: BEAT_SPAN[ref] || {}, loc: BEAT_LOC[ref] || {}, src: DAF_SRC[ref] || {},
    explain: pick(EX.EXPLAIN, ref), psukOf: pick(PS.PSUK_OF, ref), rashiAt: pick(RA.RASHI_AT, ref),
  };
  pack.psuk = {}; for (const v of Object.values(pack.psukOf)) for (const [, k] of v) pack.psuk[k] = PS.PSUK[k];
  pack.explainTitle = {}; for (const v of Object.values(pack.explain)) for (const x of [].concat(v)) pack.explainTitle[x] = EX.EXPLAIN_TITLE[x];
  const body = `// ✳️ נוצר אוטומטית (.claude/tools/build.py) — לא לערוך ביד. כל הנתונים של ${AMUD_NAME[ref] || ref} (${MAS_NAME}).\nPAGE_IN(${JSON.stringify(ref)}, ${JSON.stringify(pack)});\n`;
  fs.writeFileSync(path.join(DD, ref + '.js'), body);
  man.v[ref] = hash(body);
  { // גרסת הצילומים של הדף (מלא + חיתוכים): משתנה כשמחליפים צילום, כדי שהטלפון לא יציג תמונה ישנה מהשמור
    const ID = path.join(ROOT, 'taanit-img'); const fsx = fs.readdirSync(ID).filter(f => f.startsWith(ref + '-') && f.endsWith('.jpg')).sort();
    man.iv[ref] = hash(fsx.map(f => f + fs.statSync(path.join(ID, f)).size + crypto.createHash('md5').update(fs.readFileSync(path.join(ID, f))).digest('hex')).join('|')); } man.names[ref] = AMUD_NAME[ref] || ref; man.box[ref] = PAGE_BOX[ref] || null;
  if (pack.tree) { man.titles[ref] = pack.tree.title; man.sums[ref] = pack.tree.sum || ''; }
  man.scenes[ref] = Math.max(pack.sections.length, ...Object.keys(pack.loc).map(k => +k + 1), 0);
  man.marks[ref] = Object.keys(pack.src).map(Number).filter(i => (pack.loc[i] || []).some(x => x)).sort((a, b) => a - b);
}
for (const f of fs.readdirSync(DD)) if (/^\d+[ab]\.js$/.test(f) && !refs.includes(f.slice(0, -3))) fs.unlinkSync(path.join(DD, f));

// common: מילון ומונחים
const common = `// ✳️ נוצר אוטומטית (.claude/tools/build.py) — לא לערוך ביד.\nconst WDICT = ${JSON.stringify(WDICT)};\nconst KEY_TERMS = ${JSON.stringify(KEY_TERMS)};\n`;
fs.writeFileSync(path.join(ROOT, 'data', 'common.js'), common);

// 🔤 לימוד מילים: מריצים את words-build.js (הקוד שהיה ב־words.html) פעם אחת כאן
const wordsSrc = fs.readFileSync(path.join(__dirname, 'words-build.js'), 'utf8');
const clean = s => String(s || '').replace(/<[^>]+>/g, '').replace(/[֑-ׇ״"׳'.,:;!?()\[\]]/g, '').replace(/\s+/g, ' ').trim();
const ctx = { TX: { WBW, PUNCT, WDICT, KEY_TERMS }, REFS: refs, clean, Map, Set, Object, String, Array };
vm.runInNewContext(wordsSrc.replace(/^const (W|ALL|FIRST) = /gm, 'var $1 = '), ctx);
// הדוגמה מהגמרא לא נשמרת כאן (כדי שהקובץ יישאר קטן): words.html טוען את הדף של המילה כשהופכים כרטיס
const WORDS = ctx.ALL.map(x => { const o = { w: x.w, m: x.m, r: x.refs, k: x.keys }; if (x.id !== clean(x.w)) o.id = x.id; if (x.type !== 'w') o.t = x.type; return o; });
fs.writeFileSync(path.join(DD, 'words.js'), `// ✳️ נוצר אוטומטית (.claude/tools/build.py) — לא לערוך ביד. לימוד מילים: ${WORDS.length} מילים.\nconst WORDS = ${JSON.stringify(WORDS)};\n`);

man.vWords = hash(fs.readFileSync(path.join(DD, 'words.js'), 'utf8'));
man.vCommon = hash(common);
fs.writeFileSync(path.join(DD, 'index.js'), `// ✳️ נוצר אוטומטית (.claude/tools/build.py) — לא לערוך ביד. המפה של מסכת ${MAS_NAME}.\nconst MAS = ${JSON.stringify(man)};\n`);
fs.mkdirSync(path.join(ROOT, '.claude', 'out'), { recursive: true });
fs.writeFileSync(path.join(ROOT, '.claude', 'out', 'pairs.json'), JSON.stringify({ MISHNA, PAIRS }));
const kb = f => Math.round(fs.statSync(f).size / 1024);
console.log(`data/${MAS}: ${refs.length} דפים · index ${kb(path.join(DD, 'index.js'))}KB · words ${kb(path.join(DD, 'words.js'))}KB (${WORDS.length}) · common ${kb(path.join(ROOT, 'data', 'common.js'))}KB`);
