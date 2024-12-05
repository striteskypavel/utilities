// Definujeme seznam blokovaných domén
const blockedSites = [
    "*://*.facebook.com/*",
    "*://*.twitter.com/*",
    "*://*.instagram.com/*",
    "*://*.tiktok.com/*",
    "*://*.snapchat.com/*",
    "*://*.linkedin.com/*"
  ];
  
  // Posluchač pro blokování požadavků
  chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
      console.log(`Blocked: ${details.url}`); // Log blokovaných URL pro ladění
      return { redirectUrl: chrome.runtime.getURL("blocked.html") }; // Přesměrování na vlastní blokovací stránku
    },
    { urls: blockedSites },
    ["blocking"]
  );
  