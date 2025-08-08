const cacheName = 'mail-pwa-v1';
const assets = [
  '/',
  '/static/css/style.css',
  '/static/js/script.js',
  '/static/images/mail_192.png',
  '/static/images/mail_512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(cacheName).then(cache => cache.addAll(assets))
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.url.includes('/') || e.request.url.includes('/static/')) {
    e.respondWith(
      caches.match(e.request).then(res => res || fetch(e.request))
    );
  }
});