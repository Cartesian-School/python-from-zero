// Cartesian School course-experience enhancement: viewport-aware entrance
// choreography and animation suspension. The semantic content and complete
// static composition remain available when JavaScript is disabled.
(function () {
  "use strict";

  var root = document.querySelector(".course-experience");
  if (!root) return;

  var reveals = Array.prototype.slice.call(root.querySelectorAll(".experience-reveal"));
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var revealObserver = null;
  var visibilityObserver = null;

  root.classList.add("is-enhanced");

  function revealAll() {
    reveals.forEach(function (element) {
      element.classList.add("is-revealed");
    });
  }

  function disconnectObservers() {
    if (revealObserver) revealObserver.disconnect();
    if (visibilityObserver) visibilityObserver.disconnect();
    revealObserver = null;
    visibilityObserver = null;
  }

  function startObservers() {
    disconnectObservers();

    if (!("IntersectionObserver" in window)) {
      revealAll();
      root.classList.add("is-in-view");
      return;
    }

    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-revealed");
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    reveals.forEach(function (element) {
      if (!element.classList.contains("is-revealed")) revealObserver.observe(element);
    });

    visibilityObserver = new IntersectionObserver(function (entries) {
      root.classList.toggle("is-in-view", entries[0].isIntersecting);
    }, { rootMargin: "160px 0px", threshold: 0 });
    visibilityObserver.observe(root);
  }

  function syncMotionMode() {
    if (reducedMotion.matches) {
      disconnectObservers();
      revealAll();
      root.classList.add("is-in-view");
    } else {
      startObservers();
    }
  }

  if (typeof reducedMotion.addEventListener === "function") {
    reducedMotion.addEventListener("change", syncMotionMode);
  } else if (typeof reducedMotion.addListener === "function") {
    reducedMotion.addListener(syncMotionMode);
  }

  syncMotionMode();
})();
