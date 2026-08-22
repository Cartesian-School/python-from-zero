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

// Drives whichever element the .nav-toggle button's aria-controls points at.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var panel = toggle && document.getElementById(toggle.getAttribute("aria-controls"));
  if (!toggle || !panel) return;

  function isOpen() {
    return panel.classList.contains("open");
  }

  function openMenu() {
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
