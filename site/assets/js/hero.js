// Cartesian School homepage hero: restrained pointer depth and off-screen
// animation suspension. The static composition is complete without JavaScript.
(function () {
  "use strict";

  var hero = document.querySelector(".home-hero");
  var system = hero && hero.querySelector(".hero-system");
  if (!hero || !system) return;

  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var frame = 0;
  var bounds = null;
  var currentX = 0;
  var currentY = 0;
  var targetX = 0;
  var targetY = 0;
  var pointerEnabled = false;

  function writeDepth() {
    currentX += (targetX - currentX) * 0.14;
    currentY += (targetY - currentY) * 0.14;

    system.style.setProperty("--hero-back-x", (currentX * 2).toFixed(2) + "px");
    system.style.setProperty("--hero-back-y", (currentY * 2).toFixed(2) + "px");
    system.style.setProperty("--hero-plane-x", (currentX * 5).toFixed(2) + "px");
    system.style.setProperty("--hero-plane-y", (currentY * 4).toFixed(2) + "px");

    if (Math.abs(targetX - currentX) > 0.004 || Math.abs(targetY - currentY) > 0.004) {
      frame = window.requestAnimationFrame(writeDepth);
    } else {
      frame = 0;
    }
  }

  function requestDepthFrame() {
    if (!frame) frame = window.requestAnimationFrame(writeDepth);
  }

  function onPointerEnter() {
    bounds = hero.getBoundingClientRect();
  }

  function onPointerMove(event) {
    if (!bounds) bounds = hero.getBoundingClientRect();
    targetX = Math.max(-1, Math.min(1, ((event.clientX - bounds.left) / bounds.width - 0.5) * 2));
    targetY = Math.max(-1, Math.min(1, ((event.clientY - bounds.top) / bounds.height - 0.5) * 2));
    requestDepthFrame();
  }

  function onPointerLeave() {
    bounds = null;
    targetX = 0;
    targetY = 0;
    requestDepthFrame();
  }

  function onResize() {
    bounds = null;
  }

  function enablePointerDepth() {
    if (pointerEnabled) return;
    pointerEnabled = true;
    hero.addEventListener("pointerenter", onPointerEnter, { passive: true });
    hero.addEventListener("pointermove", onPointerMove, { passive: true });
    hero.addEventListener("pointerleave", onPointerLeave, { passive: true });
  }

  function disablePointerDepth() {
    if (!pointerEnabled) return;
    pointerEnabled = false;
    hero.removeEventListener("pointerenter", onPointerEnter);
    hero.removeEventListener("pointermove", onPointerMove);
    hero.removeEventListener("pointerleave", onPointerLeave);
    targetX = 0;
    targetY = 0;
    requestDepthFrame();
  }

  function syncMotionMode() {
    if (finePointer.matches && !reducedMotion.matches) enablePointerDepth();
    else disablePointerDepth();
  }

  finePointer.addEventListener("change", syncMotionMode);
  reducedMotion.addEventListener("change", syncMotionMode);
  window.addEventListener("resize", onResize, { passive: true });
  syncMotionMode();

  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      hero.classList.toggle("is-paused", !entries[0].isIntersecting);
    }, { rootMargin: "120px 0px" });
    observer.observe(hero);
  }
})();
