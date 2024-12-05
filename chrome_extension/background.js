chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
      // Dynamické přesměrování na stránku blocked.html uvnitř rozšíření
      return { redirectUrl: chrome.runtime.getURL("blocked.html") };
    },
    {
      urls: [
        "*://*.facebook.com/*",
        "*://*.twitter.com/*",
        "*://*.instagram.com/*",
        "*://*.tiktok.com/*",
        "*://*.snapchat.com/*",
        "*://*.linkedin.com/*"
      ],
      types: ["main_frame"]
    },
    ["blocking"]
  );
  