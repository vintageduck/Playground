const CACHE_NAME = 'playground-v4';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './manifest.json',
    './polecatting.html',
    './betterloxd.html',
    './rating.html',
    './uni-grades.html',
    './ratking.svg',
    './maccies.html',
    './trim-tag.html',
    './icons/icon-192.png',
    './icons/icon-512.png'
];

// External CDN resources used by trim-tag.html
const CDN_TO_CACHE = [
    'https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jsmediatags/3.9.7/jsmediatags.min.js',
    'https://cdn.jsdelivr.net/npm/browser-id3-writer@6.3.1/dist/browser-id3-writer.mjs'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // Cache local assets first, then try CDN (don't fail install if CDN is down)
            return cache.addAll(ASSETS_TO_CACHE).then(() => {
                return Promise.allSettled(
                    CDN_TO_CACHE.map(url => cache.add(url))
                );
            });
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    // Clean up old caches
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // For navigation requests (HTML pages): network-first, fall back to cache
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    const clone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    return networkResponse;
                })
                .catch(() => caches.match(event.request))
        );
    } else {
        // For everything else (scripts, images, etc.): cache-first
        event.respondWith(
            caches.match(event.request).then((response) => response || fetch(event.request))
        );
    }
});
