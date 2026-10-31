/* Layout probe injected by tools/responsive_check.py.
   Reports, in document.title:
     viewport x documentWidth | overflowing elements | js errors | hero gap | header overlap */
(function () {
  var errors = [];

  window.addEventListener("error", function (event) {
    errors.push((event.message || "error") + " @" + String(event.filename || "").split("/").pop() + ":" + event.lineno);
  });

  window.addEventListener("unhandledrejection", function (event) {
    errors.push("rejection: " + ((event.reason && event.reason.message) || event.reason));
  });

  function label(el) {
    var name = el.tagName.toLowerCase();
    if (el.id) {
      name += "#" + el.id;
    } else if (el.className && typeof el.className === "string") {
      name += "." + el.className.trim().split(/\s+/).slice(0, 2).join(".");
    }
    return name;
  }

  function inScroller(el) {
    var node = el.parentElement;
    while (node) {
      var style = window.getComputedStyle(node);
      if (style.overflowX === "auto" || style.overflowX === "scroll") return true;
      node = node.parentElement;
    }
    return false;
  }

  function clean(value) {
    return String(value).replace(/["<>|]/g, " ").replace(/\s+/g, " ").trim();
  }

  function report() {
    var vw = window.innerWidth;
    var docW = document.documentElement.scrollWidth;
    var offenders = [];

    Array.prototype.forEach.call(document.querySelectorAll("body *"), function (el) {
      var rect = el.getBoundingClientRect();
      if (!rect.width && !rect.height) return;
      if (rect.right <= vw + 1.5) return;
      if (inScroller(el)) return;
      var text = (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 24);
      var parent = el.parentElement ? label(el.parentElement) : "";
      offenders.push(
        label(el) + " w" + Math.round(rect.width) +
        " over" + Math.round(rect.right - vw) +
        " in<" + parent + "> '" + text + "'"
      );
    });

    var hero = document.querySelector(".hero");
    var next = document.querySelector("#overview");
    var gap = "";
    if (hero && next) {
      gap = Math.round(
        next.getBoundingClientRect().top - hero.getBoundingClientRect().bottom
      );
    }

    var header = document.querySelector(".site-header");
    var overlap = "";
    if (header && hero) {
      overlap = Math.round(
        header.getBoundingClientRect().bottom - hero.getBoundingClientRect().top
      );
    }

    // nothing named but the document is still too wide: bisect the tree,
    // hiding one child at a time and keeping the branch that fixes it
    function bisect(container, depth) {
      var target = document.documentElement.scrollWidth;
      var found = null;
      Array.prototype.forEach.call(container.children, function (child) {
        if (found) return;
        var previous = child.style.display;
        child.style.display = "none";
        var shrunk = document.documentElement.scrollWidth;
        child.style.display = previous;
        if (shrunk <= vw) found = child;
      });
      if (!found) return null;
      if (depth <= 0) return found;
      return bisect(found, depth - 1) || found;
    }

    if (docW > vw && !offenders.length) {
      var culprit = bisect(document.body, 3);
      if (culprit) {
        offenders.push(
          "CULPRIT " + label(culprit) + " '" +
          (culprit.textContent || "").replace(/\s+/g, " ").trim().slice(0, 40) + "'"
        );
      }
    }

    document.title =
      vw + "x" + docW + "|" +
      clean(offenders.slice(0, 6).join(" ~ ")) + "|" +
      clean(errors.slice(0, 4).join(" ; ")) + "|" +
      "gap=" + gap + "|headerOverlap=" + overlap;
  }

  if (document.readyState === "complete") {
    window.setTimeout(report, 600);
  } else {
    window.addEventListener("load", function () {
      window.setTimeout(report, 600);
    });
  }
})();
