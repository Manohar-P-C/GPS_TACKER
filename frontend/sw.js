
const CACHE_NAME = "gps-tracker-shell-v1";

const APP_FILES = [
    "/",
    "/manifest.webmanifest",
    "/icons/icon-192.png",
    "/icons/icon-512.png"
];

// Install service worker and cache essential app files
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(APP_FILES))
            .then(() => self.skipWaiting())
    );
});

// Activate and clean old caches
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys
                    .filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            )
        ).then(() => self.clients.claim())
    );
});

// Handle network requests
self.addEventListener("fetch", event => {
    const request = event.request;
    const url = new URL(request.url);

    if (request.method !== "GET") return;
    if (url.origin !== self.location.origin) return;

    // Always fetch fresh GPS coordinates
    if (url.pathname === "/location") {
        event.respondWith(
            fetch(request, { cache: "no-store" })
        );
        return;
    }

    // Network first for dashboard page
    if (request.mode === "navigate") {
        event.respondWith(
            fetch(request)
                .then(response => {
                    if (response.ok) {
                        const copy = response.clone();

                        caches.open(CACHE_NAME)
                            .then(cache => cache.put("/", copy));
                    }

                    return response;
                })
                .catch(() => caches.match("/"))
        );

        return;
    }

    // Cache essential application files
    if (APP_FILES.includes(url.pathname)) {
        event.respondWith(
            caches.match(request).then(cached => {
                return cached || fetch(request);
            })
        );
    }
});
