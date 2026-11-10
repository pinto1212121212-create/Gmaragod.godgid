// 📲 Service worker: האתר נפתח גם בלי אינטרנט, ונטען מהר.
// קוד ונתונים (html/js/css): קודם מהרשת (תמיד הגרסה החדשה), ואם אין רשת — מהשמור.
// תמונות (צילומי דף, איורים, אייקונים): קודם מהשמור, כי הן כמעט לא משתנות; מתעדכנות ברקע.
// שינוי גדול במבנה? מעלים את VERSION.
const VERSION = 'v2';
const CORE = ['./', 'index.html', 'taanit.html', 'tree.html', 'theme.css', 'prefs.js', 'tree-data.js', 'context-data.js',
  'people-data.js', 'explain-data.js', 'daf-marks.js', 'manifest.webmanifest', 'icons/icon-192.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open('core-' + VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => !k.endsWith(VERSION)).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin || r.cache === 'no-store') return;
  if (/\.(jpe?g|png|webp)$/i.test(u.pathname)) {
    e.respondWith(caches.open('img-' + VERSION).then(async c => {
      const hit = await c.match(r);
      const net = fetch(r).then(res => { if (res.ok) c.put(r, res.clone()); return res; }).catch(() => hit);
      return hit || net;
    }));
    return;
  }
  e.respondWith(fetch(r).then(res => {
    if (res.ok) { const cp = res.clone(); caches.open('core-' + VERSION).then(c => c.put(r, cp)); }
    return res;
  }).catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || caches.match('index.html'))));
});
