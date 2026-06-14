// Service Worker — SMASH by Bubblesuz
const CACHE = 'smash-v1';
const ASSETS = ['/'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // Ne pas mettre en cache Firebase et Stripe
  if (e.request.url.includes('firebase') || 
      e.request.url.includes('stripe') ||
      e.request.url.includes('googleapis')) {
    return;
  }
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(cache => cache.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});

// Push notifications
self.addEventListener('push', e => {
  const data = e.data ? e.data.json() : {};
  self.registration.showNotification(data.title || '🍔 SMASH by Bubblesuz', {
    body: data.body || 'Nouvelle commande !',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    vibrate: [300, 100, 300],
    tag: 'smash-notification'
  });
});
