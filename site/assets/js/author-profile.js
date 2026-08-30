// Cartesian School author-profile enhancement: a one-shot editorial entrance
// and off-screen suspension for the sparse ambient decoration. The complete
// profile is visible without JavaScript and under reduced-motion preferences.
(function () {
  "use strict";

  var root = document.querySelector(".author-profile");
  if (!root) return;

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var completionTarget = root.querySelector(".author-domain:last-child");
  var observer = null;
  var fallbackTimer = 0;
  var entranceStarted = false;
  var entranceFinished = false;

  root.classList.add("is-enhanced");

  function clearCompletionHooks() {
    if (fallbackTimer) window.clearTimeout(fallbackTimer);
    fallbackTimer = 0;
    if (completionTarget) completionTarget.removeEventListener("animationend", onEntranceComplete);
  }

  function finishEntrance() {
    if (entranceFinished) return;
    entranceFinished = true;
    clearCompletionHooks();
    root.classList.remove("is-profile-entering");
    root.classList.add("is-profile-revealed");
  }

  function onEntranceComplete(event) {
    if (event.target !== completionTarget || event.animationName !== "author-content-enter") return;
    finishEntrance();
  }

  function startEntrance() {
    if (entranceStarted) return;
    entranceStarted = true;

    if (reducedMotion.matches) {
      finishEntrance();
      return;
    }

    if (completionTarget) completionTarget.addEventListener("animationend", onEntranceComplete);
    root.classList.add("is-profile-entering");
    fallbackTimer = window.setTimeout(finishEntrance, 1700);
  }

  function disconnectObserver() {
    if (observer) observer.disconnect();
    observer = null;
  }

  function observeProfile() {
    disconnectObserver();

    if (!("IntersectionObserver" in window)) {
      root.classList.add("is-profile-in-view");
      startEntrance();
      return;
    }

    observer = new IntersectionObserver(function (entries) {
      var entry = entries[0];
      root.classList.toggle("is-profile-in-view", entry.isIntersecting);
      if (entry.isIntersecting) startEntrance();
    }, { rootMargin: "140px 0px", threshold: 0.08 });
    observer.observe(root);
  }

  function syncMotionMode() {
    if (reducedMotion.matches) {
      disconnectObserver();
      root.classList.add("is-profile-in-view");
      startEntrance();
      finishEntrance();
      return;
    }
    observeProfile();
  }

  if (typeof reducedMotion.addEventListener === "function") {
    reducedMotion.addEventListener("change", syncMotionMode);
  } else if (typeof reducedMotion.addListener === "function") {
    reducedMotion.addListener(syncMotionMode);
  }

  syncMotionMode();
})();
