// ===== לוח דיבוג זמני (להסרה אחרי שנמצא את הקפיצות) =====
// מציג בצד המסך: מצב נוכחי (קטע, שלב, גלילה) + יומן של כל מה שקרה, עם הסיבה.
// כל קפיצה מסומנת ב־⚠. כפתור 📋 מעתיק את היומן כדי להדביק בצ׳אט.
(function () {
  const T0 = Date.now();
  const log = [];
  let lastInput = { type: '', t: 0, where: '' };
  const now = () => ((Date.now() - T0) / 1000).toFixed(1);
  const css = `
  #dbg { position: fixed; left: 2px; top: 30vh; z-index: 9999; width: 142px; max-height: 42vh; opacity: .9; display: flex; flex-direction: column;
    background: rgba(0,0,0,.82); color: #cfe; font: 9.5px/1.3 monospace; direction: rtl; border: 1px solid #4a8; border-radius: 8px; }
  #dbg.min { width: auto; max-height: none; }
  #dbg.min .dbg-body, #dbg.min .dbg-st { display: none; }
  #dbg .dbg-bar { display: flex; gap: 4px; padding: 3px; }
  #dbg button { font: 13px sans-serif; background: #234; color: #fff; border: 0; border-radius: 5px; padding: 3px 6px; }
  #dbg .dbg-st { padding: 2px 5px; color: #ff8; border-bottom: 1px solid #355; white-space: pre-wrap; }
  #dbg .dbg-body { overflow-y: auto; padding: 2px 5px 5px; }
  #dbg .dbg-body div { border-bottom: 1px dotted #244; padding: 1px 0; }
  #dbg .w { color: #f88; font-weight: bold; }
  #dbg .s { color: #8cf; }
  #dbg .b { color: #9e9; }`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const box = document.createElement('div'); box.id = 'dbg';
  box.innerHTML = `<div class="dbg-bar"><button id="dbgMin">🐞</button><button id="dbgCopy">📋</button><button id="dbgClr">🗑</button></div><div class="dbg-st" id="dbgSt"></div><div class="dbg-body" id="dbgBody"></div>`;
  document.body.appendChild(box);
  ['touchstart', 'touchmove', 'touchend'].forEach(t => box.addEventListener(t, e => e.stopPropagation(), { passive: true }));
  const body = box.querySelector('#dbgBody'), stEl = box.querySelector('#dbgSt');
  function add(msg, cls) {
    log.push(`${now()} ${msg}`);
    if (log.length > 300) log.shift();
    const d = document.createElement('div'); if (cls) d.className = cls;
    d.textContent = `${now()} ${msg}`;
    body.prepend(d);
    while (body.children.length > 80) body.lastChild.remove();
  }
  window.dbgLog = add;
  box.querySelector('#dbgMin').onclick = () => box.classList.toggle('min');
  box.querySelector('#dbgClr').onclick = () => { log.length = 0; body.innerHTML = ''; };
  box.querySelector('#dbgCopy').onclick = () => {
    const txt = `${navigator.userAgent}\n${innerWidth}x${innerHeight}\n` + log.join('\n');
    (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => add('✓ הועתק'), () => {
      const ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); add('✓ הועתק'); } catch (e) { add('✗ לא הועתק'); } ta.remove();
    });
  };
  const where = t => !t || !t.closest ? '?' : t.closest('.src-wrap') ? 'צילום' : t.closest('.beat') ? 'כרטיס' : t.closest('.photo-overlay') ? 'דף-מלא' : t.closest('button') ? 'כפתור' : 'דף';
  const cause = () => Date.now() - lastInput.t < 900 ? `${lastInput.type}@${lastInput.where}` : 'לבד';

  // ---- קלט של המשתמש ----
  let tStart = null;
  document.addEventListener('touchstart', e => {
    if (box.contains(e.target)) return;
    const t = e.touches[0]; tStart = { x: t.clientX, y: t.clientY, at: Date.now() };
    lastInput = { type: 'מגע', t: Date.now(), where: where(e.target) };
    add(`👆 מגע ${lastInput.where} (${e.touches.length} אצבעות)`);
  }, { passive: true, capture: true });
  document.addEventListener('touchend', e => {
    if (box.contains(e.target) || !tStart) return;
    const t = e.changedTouches[0];
    lastInput = { type: 'שחרור', t: Date.now(), where: where(e.target) };
    add(`✋ שחרור dx=${Math.round(t.clientX - tStart.x)} dy=${Math.round(t.clientY - tStart.y)} ${Date.now() - tStart.at}ms`);
  }, { passive: true, capture: true });
  document.addEventListener('click', e => { if (!box.contains(e.target)) { lastInput = { type: 'לחיצה', t: Date.now(), where: where(e.target) }; add(`🖱 לחיצה ${lastInput.where}`); } }, true);

  // ---- גלילה: מזהים קפיצות ----
  let lastY = scrollY, lastYt = Date.now(), progScroll = 0;
  addEventListener('scroll', () => {
    const dy = scrollY - lastY, dt = Date.now() - lastYt;
    if (Math.abs(dy) > 220 && dt < 60 && Date.now() > progScroll) add(`⚠ קפיצת גלילה ${Math.round(lastY)}→${Math.round(scrollY)} (${cause()})`, 'w');
    lastY = scrollY; lastYt = Date.now();
  }, { passive: true });
  const srcLast = new WeakMap();
  document.addEventListener('scroll', e => {
    const w = e.target; if (!w.classList || !w.classList.contains('src-wrap')) return;
    const p = srcLast.get(w) || [w.scrollTop, w.scrollLeft];
    const d = Math.abs(w.scrollTop - p[0]) + Math.abs(w.scrollLeft - p[1]);
    if (d > 60) add(`📷 הצילום זז ${Math.round(d)}px (${w.__prog && Date.now() - w.__prog < 700 ? 'האתר הזיז' : cause()})`, w.__prog && Date.now() - w.__prog < 700 && lastInput.where === 'צילום' && Date.now() - lastInput.t < 1500 ? 'w' : '');
    srcLast.set(w, [w.scrollTop, w.scrollLeft]);
  }, true);
  // הזזה של הצילום ע״י הקוד
  for (const prop of ['scrollTop', 'scrollLeft']) {
    const d = Object.getOwnPropertyDescriptor(Element.prototype, prop);
    Object.defineProperty(Element.prototype, prop, { configurable: true, get() { return d.get.call(this); },
      set(v) { if (this.classList && this.classList.contains('src-wrap')) { this.__prog = Date.now(); if (Math.abs(d.get.call(this) - v) > 30) add(`🤖 האתר מזיז צילום ${prop === 'scrollTop' ? '↕' : '↔'} ${Math.round(d.get.call(this))}→${Math.round(v)} (${cause()})`, 's'); } d.set.call(this, v); } });
  }
  const oScrollTo = window.scrollTo.bind(window);
  window.scrollTo = function (a, b) { progScroll = Date.now() + 900; add(`🤖 גלילת דף ע״י האתר → ${typeof a === 'object' ? a.top : b} (${cause()})`, 's'); return oScrollTo(a, b); };
  const oSIV = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function (o) { progScroll = Date.now() + 900; add(`🤖 scrollIntoView ${this.className.split(' ')[0]} (${cause()})`, 's'); return oSIV.call(this, o); };
  addEventListener('resize', () => add(`↔ שינוי גודל ${innerWidth}x${innerHeight}`));

  // ---- פונקציות האתר ----
  const wrap = (name, fmt, cls) => {
    const f = window[name]; if (typeof f !== 'function') return;
    window[name] = function (...a) { const before = { s: state.sceneIdx, b: typeof focusBeat !== 'undefined' ? focusBeat : null }; const r = f.apply(this, a); const m = fmt(a, before, r); if (m) add(m, cls); return r; };
  };
  wrap('changeScene', (a, bf) => `⏭ קטע ${bf.s}→${state.sceneIdx} (${cause()})`, 'w');
  wrap('goToRef', a => `📄 עמוד ${a[0]} (${cause()})`, 'w');
  wrap('stepBeat', (a, bf, r) => r ? `⤵ stepBeat ${a[0]} (${cause()})` : '', 's');
  wrap('openPhoto', () => `🖼 נפתח הדף המלא (${cause()})`);
  wrap('showLoc', (a, bf) => bf.b !== focusBeat || !window.__dbgLastBeat || window.__dbgLastBeat !== `${state.sceneIdx}:${focusBeat}` ? (window.__dbgLastBeat = `${state.sceneIdx}:${focusBeat}`, `🎯 שלב ${focusBeat == null ? '-' : focusBeat + 1} בקטע ${state.sceneIdx} (${cause()})`) : '', 'b');

  // ---- שורת מצב ----
  setInterval(() => {
    const w = document.querySelector('.scene.active .src-wrap');
    stEl.textContent = `עמוד ${state.ref} קטע ${state.sceneIdx}\nשלב ${focusBeat == null ? '-' : focusBeat + 1}  גלילה ${Math.round(scrollY)}\nצילום ↕${w ? Math.round(w.scrollTop) : '-'} ↔${w ? Math.round(w.scrollLeft) : '-'}`;
  }, 250);
  add('🐞 דיבוג פעיל');
})();
