// Cartesian School — shared mobile navigation toggle + chapter sidebar
// active-lesson positioning. Used on every generated page (chapters, front
// matter, practice, homepage).

// Chapter sidebar: keep the active lesson in a comfortable reading context
// without moving anything else.
//
// The sidebar is a sticky, internally-scrolling pane (theory.css .sidebar),
// and on every full-page navigation a fresh document starts it at
// scrollTop 0 — there is no browser memory of where a reader had scrolled
// it before clicking a link. A first version of this fix only nudged the
// pane the minimum distance needed to make the active link technically
// visible, which meant it usually landed pinned right at the bottom edge
// of the pane on long chapters: the current lesson was visible, but every
// lesson after it — and the whole practice section — was scrolled out of
// view, so the chapter's continuation disappeared exactly when a reader
// most wants to see it.
//
// Fix: position the active link at a fixed FRACTION of the pane's height
// (SIDEBAR_TARGET_FRACTION) rather than at whichever edge is nearest, so a
// reader in the middle of a long chapter sees several finished lessons
// above and several upcoming ones (plus, near the end, the start of
// Practice) below. A comfort zone (SIDEBAR_COMFORT_UPPER..LOWER) avoids
// re-adjusting on every navigation when the item is already reasonably
// placed, and clamping keeps the pane from ever showing empty space above
// the first item or below the last.
var SIDEBAR_TARGET_FRACTION = 0.35; // where the active item lands when repositioned
var SIDEBAR_COMFORT_UPPER = 0.25; // above this fraction of pane height: too close to the top edge
var SIDEBAR_COMFORT_LOWER = 0.55; // below this fraction of pane height: too close to the bottom edge

function positionActiveLesson() {
  var sidebar = document.querySelector(".sidebar");
  if (!sidebar || sidebar.clientHeight === 0) return; // hidden (mobile drawer, closed)

  // On the mobile drawer, .mobile-nav-links (the site-wide nav row) sits
  // above the chapter TOC and must stay visible the moment the drawer
  // opens — that row is the whole point of the drawer. Auto-scrolling the
  // pane to favor the active lesson would push it out of the pane's own
  // internal scroll area (theory.css caps the open drawer's height so it
  // stays under the header, which is what makes it scrollable at all).
  // On desktop that row is display:none (0 height), so this never affects
  // the always-visible reading-companion sidebar this function targets.
  var mobileNavLinks = sidebar.querySelector(".mobile-nav-links");
  if (mobileNavLinks && mobileNavLinks.clientHeight > 0) return;

  // .sidebar also carries the mobile drawer's site-wide links (this file's
  // toggle target below), which mark their own "Главы" entry .active — that
  // is not the current lesson and must be ignored here.
  var active = null;
  var candidates = sidebar.querySelectorAll(".toc-list a.active");
  for (var i = 0; i < candidates.length; i++) {
    if (!candidates[i].closest(".mobile-nav-links")) {
      active = candidates[i];
      break;
    }
  }
  if (!active) return;

  var paneRect = sidebar.getBoundingClientRect();
  var itemRect = active.getBoundingClientRect();
  var itemCenter = (itemRect.top + itemRect.bottom) / 2 - paneRect.top; // px from pane top

  var upperBound = sidebar.clientHeight * SIDEBAR_COMFORT_UPPER;
  var lowerBound = sidebar.clientHeight * SIDEBAR_COMFORT_LOWER;
  if (itemCenter >= upperBound && itemCenter <= lowerBound) {
    return; // already in a comfortable context zone — leave the pane alone
  }

  var desiredCenter = sidebar.clientHeight * SIDEBAR_TARGET_FRACTION;
  var target = sidebar.scrollTop + (itemCenter - desiredCenter);

  var maxScrollTop = Math.max(0, sidebar.scrollHeight - sidebar.clientHeight);
  target = Math.max(0, Math.min(target, maxScrollTop));

  sidebar.scrollTop = target; // no smooth-scroll: this runs at page-load time, not as a user gesture
}

// Keeps the mobile drawer's --mobile-nav-top CSS variable in sync with the
// header actually rendered on the page (.site-header on most pages,
// .practice-header on the interactive practice tool), so the drawer's top
// edge lines up with the header's bottom edge exactly — never a hardcoded
// px value, since header height varies with viewport width and content
// (and .practice-header, unlike .site-header, isn't sticky, so its
// boundingClientRect changes as the page scrolls past it too).
function updateMobileNavTop() {
  var header = document.querySelector(".site-header, .practice-header");
  if (!header) return;
  var bottom = header.getBoundingClientRect().bottom;
  document.documentElement.style.setProperty("--mobile-nav-top", bottom + "px");
}

updateMobileNavTop();
window.addEventListener("resize", updateMobileNavTop);
window.addEventListener("orientationchange", updateMobileNavTop);
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(updateMobileNavTop);
}

// Keeps --site-header-height in sync with .site-header's real rendered
// height, so theory.css's html{scroll-padding-top} reserves exactly enough
// room for the sticky header when the browser scrolls a fragment (#praktika
// etc.) into view — no more (which left the previous section's tail
// visible above the target) and no less (which would tuck the target under
// the header). Only .site-header is measured here: .practice-header (the
// interactive practice tool) isn't sticky, so there's no sticky obstruction
// for scroll-padding to compensate for on those pages.
//
// ResizeObserver, not a resize/orientationchange/fonts.ready trio like
// updateMobileNavTop above: it fires on every actual cause of a header
// height change in one place (viewport crossing the mobile/desktop
// breakpoint, zoom, a web font swapping in and nudging line height) rather
// than guessing which events to listen for, and needs no polling.
var siteHeaderForHeight = document.querySelector(".site-header");
if (siteHeaderForHeight) {
  var syncHeaderHeight = function () {
    // getBoundingClientRect().height, not the ResizeObserver entry's own
    // contentRect: contentRect is the content box only (padding and border
    // excluded), which undershoots — .site-header's real rendered (border-
    // box) height is what scroll-padding-top must reserve room for.
    document.documentElement.style.setProperty("--site-header-height", siteHeaderForHeight.getBoundingClientRect().height + "px");
  };
  if (window.ResizeObserver) {
    new ResizeObserver(syncHeaderHeight).observe(siteHeaderForHeight);
  } else {
    // ResizeObserver unsupported: fall back to the same measurement, run
    // on the events most likely to change the header's height.
    syncHeaderHeight();
    window.addEventListener("resize", syncHeaderHeight);
    window.addEventListener("orientationchange", syncHeaderHeight);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncHeaderHeight);
    }
  }
}

// Drives whichever element the .nav-toggle button's aria-controls points at.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var panel = toggle && document.getElementById(toggle.getAttribute("aria-controls"));
  if (!toggle || !panel) return;

  function isOpen() {
    return panel.classList.contains("open");
  }

  function openMenu() {
    updateMobileNavTop(); // re-measure right before showing: cheap, and guards against any drift
    panel.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    positionActiveLesson(); // panel was display:none until now — clientHeight is 0 no longer
  }

  function closeMenu() {
    panel.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }

  toggle.addEventListener("click", function () {
    if (isOpen()) closeMenu();
    else openMenu();
  });

  panel.addEventListener("click", function (event) {
    if (event.target.closest("a")) closeMenu();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && isOpen()) {
      closeMenu();
      toggle.focus();
    }
  });

  // Tapping anywhere outside the open drawer (and outside the toggle
  // itself, which already has its own open/close handler above) closes it.
  document.addEventListener("click", function (event) {
    if (!isOpen()) return;
    if (event.target.closest("#mobile-nav-panel") || event.target.closest(".nav-toggle")) return;
    closeMenu();
  });

  // The drawer is a mobile-only affordance (theory.css's max-width: 860px
  // breakpoint). If it's left open while resizing past that breakpoint —
  // e.g. rotating a tablet, or a desktop window growing — close it so no
  // stale .open / aria-expanded="true" survives the transition, and so it
  // starts closed if the viewport later shrinks back into mobile range.
  var desktopQuery = window.matchMedia("(min-width: 861px)");
  function closeIfNowDesktop(event) {
    if (event.matches && isOpen()) closeMenu();
  }
  if (desktopQuery.addEventListener) {
    desktopQuery.addEventListener("change", closeIfNowDesktop);
  } else if (desktopQuery.addListener) {
    desktopQuery.addListener(closeIfNowDesktop); // Safari < 14
  }
})();

// Runs once at page-load time only — never on a scroll/resize listener, so
// a reader who scrolls the pane by hand afterward keeps full control of it.
positionActiveLesson();
// Web fonts (Sora/Inter, loaded async) can swap in after this script runs
// and shift line heights slightly — re-run once they've settled so the
// target position is measured against final layout, not a fallback font.
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(positionActiveLesson);
}
