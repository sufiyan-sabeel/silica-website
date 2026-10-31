/* Silica website — progressive enhancement only.
   Every page works without JavaScript; this adds theme switching, the mobile
   menu, copy-to-clipboard, the code tabs and a subtle scroll reveal. */
(function () {
  "use strict";

  var root = document.documentElement;
  var STORE = "silica-theme";

  /* ---------- theme ---------------------------------------------------- */
  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "light" ? "#fbfbfc" : "#0b0d10");
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      var label = theme === "light" ? "Switch to dark theme" : "Switch to light theme";
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
      btn.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
    });
  }

  function currentTheme() {
    var saved = null;
    try {
      saved = localStorage.getItem(STORE);
    } catch (err) {
      saved = null;
    }
    if (saved === "light" || saved === "dark") return saved;
    /* Silica's own design is the dark theme; the switch is there for readers
       who prefer light, but it is not imposed by the operating system. */
    return "dark";
  }

  applyTheme(currentTheme());

  document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-theme-toggle]");
    if (!btn) return;
    var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    applyTheme(next);
    try {
      localStorage.setItem(STORE, next);
    } catch (err) {
      /* private mode: the choice simply does not persist */
    }
  });

  /* ---------- mobile navigation ---------------------------------------- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("site-nav");
  var backdrop = document.querySelector("[data-nav-backdrop]");

  function closeNav() {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    document.body.classList.remove("nav-open");
    if (backdrop) backdrop.hidden = true;
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.body.classList.toggle("nav-open", open);
      if (backdrop) backdrop.hidden = !open;
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeNav();
    });

    if (backdrop) {
      backdrop.addEventListener("click", closeNav);
    }

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeNav();
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 800) closeNav();
    });
  }

  /* ---------- sticky header shadow ------------------------------------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- copy to clipboard ---------------------------------------- */
  document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-copy]");
    if (!btn) return;
    var target = document.getElementById(btn.getAttribute("data-copy"));
    if (!target) return;
    var text = target.innerText;

    function done() {
      var original = btn.getAttribute("data-label") || btn.textContent.trim();
      btn.setAttribute("data-label", original);
      btn.textContent = "Copied";
      window.setTimeout(function () {
        btn.textContent = original;
      }, 1600);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }

    function fallback() {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy");
        done();
      } catch (err) {
        /* nothing sensible to do; the code is still selectable by hand */
      }
      document.body.removeChild(area);
    }
  });

  /* ---------- code tabs ------------------------------------------------- */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var tabs = Array.prototype.slice.call(group.querySelectorAll('[role="tab"]'));
    if (!tabs.length) return;

    function select(index) {
      tabs.forEach(function (tab, i) {
        var selected = i === index;
        tab.setAttribute("aria-selected", selected ? "true" : "false");
        tab.setAttribute("tabindex", selected ? "0" : "-1");
        var panel = document.getElementById(tab.getAttribute("aria-controls"));
        if (panel) panel.hidden = !selected;
      });
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () {
        select(i);
      });
      tab.addEventListener("keydown", function (event) {
        var next = null;
        if (event.key === "ArrowRight") next = (i + 1) % tabs.length;
        if (event.key === "ArrowLeft") next = (i - 1 + tabs.length) % tabs.length;
        if (event.key === "Home") next = 0;
        if (event.key === "End") next = tabs.length - 1;
        if (next === null) return;
        event.preventDefault();
        select(next);
        tabs[next].focus();
      });
    });
  });

  /* ---------- collapsible documentation menu ---------------------------- */
  var docsMenu = document.querySelector("[data-docs-menu]");
  if (docsMenu) {
    var docsToggle = docsMenu.querySelector("[data-docs-toggle]");
    var narrow = window.matchMedia("(max-width: 1080px)");

    function syncDocsMenu() {
      docsMenu.setAttribute("data-ready", "");
      if (narrow.matches) {
        docsMenu.classList.add("is-collapsed");
        docsToggle.setAttribute("aria-expanded", "false");
      } else {
        docsMenu.classList.remove("is-collapsed", "is-open");
        docsToggle.setAttribute("aria-expanded", "true");
      }
    }

    syncDocsMenu();
    if (narrow.addEventListener) {
      narrow.addEventListener("change", syncDocsMenu);
    } else if (narrow.addListener) {
      narrow.addListener(syncDocsMenu);
    }

    if (docsToggle) {
      docsToggle.addEventListener("click", function () {
        var collapsed = docsMenu.classList.toggle("is-collapsed");
        docsMenu.classList.toggle("is-open", !collapsed);
        docsToggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
      });
    }
  }

  /* ---------- "on this page" highlight ---------------------------------- */
  var tocLinks = Array.prototype.slice.call(
    document.querySelectorAll(".toc a[href^='#']")
  );
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    var headings = [];
    tocLinks.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var heading = document.getElementById(id);
      if (!heading) return;
      byId[id] = link;
      headings.push(heading);
    });

    var setActive = function (id) {
      tocLinks.forEach(function (link) {
        link.classList.toggle("is-active", link === byId[id]);
      });
    };

    var spy = new IntersectionObserver(
      function (entries) {
        var visible = entries
          .filter(function (entry) {
            return entry.isIntersecting;
          })
          .sort(function (a, b) {
            return a.boundingClientRect.top - b.boundingClientRect.top;
          });
        if (visible.length) setActive(visible[0].target.id);
      },
      { rootMargin: "-" + 72 + "px 0px -70% 0px", threshold: 0 }
    );

    headings.forEach(function (heading) {
      spy.observe(heading);
    });
  }

  /* ---------- scroll reveal -------------------------------------------- */
  var revealables = Array.prototype.slice.call(
    document.querySelectorAll(".reveal")
  );
  if (!("IntersectionObserver" in window) || !revealables.length) return;

  /* Only sections that start below the fold are hidden and then revealed, so
     anything already on screen is painted immediately. */
  var pending = revealables.filter(function (el) {
    var top = el.getBoundingClientRect().top;
    if (top < window.innerHeight * 0.9) return false;
    el.classList.add("reveal-pending");
    return true;
  });

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.remove("reveal-pending");
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -6% 0px", threshold: 0.05 }
  );

  pending.forEach(function (el) {
    observer.observe(el);
  });

  /* Safety net: never leave a section invisible if the observer never fires. */
  window.setTimeout(function () {
    pending.forEach(function (el) {
      el.classList.remove("reveal-pending");
      el.classList.add("is-visible");
    });
  }, 2500);
})();
