const CACHE_NAME = 'playground-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './manifest.json',
    './polecatting.html',
    './betterloxd.html',
    './rating.html',
    './ratking.svg',
    './icons/icon-192.png',
    './icons/icon-512.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => response || fetch(event.request))
    );
});


