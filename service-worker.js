const CACHE_NAME = 'playground-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './manifest.json',
    // Add your widget paths here as you build them
    // './template-widget/index.html' 
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


