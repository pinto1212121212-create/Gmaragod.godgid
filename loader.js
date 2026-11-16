// 📦 טוען הנתונים לפי דף — משותף לדף הלימוד (taanit.html) ולעץ (tree.html).
// לפני הקובץ הזה נטענים: data/common.js (WDICT, KEY_TERMS) ו־data/<מסכת>/index.js (MAS = המפה של המסכת).
// הנתונים של כל דף נמצאים ב־data/<מסכת>/<ref>.js (נבנים ע״י .claude/tools/build.py), ובסופם PAGE_IN(ref, {...}).
// כך האתר נטען באותה מהירות גם כשיהיו בו אלפי דפים: נטען רק הדף שצריך.

const TREE = {}, SECTION_NAMES = {}, SUGYA_TOPIC = {}, TREE_CX = {}, PEOPLE = {}, CONTEXT = {};
const WBW = {}, PUNCT = {}, TAKHLES = {}, DAF_LINES = {}, BEAT_SPAN = {}, BEAT_LOC = {}, DAF_SRC = {}, BEAT_WORDS = {};
const EXPLAIN = {}, EXPLAIN_TITLE = {}, TREE_SECS = {};
const TX = { WBW, PUNCT, TAKHLES, WDICT: typeof WDICT !== 'undefined' ? WDICT : {}, KEY_TERMS: typeof KEY_TERMS !== 'undefined' ? KEY_TERMS : [] };
const PACKS = new Set(), PACK_WAIT = {};
const masHas = ref => typeof MAS !== 'undefined' && MAS.refs.includes(ref);

// נקרא מתוך data/<מסכת>/<ref>.js
function PAGE_IN(ref, d) {
  if (d.tree) TREE[ref] = d.tree;
  SECTION_NAMES[ref] = d.sections; SUGYA_TOPIC[ref] = d.topic; TREE_CX[ref] = d.cx; PEOPLE[ref] = d.people;
  Object.assign(CONTEXT, d.context); Object.assign(WBW, d.wbw); Object.assign(PUNCT, d.punct); Object.assign(TAKHLES, d.takhles);
  Object.assign(DAF_LINES, d.lines); BEAT_SPAN[ref] = d.span; BEAT_LOC[ref] = d.loc; DAF_SRC[ref] = d.src;
  Object.assign(EXPLAIN, d.explain); Object.assign(EXPLAIN_TITLE, d.explainTitle);
  for (const [k, v] of Object.entries(d.wbw)) BEAT_WORDS[k] = v.split('|').map(p => p.split('=')[0].trim()).join(' ');
  if (d.tree) { const set = new Set(), w = n => { set.add(n.s); (n.k || []).forEach(w); }; d.tree.roots.forEach(w); TREE_SECS[ref] = [...set]; }
  PACKS.add(ref);
  if (PACK_WAIT[ref]) { PACK_WAIT[ref].res(true); delete PACK_WAIT[ref]; }
}

// טוען script פעם אחת, עם עד 3 ניסיונות חוזרים (רשת חלשה)
function loadScript(url, onFail) {
  return new Promise(res => {
    const go = n => {
      const s = document.createElement('script');
      s.src = url + (n ? (url.includes('?') ? '&' : '?') + 'r=' + n : '');
      s.onload = () => res(true);
      s.onerror = () => { s.remove(); if (n < 3) setTimeout(() => go(n + 1), 700 * (n + 1)); else { if (onFail) onFail(); res(false); } };
      document.head.appendChild(s);
    };
    go(0);
  });
}

function loadPack(ref) {
  if (PACKS.has(ref)) return Promise.resolve(true);
  if (!masHas(ref)) return Promise.resolve(false);
  if (PACK_WAIT[ref]) return PACK_WAIT[ref].p;
  let res; const p = new Promise(r => res = r); PACK_WAIT[ref] = { p, res };
  loadScript(`data/${MAS.id}/${ref}.js?v=${MAS.v[ref]}`).then(ok => { if (!ok && PACK_WAIT[ref]) { PACK_WAIT[ref].res(false); delete PACK_WAIT[ref]; } });
  return p;
}
