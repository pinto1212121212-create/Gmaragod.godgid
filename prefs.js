// ♿ הגדרות נוחות ונגישות — משותף לכל הדפים (נטען מוקדם ב־<head>).
// נשמר ב־localStorage 'gemara:prefs' = {hc, rm, ls, fz}. מוחל כמחלקות על <html>:
//   hc = ניגודיות גבוהה · rm = בלי תנועה · ls = שורות מרווחות · --fz = גודל אותיות (gemara:fz, 0..4)
(function () {
  const H = document.documentElement;
  window.PREFS = { hc: false, rm: false, ls: false };
  try { Object.assign(PREFS, JSON.parse(localStorage.getItem('gemara:prefs') || '{}')); } catch (e) {}
  const FZ = [0.92, 1, 1.1, 1.22, 1.36];
  window.prefApply = function () {
    H.classList.toggle('p-hc', !!PREFS.hc); H.classList.toggle('p-rm', !!PREFS.rm); H.classList.toggle('p-ls', !!PREFS.ls);
    let i = 1; try { const v = localStorage.getItem('gemara:fz'); if (v !== null && FZ[+v]) i = +v; } catch (e) {}
    H.style.setProperty('--fz', FZ[i]);
  };
  window.prefSet = function (k, v) { PREFS[k] = v; try { localStorage.setItem('gemara:prefs', JSON.stringify(PREFS)); } catch (e) {} prefApply(); };
  prefApply();
  // 🔊 הקראה בקול (Web Speech, עברית). speak(טקסט, כפתור) — לחיצה שנייה עוצרת.
  let curBtn = null;
  window.canSpeak = 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';
  window.speak = function (text, btn) {
    if (!canSpeak) return;
    const was = curBtn; speechSynthesis.cancel(); if (curBtn) { curBtn.classList.remove('on'); curBtn.setAttribute('aria-pressed', 'false'); } curBtn = null;
    if (btn && was === btn) return;
    const u = new SpeechSynthesisUtterance(String(text).replace(/[״"]/g, '').replace(/\s+/g, ' '));
    u.lang = 'he-IL'; u.rate = 0.95;
    const v = speechSynthesis.getVoices().find(x => /^he|^iw/i.test(x.lang)); if (v) u.voice = v;
    if (btn) { curBtn = btn; btn.classList.add('on'); btn.setAttribute('aria-pressed', 'true'); }
    u.onend = u.onerror = () => { if (curBtn === btn && btn) { btn.classList.remove('on'); btn.setAttribute('aria-pressed', 'false'); curBtn = null; } };
    speechSynthesis.speak(u);
  };
  window.addEventListener('pagehide', () => { try { speechSynthesis.cancel(); } catch (e) {} });
  // לוח הגדרות (משותף): מחזיר HTML; prefBind(שורש) מחבר את הכפתורים
  window.prefsHTML = function () {
    const sw = (k, t, d) => `<label class="pf-row"><span><b>${t}</b><small>${d}</small></span><input type="checkbox" class="pf-sw" data-pf="${k}" ${PREFS[k] ? 'checked' : ''}></label>`;
    let fi = 1; try { const v = localStorage.getItem('gemara:fz'); if (v !== null && FZ[+v]) fi = +v; } catch (e) {}
    return `<div class="pf-box" role="group" aria-label="נוחות ונגישות">
      <div class="pf-row"><span><b>🔠 גודל אותיות</b><small>בכרטיסים, בהסברים ובגמרא</small></span><span class="pf-fz"><button type="button" data-fz="-1" aria-label="אותיות קטנות יותר">א−</button><output aria-live="polite">${Math.round(FZ[fi] * 100)}%</output><button type="button" data-fz="1" aria-label="אותיות גדולות יותר">א+</button></span></div>
      ${sw('hc', '🌓 ניגודיות גבוהה', 'טקסט בהיר יותר ומסגרות ברורות')}
      ${sw('ls', '📏 שורות מרווחות', 'יותר רווח בין השורות — קל יותר לקרוא')}
      ${sw('rm', '🧘 בלי תנועה', 'מבטל אנימציות והבהובים')}
      ${canSpeak ? '<div class="pf-note">🔊 בכל כרטיס יש כפתור הקראה בקול.</div>' : ''}
    </div>`;
  };
  window.prefBind = function (root, onChange) {
    root.querySelectorAll('[data-pf]').forEach(c => c.onchange = () => { prefSet(c.dataset.pf, c.checked); onChange && onChange(); });
    root.querySelectorAll('[data-fz]').forEach(b => b.onclick = () => {
      let i = 1; try { const v = localStorage.getItem('gemara:fz'); if (v !== null && FZ[+v]) i = +v; } catch (e) {}
      i = Math.max(0, Math.min(FZ.length - 1, i + +b.dataset.fz)); try { localStorage.setItem('gemara:fz', i); } catch (e) {}
      prefApply(); const o = root.querySelector('.pf-fz output'); if (o) o.textContent = Math.round(FZ[i] * 100) + '%'; onChange && onChange();
    });
  };
})();
