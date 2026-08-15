// Cartesian School — homepage behavior: progress aggregation, the Practice
// catalog's Все/В браузере/Локально filter, and active-menu-on-scroll.
//
// Reads the SAME localStorage progress store the practice runner already
// writes to (cartesian.python.progress.v1 — see web/src/practice-app.js and
// site_lib.py's local_required_card()/build_practice_pages.py's completion
// button). This is intentionally the only progress store in the product:
// this script only aggregates it for display, it never writes to it.
//
// DOM contract (all attributes are set at build time by build_site_index.py):
//   [data-lesson-id]                     one practice lesson row/checkmark
//   [data-chapter][data-lesson-ids]      a chapter group or roadmap milestone
//                                        (data-lesson-ids is a comma-separated
//                                        list of the real lesson ids in that
//                                        chapter, possibly empty)
//   #journey-progress[data-total-lessons] the course-wide progress summary
(function () {
  var PROGRESS_KEY = "cartesian.python.progress.v1";

  function readProgress() {
    try {
      return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function isDone(entry) {
    return !!entry && (entry.status === "completed" || entry.status === "completed-local");
  }

  var progress = readProgress();

  function lessonIdsOf(el) {
    var raw = el.getAttribute("data-lesson-ids") || "";
    return raw.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
  }

  // 1. Per-lesson checkmarks in the Practice catalog.
  var doneCount = 0;
  var totalLessons = 0;
  document.querySelectorAll("[data-lesson-id]").forEach(function (row) {
    totalLessons += 1;
    var id = row.getAttribute("data-lesson-id");
    var done = isDone(progress[id]);
    if (done) doneCount += 1;
    var check = row.querySelector(".plr-check");
    if (check) check.classList.toggle("done", done);
  });

  // 2. Chapter groups (Practice catalog <details>) and roadmap milestones —
  //    same aggregation logic, different visual output, driven by the same
  //    data-chapter/data-lesson-ids attributes so there is one source of truth.
  document.querySelectorAll("[data-chapter][data-lesson-ids]").forEach(function (group) {
    var ids = lessonIdsOf(group);
    var total = ids.length;
    var done = ids.filter(function (id) { return isDone(progress[id]); }).length;
    var pct = total > 0 ? Math.round((done / total) * 100) : 0;

    var barFill = group.querySelector(".pcg-bar-fill, .jn-progress-fill");
    if (barFill) barFill.style.width = pct + "%";

    var countEl = group.querySelector(".pcg-count");
    if (countEl && total > 0) countEl.textContent = done + " из " + total + " выполнено";

    if (group.classList.contains("journey-node")) {
      group.classList.remove("state-not-started", "state-in-progress", "state-completed", "state-no-lessons");
      var state;
      if (total === 0) state = "no-lessons";
      else if (done === 0) state = "not-started";
      else if (done === total) state = "completed";
      else state = "in-progress";
      group.classList.add("state-" + state);
      group.dataset.state = state;

      var badge = group.querySelector(".jn-state-badge");
      if (badge) {
        var labels = {
          "no-lessons": "",
          "not-started": "Не начато",
          "in-progress": "В процессе",
          "completed": "Завершено",
        };
        badge.textContent = labels[state] || "";
        badge.style.display = state === "no-lessons" ? "none" : "";
      }
    }
  });

  // 3. "Current chapter" = the first roadmap milestone (by chapter number)
  //    that is not yet completed and does have real lessons to complete —
  //    an honest, purely-derived notion of "what to do next", never a lock.
  var nodes = Array.prototype.slice.call(document.querySelectorAll(".journey-node[data-chapter]"))
    .sort(function (a, b) { return Number(a.dataset.chapter) - Number(b.dataset.chapter); });
  for (var i = 0; i < nodes.length; i++) {
    var st = nodes[i].dataset.state;
    if (st === "not-started" || st === "in-progress") {
      nodes[i].classList.add("state-current");
      var curBadge = nodes[i].querySelector(".jn-state-badge");
      if (curBadge) curBadge.textContent = "Текущая глава";
      break;
    }
  }

  // 4. Course-wide progress summary.
  var summary = document.getElementById("journey-progress");
  if (summary) {
    var total = Number(summary.getAttribute("data-total-lessons")) || 0;
    var done = 0;
    Object.keys(progress).forEach(function (id) {
      if (isDone(progress[id])) done += 1;
    });
    // Only count lessons that are actually part of the current curriculum.
    done = Math.min(done, total);
    var pct = total > 0 ? Math.round((done / total) * 100) : 0;
    var headline = summary.querySelector(".jp-detail");
    if (headline) headline.textContent = done + " из " + total + " практических заданий выполнено";
    var fill = summary.querySelector(".jp-bar-fill");
    if (fill) fill.style.width = pct + "%";
  }

  // 5. Practice catalog filter buttons (Все / В браузере / Локально).
  //    Pure show/hide — no framework, degrades to "show everything" with JS off.
  var filterButtons = document.querySelectorAll(".pf-btn");
  filterButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      filterButtons.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      var mode = btn.getAttribute("data-filter");
      document.querySelectorAll(".practice-chapter-group").forEach(function (group) {
        var anyVisible = false;
        group.querySelectorAll(".practice-lesson-row").forEach(function (row) {
          var match = mode === "all" || row.getAttribute("data-mode") === mode;
          row.style.display = match ? "" : "none";
          if (match) anyVisible = true;
        });
        group.style.display = anyVisible ? "" : "none";
      });
    });
  });

  // 6. Active main-menu state driven by which homepage section is in view —
  //    lightweight IntersectionObserver, no scroll-event polling.
  if ("IntersectionObserver" in window) {
    var navLinks = document.querySelectorAll('.top-nav a[href^="/index.html#"], .mobile-nav-links a[href^="/index.html#"]');
    var sectionIds = Array.prototype.map.call(navLinks, function (a) { return a.getAttribute("href").split("#")[1]; });
    var uniqueIds = sectionIds.filter(function (id, i) { return sectionIds.indexOf(id) === i; });
    var sections = uniqueIds.map(function (id) { return document.getElementById(id); }).filter(Boolean);

    function setActive(id) {
      navLinks.forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("href").split("#")[1] === id);
      });
    }

    var observer = new IntersectionObserver(
      function (entries) {
        var visible = entries.filter(function (e) { return e.isIntersecting; });
        if (visible.length === 0) return;
        visible.sort(function (a, b) { return b.intersectionRatio - a.intersectionRatio; });
        setActive(visible[0].target.id);
      },
      { rootMargin: "-96px 0px -60% 0px", threshold: [0, 0.25, 0.5, 0.75, 1] }
    );
    sections.forEach(function (s) { observer.observe(s); });
  }
})();
