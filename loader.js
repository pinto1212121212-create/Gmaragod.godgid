// 📦 טוען הנתונים לפי דף — משותף לדף הלימוד (taanit.html) ולעץ (tree.html).
// לפני הקובץ הזה נטענים: data/common.js (WDICT, KEY_TERMS) ו־data/<מסכת>/index.js (MAS = המפה של המסכת).
// הנתונים של כל דף נמצאים ב־data/<מסכת>/<ref>.js (נבנים ע״י .claude/tools/build.py), ובסופם PAGE_IN(ref, {...}).
// כך האתר נטען באותה מהירות גם כשיהיו בו אלפי דפים: נטען רק הדף שצריך.

const TREE = {}, SECTION_NAMES = {}, SUGYA_TOPIC = {}, TREE_CX = {}, PEOPLE = {}, CONTEXT = {};
const WBW = {}, PUNCT = {}, TAKHLES = {}, DAF_LINES = {}, BEAT_SPAN = {}, BEAT_LOC = {}, DAF_SRC = {}, BEAT_WORDS = {};
const EXPLAIN = {}, EXPLAIN_TITLE = {}, TREE_SECS = {};
const PSUK = {}, PSUK_OF = {}, RASHI_AT = {};   // 📜 RASHI_AT: רש״י צמוד לשלב (rashi-data.js)   // 📖 הפסוק במקומו (psuk-data.js)
const TX = { WBW, PUNCT, TAKHLES, WDICT: typeof WDICT !== 'undefined' ? WDICT : {}, KEY_TERMS: typeof KEY_TERMS !== 'undefined' ? KEY_TERMS : [] };
// 🧑 דמויות עם כיפה (במקום אמוג׳י של אנשים): KIP.man / elder / young / two. נבנה ב־.claude/tools/explain/kip.py
const KIP = {"man": "<svg class=\"kip\" viewBox=\"0 0 48 48\" width=\"1.20em\" height=\"1.2em\" style=\"vertical-align:-.25em\" aria-hidden=\"true\"><circle cx=\"24\" cy=\"25\" r=\"13\" fill=\"#f2c9a0\"/><path d=\"M11 22c-1 4 0 7 2 9M37 22c1 4 0 7-2 9\" stroke=\"#5a3b22\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M11 25c0 9 6 16 13 16s13-7 13-16c-3 5-8 7-13 7s-10-2-13-7z\" fill=\"#5a3b22\"/><circle cx=\"19.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><circle cx=\"28.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><path d=\"M12.5 17.5a11.5 7.5 0 0 1 23 0z\" fill=\"#1b2654\"/><path d=\"M12.5 17.5h23\" stroke=\"#e8b76d\" stroke-width=\"1.3\"/></svg>", "elder": "<svg class=\"kip\" viewBox=\"0 0 48 48\" width=\"1.20em\" height=\"1.2em\" style=\"vertical-align:-.25em\" aria-hidden=\"true\"><circle cx=\"24\" cy=\"25\" r=\"13\" fill=\"#f2c9a0\"/><path d=\"M11 22c-1 4 0 7 2 9M37 22c1 4 0 7-2 9\" stroke=\"#ece7dc\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M11 25c0 13 6 20 13 20s13-7 13-20c-3 5-8 7-13 7s-10-2-13-7z\" fill=\"#ece7dc\"/><circle cx=\"19.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><circle cx=\"28.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><path d=\"M12.5 17.5a11.5 7.5 0 0 1 23 0z\" fill=\"#1b2654\"/><path d=\"M12.5 17.5h23\" stroke=\"#e8b76d\" stroke-width=\"1.3\"/></svg>", "young": "<svg class=\"kip\" viewBox=\"0 0 48 48\" width=\"1.20em\" height=\"1.2em\" style=\"vertical-align:-.25em\" aria-hidden=\"true\"><circle cx=\"24\" cy=\"25\" r=\"13\" fill=\"#f2c9a0\"/><path d=\"M11 22c-1 4 0 7 2 9M37 22c1 4 0 7-2 9\" stroke=\"#4a3423\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M20 31q4 3 8 0\" stroke=\"#9a5a3a\" stroke-width=\"1.6\" fill=\"none\" stroke-linecap=\"round\"/><circle cx=\"19.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><circle cx=\"28.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><path d=\"M12.5 17.5a11.5 7.5 0 0 1 23 0z\" fill=\"#1b2654\"/><path d=\"M12.5 17.5h23\" stroke=\"#e8b76d\" stroke-width=\"1.3\"/></svg>", "two": "<svg class=\"kip\" viewBox=\"0 0 80 48\" width=\"2.00em\" height=\"1.2em\" style=\"vertical-align:-.25em\" aria-hidden=\"true\"><circle cx=\"25\" cy=\"25\" r=\"13\" fill=\"#f2c9a0\"/><path d=\"M12 22c-1 4 0 7 2 9M38 22c1 4 0 7-2 9\" stroke=\"#5a3b22\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M12 25c0 9 6 16 13 16s13-7 13-16c-3 5-8 7-13 7s-10-2-13-7z\" fill=\"#5a3b22\"/><circle cx=\"20.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><circle cx=\"29.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><path d=\"M13.5 17.5a11.5 7.5 0 0 1 23 0z\" fill=\"#3a2a5a\"/><path d=\"M13.5 17.5h23\" stroke=\"#e8b76d\" stroke-width=\"1.3\"/><circle cx=\"55\" cy=\"25\" r=\"13\" fill=\"#f2c9a0\"/><path d=\"M42 22c-1 4 0 7 2 9M68 22c1 4 0 7-2 9\" stroke=\"#6b4a2a\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M42 25c0 9 6 16 13 16s13-7 13-16c-3 5-8 7-13 7s-10-2-13-7z\" fill=\"#6b4a2a\"/><circle cx=\"50.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><circle cx=\"59.5\" cy=\"24\" r=\"1.7\" fill=\"#2a1d12\"/><path d=\"M43.5 17.5a11.5 7.5 0 0 1 23 0z\" fill=\"#1b2654\"/><path d=\"M43.5 17.5h23\" stroke=\"#e8b76d\" stroke-width=\"1.3\"/></svg>"};
const PACKS = new Set(), PACK_WAIT = {};
// 📖 ״הפסוק במקומו״ לשלב אחד או לכמה (בעץ: כל המפתחות של הצומת)
function psukHTML(keys) {
  const seen = new Set(), out = [];
  for (const k of [].concat(keys)) for (const [ref, id] of (PSUK_OF[k] || [])) { if (seen.has(id)) continue; seen.add(id); const e = PSUK[id]; if (e) out.push(`<div class="psk"><div class="psk-h"><b>${ref}</b><span>${e[0]}</span></div><p>${e[1]}</p></div>`); }
  return out.join('');
}
// 📜 רש״י של שלב (או של כמה שלבים): דיבור המתחיל, לשון רש״י, ובפשטות
function rashiHTML(keys) {
  const out = [];
  for (const k of [].concat(keys)) (RASHI_AT[k] || []).forEach(([dh, r, p], i) => out.push(`<div class="rsi" data-rs="${k}#${i}"><div class="rsi-dh">${dh}</div><div class="rsi-t">${r}</div>${p ? `<div class="rsi-p"><b>בפשטות:</b> ${p}</div>` : ''}</div>`));
  return out.join('');
}
// לשונית רש״י — תמיד קיימת: רש״י של השלב; אם אין — רש״י על שאר הקטע; ואם גם לא — רש״י המסוכם של הדף
function rashiTabHTML(keys) {
  keys = [].concat(keys).filter(Boolean);
  const own = rashiHTML(keys); if (own) return own;
  const k0 = keys[0]; if (!k0) return '';
  const [ref, si] = k0.split(':'), pre = ref + ':' + si + ':';
  const sc = Object.keys(RASHI_AT).filter(k => k.startsWith(pre)).sort((a, b) => +a.split(':')[2] - +b.split(':')[2]);
  if (sc.length) return '<div class="rs-none">על השלב הזה רש״י לא מפרש. רש״י על הקטע:</div>' + sc.map(k => rashiHTML(k)).join('');
  const am = typeof amudim !== 'undefined' && amudim[ref] && amudim[ref].rashi;
  if (am && am.length) return '<div class="rs-none">רש״י על הדף (בקיצור):</div>' + am.map(e => `<div class="rsi"><div class="rsi-dh">${e.dh}</div><div class="rsi-t">${e.content}</div></div>`).join('');
  return '<div class="rs-none">אין כאן פירוש רש״י.</div>';
}
// בטקסט הגמרא: מסמנים את ״דיבור המתחיל״ של רש״י בקו זהב (הקשה — פותחת את רש״י)
function rashiMark(html, keys) {
  const NK = '[\\u0591-\\u05C7]*', SEP = '(?:[\\s,.:;?!״"׳\'—\\-–()\\[\\]]|<[^>]+>)+';
  for (const k of [].concat(keys)) (RASHI_AT[k] || []).forEach(([dh], i) => {
    const words = dh.replace(/[״"׳'.,:;?!()]/g, ' ').trim().split(/\s+/).filter(Boolean); if (!words.length) return;
    const rx = new RegExp('(' + words.map(w => [...w].map(c => c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + NK).join('')).join(SEP) + ')');
    // באמצע יכולות להיות תגיות (<q> של ציטוט): SEP מדלג עליהן, וכל קטע טקסט נעטף בנפרד כדי לא לשבור את ה־HTML
    const m = rx.exec(html); if (!m) return;
    const seg = m[0].replace(/(<[^>]+>)|([^<]+)/g, (q, tag, txt) => tag ? tag : `<mark class="rs-dh" data-rs="${k}#${i}">${txt}</mark>`);
    html = html.slice(0, m.index) + seg + html.slice(m.index + m[0].length);
  });
  return html;
}
// הקשה על מילים מסומנות: עוברים ללשונית רש״י (בסרגל, בדף המלא או בעץ) ומדגישים את הפירוש
document.addEventListener('click', e => {
  const m = e.target.closest && e.target.closest('.rs-dh'); if (!m) return;
  e.stopPropagation(); const id = m.dataset.rs;
  { const b = m.closest('.ed-page [data-j]'); if (b && typeof edSelect === 'function') edSelect(+b.dataset.j); }   // במהדורה שלנו: קודם בוחרים את השלב
  const tab = m.closest('.ed-page') ? document.querySelector('#edCall .po-tab[data-pt="rs"]') : m.closest('.po-tools') ? m.closest('.po-tools').querySelector('.po-tab[data-pt="rs"]') : document.querySelector('#dockTabs .dock-tab[data-dk="rs"]') || document.querySelector('.sh-tab[data-t="rs"]');
  if (tab && !tab.classList.contains('on')) tab.click();
  setTimeout(() => { const it = [...document.querySelectorAll('.rsi')].find(x => x.dataset.rs === id && x.offsetParent); if (it) { it.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); it.classList.remove('flash'); void it.offsetWidth; it.classList.add('flash'); } }, 80);
}, true);
// כתובת צילום עם גרסה (MAS.iv) — כשמחליפים צילום, הטלפון מוריד את החדש ולא מציג את השמור
const imgUrl = (ref, part) => `taanit-img/${ref}-${part}.jpg${typeof MAS !== 'undefined' && MAS.iv && MAS.iv[ref] ? '?i=' + MAS.iv[ref] : ''}`;
// 📜 דפים במהדורה שלנו: אין בהם צילום של שום הוצאה — רק טקסט מעומד אצלנו (המשתמש: ״כל דף שאתה מתקן — תוריד את הדף של ווגשל לגמרי״)
const EDITION = new Set(['2a', '2b', '3a', '3b', '4a', '4b', '5a', '5b', '6a', '6b', '7a', '7b', '8a', '8b', '9a', '9b', '10a']);
const edTxt = t => (t || '').replace(/[\u0591-\u05C7]/g, '').replace(/\s*\([^()]*,[^()]*\)/g, '').replace(/\s*\((ממשיך|ההמשך)[^)]*\)/g, '');
const masHas = ref => typeof MAS !== 'undefined' && MAS.refs.includes(ref);

// נקרא מתוך data/<מסכת>/<ref>.js
function PAGE_IN(ref, d) {
  if (d.tree) TREE[ref] = d.tree;
  SECTION_NAMES[ref] = d.sections; SUGYA_TOPIC[ref] = d.topic; TREE_CX[ref] = d.cx; PEOPLE[ref] = d.people;
  Object.assign(CONTEXT, d.context); Object.assign(WBW, d.wbw); Object.assign(PUNCT, d.punct); Object.assign(TAKHLES, d.takhles);
  Object.assign(DAF_LINES, d.lines); BEAT_SPAN[ref] = d.span; BEAT_LOC[ref] = d.loc; DAF_SRC[ref] = d.src;
  Object.assign(EXPLAIN, d.explain); Object.assign(EXPLAIN_TITLE, d.explainTitle);
  Object.assign(PSUK, d.psuk || {}); Object.assign(PSUK_OF, d.psukOf || {}); Object.assign(RASHI_AT, d.rashiAt || {});
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
