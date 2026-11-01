/* Silica website — interaction layer.

   Everything here is progressive enhancement: the pages are readable and
   navigable with this file missing. Order matters — theme first, so the first
   paint is already correct. */
(function () {
  "use strict";

  var root = document.documentElement;
  var STORE = "silica-theme";
  var ACCENT_STORE = "silica-accent";
  var ACCENTS = ["indigo", "teal", "violet", "amber", "rose"];

  /* ---------- theme ------------------------------------------------------ */
  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute("content", theme === "light" ? "#f7f8fc" : "#0b1020");
    }
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
    /* Silica's identity is the dark theme; the switch is a choice, not a
       default imposed by the operating system. */
    return "dark";
  }

  function syncThemeChoices() {
    var theme = root.getAttribute("data-theme");
    document.querySelectorAll("[data-theme-choice]").forEach(function (btn) {
      btn.setAttribute(
        "aria-pressed",
        btn.getAttribute("data-theme-choice") === theme ? "true" : "false"
      );
    });
  }

  function setTheme(next, persist) {
    applyTheme(next);
    syncThemeChoices();
    if (persist) {
      try {
        localStorage.setItem(STORE, next);
      } catch (err) {
        /* private mode: the choice simply does not persist */
      }
    }
    /* the crystal reads its colours from these tokens */
    document.dispatchEvent(new CustomEvent("silica:palette"));
  }

  function currentAccent() {
    var saved = null;
    try {
      saved = localStorage.getItem(ACCENT_STORE);
    } catch (err) {
      saved = null;
    }
    return ACCENTS.indexOf(saved) > -1 ? saved : "indigo";
  }

  function setAccent(name, persist) {
    if (ACCENTS.indexOf(name) === -1) name = "indigo";
    root.setAttribute("data-accent", name);
    document.querySelectorAll("[data-accent-choice]").forEach(function (btn) {
      btn.setAttribute(
        "aria-pressed",
        btn.getAttribute("data-accent-choice") === name ? "true" : "false"
      );
    });
    if (persist) {
      try {
        localStorage.setItem(ACCENT_STORE, name);
      } catch (err) {
        /* ignore */
      }
    }
    document.dispatchEvent(new CustomEvent("silica:palette"));
  }

  applyTheme(currentTheme());
  syncThemeChoices();
  setAccent(currentAccent(), false);

  document.addEventListener("click", function (event) {
    var toggle = event.target.closest("[data-theme-toggle]");
    if (toggle) {
      setTheme(root.getAttribute("data-theme") === "light" ? "dark" : "light", true);
      return;
    }

    var themeChoice = event.target.closest("[data-theme-choice]");
    if (themeChoice) {
      setTheme(themeChoice.getAttribute("data-theme-choice"), true);
      return;
    }

    var accentChoice = event.target.closest("[data-accent-choice]");
    if (accentChoice) {
      setAccent(accentChoice.getAttribute("data-accent-choice"), true);
      return;
    }
  });

  /* ---------- appearance customiser panel -------------------------------- */
  var customizer = document.querySelector("[data-customizer]");
  if (customizer) {
    var customizerToggle = customizer.querySelector("[data-customizer-toggle]");
    var customizerPanel = customizer.querySelector(".customizer__panel");

    function closeCustomizer() {
      customizerPanel.hidden = true;
      customizerToggle.setAttribute("aria-expanded", "false");
    }

    customizerToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = customizerPanel.hidden;
      customizerPanel.hidden = !open;
      customizerToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", function (event) {
      if (customizerPanel.hidden) return;
      if (customizer.contains(event.target)) return;
      closeCustomizer();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !customizerPanel.hidden) {
        closeCustomizer();
        customizerToggle.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 560) closeCustomizer();
    });
  }

  /* ---------- mobile navigation ----------------------------------------- */
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

    if (backdrop) backdrop.addEventListener("click", closeNav);

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeNav();
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 940) closeNav();
    });
  }

  /* ---------- sticky header --------------------------------------------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 6);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- copy to clipboard ----------------------------------------- */
  document.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-copy]");
    if (!btn) return;
    var target = document.getElementById(btn.getAttribute("data-copy"));
    if (!target) return;
    var text = target.innerText;

    function done() {
      if (!btn.getAttribute("data-label")) {
        btn.setAttribute("data-label", btn.textContent.trim());
      }
      btn.textContent = "Copied";
      window.setTimeout(function () {
        btn.textContent = btn.getAttribute("data-label");
      }, 1600);
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
        /* the code stays selectable by hand */
      }
      document.body.removeChild(area);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
  });

  /* ---------- code tabs -------------------------------------------------- */
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
    if (narrow.addEventListener) narrow.addEventListener("change", syncDocsMenu);
    else if (narrow.addListener) narrow.addListener(syncDocsMenu);

    if (docsToggle) {
      docsToggle.addEventListener("click", function () {
        var collapsed = docsMenu.classList.toggle("is-collapsed");
        docsMenu.classList.toggle("is-open", !collapsed);
        docsToggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
      });
    }
  }

  /* ---------- "on this page" -------------------------------------------- */
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

    var spy = new IntersectionObserver(
      function (entries) {
        var visible = entries
          .filter(function (entry) {
            return entry.isIntersecting;
          })
          .sort(function (a, b) {
            return a.boundingClientRect.top - b.boundingClientRect.top;
          });
        if (!visible.length) return;
        var id = visible[0].target.id;
        tocLinks.forEach(function (link) {
          link.classList.toggle("is-active", link === byId[id]);
        });
      },
      { rootMargin: "-80px 0px -68% 0px", threshold: 0 }
    );

    headings.forEach(function (heading) {
      spy.observe(heading);
    });
  }

  /* ---------- documentation search --------------------------------------- */
  var dialog = document.getElementById("search-dialog");
  var openers = Array.prototype.slice.call(document.querySelectorAll("[data-search-open]"));
  var input = dialog ? dialog.querySelector("input[type='search']") : null;
  var results = dialog ? dialog.querySelector(".search-results") : null;
  var empty = dialog ? dialog.querySelector(".search-empty") : null;
  var closeBtn = dialog ? dialog.querySelector("[data-search-close]") : null;
  var index = null;
  var loading = false;
  var active = -1;
  var items = [];

  function openSearch() {
    if (!dialog) return;
    dialog.classList.add("is-open");
    dialog.removeAttribute("hidden");
    document.body.classList.add("nav-open");
    if (!index && !loading) loadIndex();
    window.setTimeout(function () {
      if (input) input.focus();
    }, 20);
  }

  function closeSearch() {
    if (!dialog) return;
    dialog.classList.remove("is-open");
    dialog.setAttribute("hidden", "");
    document.body.classList.remove("nav-open");
    active = -1;
  }

  function loadIndex() {
    loading = true;
    var url = dialog.getAttribute("data-index");
    fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error("index " + res.status);
        return res.json();
      })
      .then(function (data) {
        index = data;
        loading = false;
        if (input && input.value.trim()) render(input.value);
      })
      .catch(function () {
        loading = false;
        if (empty) {
          empty.textContent = "Search could not load. The documentation index is on the documentation page.";
          empty.hidden = false;
        }
      });
  }

  function score(entry, query) {
    var title = entry.title.toLowerCase();
    var text = entry.text.toLowerCase();
    var page = entry.page.toLowerCase();
    var total = 0;
    if (title === query) total += 120;
    if (title.indexOf(query) === 0) total += 60;
    else if (title.indexOf(query) > -1) total += 34;
    if (page.indexOf(query) > -1) total += 16;
    var at = text.indexOf(query);
    if (at > -1) {
      total += 14;
      if (at < 90) total += 6;
    }
    query.split(/\s+/).forEach(function (word) {
      if (word && text.indexOf(word) > -1) total += 4;
      if (word && title.indexOf(word) > -1) total += 8;
    });
    return total;
  }

  function snippet(text, query) {
    var at = text.toLowerCase().indexOf(query);
    if (at < 0) return text.slice(0, 130) + (text.length > 130 ? "…" : "");
    var start = Math.max(0, at - 48);
    var out = text.slice(start, start + 150);
    return (start > 0 ? "…" : "") + out + (start + 150 < text.length ? "…" : "");
  }

  function render(value) {
    if (!results) return;
    var query = value.trim().toLowerCase();
    results.innerHTML = "";
    items = [];
    active = -1;

    if (!query) {
      if (empty) {
        empty.textContent = "Type to search the documentation.";
        empty.hidden = false;
      }
      return;
    }

    if (!index) {
      if (empty) {
        empty.textContent = "Loading the index…";
        empty.hidden = false;
      }
      return;
    }

    var hits = index
      .map(function (entry) {
        return { entry: entry, score: score(entry, query) };
      })
      .filter(function (hit) {
        return hit.score > 0;
      })
      .sort(function (a, b) {
        return b.score - a.score;
      })
      .slice(0, 12);

    if (!hits.length) {
      if (empty) {
        empty.textContent = "Nothing matched “" + value.trim() + "”.";
        empty.hidden = false;
      }
      return;
    }

    if (empty) empty.hidden = true;

    hits.forEach(function (hit, i) {
      var entry = hit.entry;
      var li = document.createElement("li");
      var link = document.createElement("a");
      link.href = entry.url;
      link.innerHTML =
        '<span class="search-results__page">' + entry.page + "</span>" +
        '<span class="search-results__title">' + entry.title + "</span>" +
        '<span class="search-results__snippet">' +
        snippet(entry.text, query) +
        "</span>";
      li.appendChild(link);
      results.appendChild(li);
      items.push(link);
    });
  }

  function moveActive(step) {
    if (!items.length) return;
    active = (active + step + items.length) % items.length;
    items.forEach(function (item, i) {
      item.classList.toggle("is-active", i === active);
    });
    items[active].scrollIntoView({ block: "nearest" });
  }

  openers.forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      openSearch();
    });
  });

  if (dialog) {
    if (closeBtn) closeBtn.addEventListener("click", closeSearch);
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) closeSearch();
    });
    if (input) {
      input.addEventListener("input", function () {
        render(input.value);
      });
      input.addEventListener("keydown", function (event) {
        if (event.key === "ArrowDown") {
          event.preventDefault();
          moveActive(1);
        } else if (event.key === "ArrowUp") {
          event.preventDefault();
          moveActive(-1);
        } else if (event.key === "Enter") {
          if (active > -1 && items[active]) {
            event.preventDefault();
            window.location.href = items[active].href;
          }
        } else if (event.key === "Escape") {
          closeSearch();
        }
      });
    }
  }

  document.addEventListener("keydown", function (event) {
    var typing = /^(input|textarea|select)$/i.test(
      (event.target.tagName || "").toLowerCase()
    );
    if (typing) return;
    if (event.key === "/" || ((event.metaKey || event.ctrlKey) && event.key === "k")) {
      if (!dialog) return;
      event.preventDefault();
      openSearch();
    }
    if (event.key === "Escape" && dialog && dialog.classList.contains("is-open")) {
      closeSearch();
    }
  });

  /* ---------- live repository status ------------------------------------- */
  var statusRoots = document.querySelectorAll("[data-repo-status]");
  if (statusRoots.length) {
    var api = "https://api.github.com/repos/sufiyan-sabeel/silica";
    var headers = { Accept: "application/vnd.github+json" };

    function set(key, value) {
      if (value === null || value === undefined || value === "") return;
      document.querySelectorAll('[data-repo="' + key + '"]').forEach(function (node) {
        node.textContent = value;
      });
    }

    function setHref(key, url) {
      if (!url) return;
      document.querySelectorAll('[data-repo="' + key + '"]').forEach(function (node) {
        node.setAttribute("href", url);
      });
    }

    function day(value) {
      return value ? String(value).slice(0, 10) : null;
    }

    function stamp(text) {
      document.querySelectorAll("[data-status-time]").forEach(function (node) {
        node.textContent = text;
      });
    }

    function checkedNow() {
      var now = new Date();
      var hh = String(now.getHours()).padStart(2, "0");
      var mm = String(now.getMinutes()).padStart(2, "0");
      stamp("checked " + hh + ":" + mm);
    }

    function getJSON(url) {
      return fetch(url, { headers: headers }).then(function (res) {
        if (!res.ok) throw new Error("status " + res.status);
        return res.json();
      });
    }

    getJSON(api)
      .then(function (repo) {
        set("stars", repo.stargazers_count);
        set("forks", repo.forks_count);
        set("issues", repo.open_issues_count);
        set("updated", day(repo.pushed_at));
        statusRoots.forEach(function (root) {
          root.setAttribute("data-live", "true");
        });
        checkedNow();
        return getJSON(api + "/releases/latest").catch(function () {
          return null;
        });
      })
      .then(function (release) {
        if (release && release.tag_name) {
          set("release", release.tag_name);
          set("release-date", day(release.published_at));
          setHref("release-link", release.html_url);
          document.querySelectorAll("[data-version-label]").forEach(function (node) {
            node.textContent = release.tag_name;
          });
        }
        return getJSON(api + "/commits?per_page=1").catch(function () {
          return null;
        });
      })
      .then(function (commits) {
        var latest = Array.isArray(commits) ? commits[0] : null;
        if (latest) {
          var commit = latest.commit || {};
          set("commit-sha", (latest.sha || "").slice(0, 7));
          set("commit-msg", (commit.message || "").split("\n")[0]);
          set("commit-date", day((commit.committer || {}).date));
          setHref("commit-link", latest.html_url);
        }
      })
      .catch(function () {
        /* rate limited or offline: the values baked at build time stand, and the
           stamp keeps saying when they were captured. */
      });
  }

  /* ---------- scroll reveal ---------------------------------------------- */
  var revealables = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (!("IntersectionObserver" in window) || !revealables.length) return;

  var pending = revealables.filter(function (el) {
    if (el.getBoundingClientRect().top < window.innerHeight * 0.92) return false;
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
    { rootMargin: "0px 0px -6% 0px", threshold: 0.04 }
  );

  pending.forEach(function (el) {
    observer.observe(el);
  });

  window.setTimeout(function () {
    pending.forEach(function (el) {
      el.classList.remove("reveal-pending");
      el.classList.add("is-visible");
    });
  }, 2600);
})();
