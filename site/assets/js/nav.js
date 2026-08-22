// Cartesian School — shared mobile navigation toggle + chapter sidebar
// active-lesson visibility. Used on every generated page (chapters, front
// matter, practice, homepage).

// Chapter sidebar: reveal the active lesson without moving anything else.
//
// The sidebar is a sticky, internally-scrolling pane (theory.css .sidebar),
// and on every full-page navigation a fresh document starts it at
// scrollTop 0 — there is no browser memory of where a reader had scrolled
// it before clicking a link. On short chapters that's invisible: the active
// item is near the top anyway. On long chapters (30+ lessons) it means the
// active item can load below the fold, so readers scroll the pane by hand
// to find it, then lose that position again on the very next click — which
// reads as the whole menu "jumping" between lessons.
//
// Fix: adjust ONLY sidebar.scrollTop, and only by the minimum distance
// needed to bring the active link inside the pane — never scroll the page,
// never center the item, and do nothing at all when it's already visible
// (the common case, including every short chapter).
function revealActiveLesson() {
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

  if (itemRect.top < paneRect.top) {
    sidebar.scrollTop -= paneRect.top - itemRect.top;
  } else if (itemRect.bottom > paneRect.bottom) {
    sidebar.scrollTop += itemRect.bottom - paneRect.bottom;
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
    panel.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    revealActiveLesson(); // panel was display:none until now — clientHeight is 0 no longer
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

revealActiveLesson();
// Web fonts (Sora/Inter, loaded async) can swap in after this script runs
// and shift line heights slightly — re-run once they've settled so the
// active item isn't left a few pixels short of fully visible.
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(revealActiveLesson);
}
