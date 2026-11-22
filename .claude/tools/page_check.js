// ✅ בדיקת שלמות לדף: האם נעשה *כל* מה שצריך בדף חדש. שימוש: node .claude/tools/page_check.js 9b   (או בלי ref — כל הדפים)
// עובר על הקבצים הבנויים (אחרי build.py) ועל המקורות, ומדפיס ✓ / ✗ לכל פריט ברשימה של CLAUDE.md (סעיף 4).
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', '..'); const rd = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
const src = rd('.claude/src/taanit.src.html');
const grab = name => { const i = src.indexOf('const ' + name + ' = {'); if (i < 0) return {}; let d = 0, j = src.indexOf('{', i);
  for (let k = j; ; k++) { if (src[k] === '{') d++; else if (src[k] === '}' && --d === 0) return eval('(' + src.slice(j, k + 1) + ')'); } };
const ED_LINES = grab('ED_LINES'), ED_GEO = grab('ED_GEO'), AMUD_NAME = grab('AMUD_NAME');
const EDITION = (rd('loader.js').match(/const EDITION = new Set\(\[([^\]]*)\]/) || [, ''])[1];
const idx = rd('index.html'), words = rd('words.html');
const refs = process.argv[2] ? [process.argv[2]] : Object.keys(AMUD_NAME);
let bad = 0;
// יוצאים מן הכלל מתועדים (לא חסר — כך בדף): ב־ו. אין תוספות על הגמרא שבצילום; דף בלי פסוקים — אין ״הפסוק״.
const NO_TOS = new Set(['6a']);
for (const ref of refs) {
  const out = []; const ok = (c, t, extra = '') => { out.push(`${c ? '✓' : '✗'} ${t}${extra ? ' — ' + extra : ''}`); if (!c) bad++; };
  const packF = path.join(ROOT, 'data/taanit', ref + '.js'), dataF = path.join(ROOT, 'taanit-data', ref + '.js');
  if (!fs.existsSync(packF) || !fs.existsSync(dataF)) { console.log(`\n${ref}: ✗ אין חבילת דף (להריץ build.py)`); bad++; continue; }
  let P; global.PAGE_IN = (r, o) => P = o; eval(fs.readFileSync(packF, 'utf8'));
  const amudim = { [ref]: {} }; global.MISHNA = {}; global.PAIRS = {};
  // הקובץ משתמש בעזרים של הדף (kv, kn, KIP, VZ...) — כל שם לא מוכר = פונקציה/אובייקט ריק
  const dummy = new Proxy(function () { return ''; }, { get: (t, k) => k === Symbol.toPrimitive ? () => '' : dummy, apply: () => '' });
  const env = new Proxy({ amudim, MISHNA: global.MISHNA, PAIRS: global.PAIRS }, { has: (t, k) => k !== 'Object' && k !== 'Array' && k !== 'JSON' && k !== 'String' && k !== 'Math', get: (t, k) => k === Symbol.unscopables ? undefined : k in t ? t[k] : dummy });
  new Function('env', 'with (env) {' + fs.readFileSync(dataF, 'utf8') + '\n}')(env);
  const sc = amudim[ref].scenes || [];
  const beats = sc.flatMap((s, si) => (s.beats || []).map((b, bi) => ({ k: `${ref}:${si}:${bi}`, si, bi })));
  const inDaf = b => P.loc && P.loc[b.si] && P.loc[b.si][b.bi];   // שלב שיש לו מקום בדף
  const miss = (obj, list) => list.filter(b => !(obj || {})[b.k]).map(b => b.k);
  const dafBeats = beats.filter(inDaf);
  ok(sc.length > 0, `קטעים: ${sc.length}, שלבים: ${beats.length} (בדף: ${dafBeats.length})`);
  let m;
  m = miss(P.takhles, beats); ok(!m.length, 'בתכלס (TAKHLES) לכל שלב', m.slice(0, 6).join(' '));
  m = miss(P.context, beats); ok(!m.length, 'הקשר (CONTEXT) לכל שלב', m.slice(0, 6).join(' '));
  m = miss(P.punct, dafBeats); ok(!m.length, 'גמרא מפוסקת (PUNCT) לכל שלב שבדף', m.slice(0, 6).join(' '));
  m = miss(P.wbw, dafBeats); ok(!m.length, 'מילה במילה (WBW) לכל שלב שבדף', m.slice(0, 6).join(' '));
  m = miss(P.span && Object.fromEntries(Object.entries(P.span).flatMap(([si, o]) => Object.keys(o).map(bi => [`${ref}:${si}:${bi}`, 1]))), dafBeats);
  ok(EDITION.includes(`'${ref}'`) || !m.length, 'הדגשה (BEAT_SPAN) — או מהדורה', m.slice(0, 6).join(' '));
  m = sc.map((s, si) => si).filter(si => ((P.loc || {})[si] || []).some(x => x) && !(P.src || {})[si]); ok(!m.length, 'DAF_SRC לכל קטע (בלעדיו אין סימון בתצוגה הרגילה)', m.join(' '));
  { const W = new Function(fs.readFileSync(path.join(ROOT, 'data/common.js'), 'utf8') + ';return WDICT')(); let a = 0, b = 0;
    for (const k in P.wbw || {}) for (const x of P.wbw[k].split('|')) { const w = x.split('=')[0].trim(); if (!w) continue; a++; if (W[w]) b++; }
    (parseInt(ref) >= 10 ? ok : (c, t, x) => out.push(`  · ${t}`))(!a || b / a >= .7, `מילון (WDICT) מכסה את מילה־במילה: ${a ? Math.round(100 * b / a) : 0}% (להריץ wdict_fill.py)`); }
  const nodes = []; const walk = n => { nodes.push(n); (n.k || []).forEach(walk); }; ((P.tree || {}).roots || []).forEach(walk);
  ok(nodes.length > 0, `עץ הסוגיה (TREE): ${nodes.length} צמתים`);
  ok((P.cx || []).length === nodes.length, 'TREE_CX לכל צומת', `${(P.cx || []).length}/${nodes.length}`);
  ok((P.sections || []).length === sc.length, 'SECTION_NAMES לכל קטע', `${(P.sections || []).length}/${sc.length}`);
  ok((P.topic || []).length === ((P.tree || {}).roots || []).length, 'SUGYA_TOPIC לכל סוגיה');
  ok((P.people || []).length > 0, `אנשים (PEOPLE): ${(P.people || []).length}`);
  const rk = Object.keys(P.rashiAt || {}); ok(rk.length > 0, `רש״י מלא (RASHI_AT): ${rk.reduce((t, k) => t + P.rashiAt[k].length, 0)} דיבורים`);
  const nz = t => t.replace(/[֑-ׇ]/g, '').replace(/<[^>]+>/g, '');
  const unm = rk.flatMap(k => P.rashiAt[k].filter(e => !nz((P.punct || {})[k] || '').includes(nz(e[0]).replace(/״|"/g, ''))).map(e => k + ' ' + e[0]));
  // דפים ישנים (ב.–ט:) — מידע; מדף י. והלאה — חובה
  (parseInt(ref) >= 10 ? ok : (c, t, x) => out.push(`  · ${t}${x ? ' — ' + x : ''}`))(unm.length <= 2, `דיבורי רש״י מסומנים בגמרא (כתיב כמו ב־PUNCT; עד 2 חריגים)`, unm.length ? unm.length + ': ' + unm.slice(0, 4).join(' | ') : '');
  ok(!!fs.existsSync(path.join(ROOT, '.claude/tools/rashi', ref + '.py')), 'מקור רש״י: .claude/tools/rashi/' + ref + '.py');
  ok(NO_TOS.has(ref) || !!(amudim[ref].tosafot || []).length, 'תוספות (amudim.tosafot)');
  ok(!!(amudim[ref].translation || []).length, 'תרגום (amudim.translation)');
  const L = ED_LINES[ref]; ok(!!L, 'מהדורה: ED_LINES (שורות הגמרא כמו בדף)'); ok(!!(L && L.tos && L.tos.length), 'מהדורה: תוספות מלא (ED_LINES.tos)');
  ok(EDITION.includes(`'${ref}'`), 'מהדורה: ב־EDITION (loader.js)');
  out.push(`  · צורת רש״י/תוספות במהדורה: ${ED_GEO[ref] ? (ED_GEO[ref].flow ? 'זרימה ידנית' : 'שורה־שורה כמו בדף ✓') : 'זרימה אוטומטית (לשורה־שורה צריך צילום PDF/מסך)'}`);
  const wc = Object.values(P.context || {}).join(' ').split('מילה קשה').length - 1;
  ok(fs.existsSync(path.join(ROOT, '.claude/tools/words', ref + '.py')) && wc > 0, `״מילה קשה״ (words/${ref}.py): ${wc}`);
  { const n = Object.keys(P.psukOf || {}).length, hasV = Object.values(P.punct || {}).some(t => /\([^)]*[א-ת]+ [א-ת]{1,3},/.test(t));
    if (n || hasV) ok(n > 0, `״הפסוק״ (PSUK_OF): ${n} שלבים`); else out.push('  · ״הפסוק״: אין פסוקים עם מראה מקום בדף'); }
  ok(Object.keys(P.explain || {}).length > 0, `הסבר מאויר (EXPLAIN): ${Object.keys(P.explain || {}).length} קטעים`);
  ok(!!AMUD_NAME[ref] && idx.includes(`'${ref}':`) && words.includes(`'${ref}':`), 'שם הדף: AMUD_NAME + AM (index.html) + AMN (words.html)');
  console.log(`\n${ref} (${AMUD_NAME[ref] || '?'}):\n  ` + out.join('\n  '));
}
console.log(bad ? `\n✗ חסרים ${bad} פריטים` : '\n✓ הכל קיים');
process.exit(bad ? 1 : 0);
