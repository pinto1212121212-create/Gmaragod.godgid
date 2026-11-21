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
  // 🔇 ההקראה בקול הוסרה מהאתר לבקשת המשתמש (כל כפתורי 🔊 תלויים ב־canSpeak). להחזרה: 'speechSynthesis' in window
  window.canSpeak = false;
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

// 🙏 תפילה קודם הלימוד ולאחר הלימוד (ברכות כח:) — חלון משותף לכל הדפים: openTefila('pre'|'post')
(function () {
  const PRE = `<p><b class="tf-big">יְהִי רָצוֹן</b> מִלְּפָנֶיךָ, יְהוָה אֱלֹהַי, שֶׁלֹּא יֶאֱרַע דְּבַר תַּקָּלָה עַל יָדִי, וְלֹא אֶכָּשֵׁל בִּדְבַר הֲלָכָה וְיִשְׂמְחוּ בִּי חֲבֵרַי, וְלֹא אֹמַר עַל טָמֵא: ״טָהוֹר״, וְלֹא עַל טָהוֹר: ״טָמֵא״, וְלֹא יִכָּשְׁלוּ חֲבֵרַי בִּדְבַר הֲלָכָה וְאֶשְׂמַח בָּהֶם.</p>
    <p><b class="tf-big">כִּי</b> יְהוָה יִתֵּן חָכְמָה מִפִּיו דַּעַת וּתְבוּנָה. גַּל עֵינַי וְאַבִּיטָה נִפְלָאוֹת מִתּוֹרָתֶךָ.</p>`;
  const POST = `<p><b class="tf-big">מוֹדֶה</b> אֲנִי לְפָנֶיךָ, יְהוָה אֱלֹהַי, שֶׁשַּׂמְתָּ חֶלְקִי מִיּוֹשְׁבֵי בֵּית הַמִּדְרָשׁ וְלֹא שַׂמְתָּ חֶלְקִי מִיּוֹשְׁבֵי קְרָנוֹת; שֶׁאֲנִי מַשְׁכִּים וְהֵם מַשְׁכִּימִים: אֲנִי מַשְׁכִּים לְדִבְרֵי תוֹרָה וְהֵם מַשְׁכִּימִים לִדְבָרִים בְּטֵלִים; אֲנִי עָמֵל וְהֵם עֲמֵלִים: אֲנִי עָמֵל וּמְקַבֵּל שָׂכָר וְהֵם עֲמֵלִים וְאֵינָם מְקַבְּלִים שָׂכָר; אֲנִי רָץ וְהֵם רָצִים: אֲנִי רָץ לְחַיֵּי הָעוֹלָם הַבָּא וְהֵם רָצִים לִבְאֵר שַׁחַת. [שֶׁנֶּאֱמַר: וְאַתָּה אֱלֹהִים תּוֹרִדֵם לִבְאֵר שַׁחַת, אַנְשֵׁי דָמִים וּמִרְמָה לֹא יֶחֱצוּ יְמֵיהֶם, וַאֲנִי אֶבְטַח בָּךְ.]</p>`;
  const CSS = `.tf-ov{position:fixed;inset:0;z-index:200;background:rgba(5,5,5,.88);display:flex;align-items:center;justify-content:center;padding:16px}
  .tf-box{width:min(560px,100%);max-height:calc(100dvh - 32px);overflow:auto;background:#121212;border:1px solid rgba(200,168,90,.45);border-radius:28px;padding:20px 20px 16px;color:#f5f1e8;direction:rtl}
  .tf-top{display:flex;align-items:center;gap:8px;margin-bottom:12px}
  .tf-tabs{display:flex;gap:6px;flex:1}
  .tf-tabs button,.tf-x{font:inherit;font-size:15px;border-radius:999px;border:1px solid rgba(200,168,90,.45);background:transparent;color:#dcc078;padding:8px 14px;min-height:40px;cursor:pointer}
  .tf-tabs button.on{background:#c8a85a;color:#0a0a0a;font-weight:700}
  .tf-x{min-width:40px;padding:8px 0}
  .tf-h{font-family:'Frank Ruhl Libre',serif;font-size:21px;font-weight:700;color:#dcc078;text-align:center;margin:6px 0 12px;padding-bottom:8px;border-bottom:1px solid rgba(200,168,90,.3)}
  .tf-txt p{font-family:'Frank Ruhl Libre',serif;font-size:calc(22px * var(--fz,1));line-height:1.85;margin:0 0 12px;text-align:justify}
  .tf-big{font-size:1.25em;color:#dcc078}
  .tf-src{font-size:13px;color:#a09a8c;border-top:1px solid rgba(245,241,232,.12);padding-top:8px;margin-top:4px}`;
  window.openTefila = function (which) {
    let ov = document.getElementById('tfOv');
    if (!ov) {
      const st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
      ov = document.createElement('div'); ov.id = 'tfOv'; ov.className = 'tf-ov'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'תפילה ללימוד');
      ov.addEventListener('click', e => { if (e.target === ov || e.target.closest('.tf-x')) ov.remove(); const t = e.target.closest('[data-tf]'); if (t) openTefila(t.dataset.tf); });
      document.addEventListener('keydown', e => { if (e.key === 'Escape' && document.getElementById('tfOv')) document.getElementById('tfOv').remove(); });
      document.body.appendChild(ov);
    }
    const pre = which !== 'post';
    ov.innerHTML = `<div class="tf-box"><div class="tf-top"><div class="tf-tabs"><button type="button" data-tf="pre" class="${pre ? 'on' : ''}">לפני הלימוד</button><button type="button" data-tf="post" class="${pre ? '' : 'on'}">אחרי הלימוד</button></div><button type="button" class="tf-x" aria-label="סגור">✕</button></div>
      <div class="tf-h">${pre ? 'תפלה קודם הלימוד' : 'תפלה לאחר הלימוד'}</div><div class="tf-txt">${pre ? PRE : POST}</div>
      <div class="tf-src">${pre ? 'ברכות כח: · משלי ב, ו · תהלים קיט, יח' : 'ברכות כח: · תהלים נה, כד'}</div></div>`;
  };
})();
