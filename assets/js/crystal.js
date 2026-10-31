/* Silica — hero crystal.
   A hand-written WebGL scene: no library, no model download, no external
   request. One icosahedron drawn three ways (back facets, front facets, edges)
   plus a smaller inner solid, lit with a single studio key light and a fresnel
   rim so the silhouette reads on a dark background.

   Behaviour, per the brief:
     * responsive canvas at device-pixel-ratio, capped at 2;
     * rendering stops when the canvas leaves the viewport or the tab is hidden;
     * prefers-reduced-motion renders one still frame and never animates;
     * no WebGL2/WebGL at all -> the static SVG stays visible, nothing breaks;
     * the canvas is sized by CSS aspect-ratio, so it cannot shift layout. */
(function () {
  "use strict";

  var stage = document.querySelector("[data-stage]");
  if (!stage) return;

  var canvas = stage.querySelector("canvas");
  if (!canvas) return;

  var gl =
    canvas.getContext("webgl", { antialias: true, alpha: true, premultipliedAlpha: false }) ||
    canvas.getContext("experimental-webgl", { antialias: true, alpha: true });

  if (!gl) {
    stage.classList.add("no-webgl");
    return;
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- geometry -------------------------------------------------- */
  function icosahedron() {
    var t = (1 + Math.sqrt(5)) / 2;
    var raw = [
      [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
      [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
      [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]
    ];
    var faces = [
      [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
      [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
      [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
      [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ];

    var verts = raw.map(function (v) {
      var len = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
      return [v[0] / len, v[1] / len, v[2] / len];
    });

    var positions = [];
    var normals = [];
    faces.forEach(function (f) {
      var a = verts[f[0]], b = verts[f[1]], c = verts[f[2]];
      var u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
      var v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
      var n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      var nl = Math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]) || 1;
      n = [n[0] / nl, n[1] / nl, n[2] / nl];
      [a, b, c].forEach(function (p) {
        positions.push(p[0], p[1], p[2]);
        normals.push(n[0], n[1], n[2]);
      });
    });

    var seen = {};
    var edges = [];
    faces.forEach(function (f) {
      for (var i = 0; i < 3; i++) {
        var p = f[i], q = f[(i + 1) % 3];
        var key = p < q ? p + "-" + q : q + "-" + p;
        if (seen[key]) continue;
        seen[key] = true;
        edges.push(verts[p][0], verts[p][1], verts[p][2]);
        edges.push(verts[q][0], verts[q][1], verts[q][2]);
      }
    });

    return {
      positions: new Float32Array(positions),
      normals: new Float32Array(normals),
      edges: new Float32Array(edges)
    };
  }

  var geo = icosahedron();

  /* ---------- shaders --------------------------------------------------- */
  var FACE_VS = [
    "attribute vec3 aPos;",
    "attribute vec3 aNormal;",
    "uniform mat4 uProj;",
    "uniform mat4 uModel;",
    "uniform mat3 uNormalMat;",
    "varying vec3 vNormal;",
    "varying vec3 vView;",
    "void main() {",
    "  vec4 world = uModel * vec4(aPos, 1.0);",
    "  vNormal = normalize(uNormalMat * aNormal);",
    "  vView = normalize(-world.xyz);",
    "  gl_Position = uProj * world;",
    "}"
  ].join("\n");

  var FACE_FS = [
    "precision mediump float;",
    "varying vec3 vNormal;",
    "varying vec3 vView;",
    "uniform vec3 uBase;",
    "uniform vec3 uRim;",
    "uniform float uAlpha;",
    "void main() {",
    "  vec3 n = normalize(vNormal);",
    "  vec3 v = normalize(vView);",
    "  vec3 key = normalize(vec3(-0.45, 0.75, 0.65));",
    "  vec3 fill = normalize(vec3(0.7, -0.35, 0.45));",
    "  float d = max(dot(n, key), 0.0);",
    "  float f = max(dot(n, fill), 0.0);",
    "  float fres = pow(1.0 - max(dot(n, v), 0.0), 2.6);",
    "  float spec = pow(max(dot(reflect(-key, n), v), 0.0), 28.0);",
    "  vec3 col = uBase * (0.28 + 0.72 * d) + uRim * f * 0.22;",
    "  col += uRim * fres * 1.05;",
    "  col += vec3(1.0) * spec * 0.35;",
    "  gl_FragColor = vec4(col, uAlpha + fres * 0.42);",
    "}"
  ].join("\n");

  var LINE_VS = [
    "attribute vec3 aPos;",
    "uniform mat4 uProj;",
    "uniform mat4 uModel;",
    "void main() {",
    "  gl_Position = uProj * uModel * vec4(aPos, 1.0);",
    "}"
  ].join("\n");

  var LINE_FS = [
    "precision mediump float;",
    "uniform vec4 uColor;",
    "void main() { gl_FragColor = uColor; }"
  ].join("\n");

  function compile(type, source) {
    var shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(shader) || "shader compile failed");
    }
    return shader;
  }

  function program(vs, fs) {
    var p = gl.createProgram();
    gl.attachShader(p, compile(gl.VERTEX_SHADER, vs));
    gl.attachShader(p, compile(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      throw new Error(gl.getProgramInfoLog(p) || "program link failed");
    }
    return p;
  }

  var faceProgram, lineProgram;
  try {
    faceProgram = program(FACE_VS, FACE_FS);
    lineProgram = program(LINE_VS, LINE_FS);
  } catch (err) {
    stage.classList.add("no-webgl");
    return;
  }

  function buffer(data) {
    var b = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
    return b;
  }

  var posBuffer = buffer(geo.positions);
  var normalBuffer = buffer(geo.normals);
  var edgeBuffer = buffer(geo.edges);

  var faceLoc = {
    aPos: gl.getAttribLocation(faceProgram, "aPos"),
    aNormal: gl.getAttribLocation(faceProgram, "aNormal"),
    uProj: gl.getUniformLocation(faceProgram, "uProj"),
    uModel: gl.getUniformLocation(faceProgram, "uModel"),
    uNormalMat: gl.getUniformLocation(faceProgram, "uNormalMat"),
    uBase: gl.getUniformLocation(faceProgram, "uBase"),
    uRim: gl.getUniformLocation(faceProgram, "uRim"),
    uAlpha: gl.getUniformLocation(faceProgram, "uAlpha")
  };

  var lineLoc = {
    aPos: gl.getAttribLocation(lineProgram, "aPos"),
    uProj: gl.getUniformLocation(lineProgram, "uProj"),
    uModel: gl.getUniformLocation(lineProgram, "uModel"),
    uColor: gl.getUniformLocation(lineProgram, "uColor")
  };

  /* ---------- matrices -------------------------------------------------- */
  function perspective(fov, aspect, near, far) {
    var f = 1 / Math.tan(fov / 2);
    var nf = 1 / (near - far);
    return new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) * nf, -1,
      0, 0, 2 * far * near * nf, 0
    ]);
  }

  function identity() {
    return new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
  }

  function rotateY(out, rad) {
    var c = Math.cos(rad), s = Math.sin(rad);
    out[0] = c; out[2] = -s;
    out[8] = s; out[10] = c;
    return out;
  }

  function rotateX(out, rad) {
    var c = Math.cos(rad), s = Math.sin(rad);
    out[5] = c; out[6] = s;
    out[9] = -s; out[10] = c;
    return out;
  }

  function multiply(a, b) {
    var out = new Float32Array(16);
    for (var i = 0; i < 4; i++) {
      for (var j = 0; j < 4; j++) {
        var sum = 0;
        for (var k = 0; k < 4; k++) sum += a[k * 4 + j] * b[i * 4 + k];
        out[i * 4 + j] = sum;
      }
    }
    return out;
  }

  function normalMatrix(m) {
    return new Float32Array([m[0], m[1], m[2], m[4], m[5], m[6], m[8], m[9], m[10]]);
  }

  function translation(z) {
    var m = identity();
    m[14] = z;
    return m;
  }

  /* ---------- palette --------------------------------------------------- */
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue("--accent").trim() || "#8b9bff";
  var violet = style.getPropertyValue("--violet").trim() || "#b79cff";

  function hexToRgb(hex) {
    var h = hex.replace("#", "");
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    return [
      parseInt(h.slice(0, 2), 16) / 255,
      parseInt(h.slice(2, 4), 16) / 255,
      parseInt(h.slice(4, 6), 16) / 255
    ];
  }

  var accentRgb = hexToRgb(accent);
  var violetRgb = hexToRgb(violet);

  /* ---------- sizing ---------------------------------------------------- */
  var dpr = 1;

  function resize() {
    var rect = stage.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.round(rect.width * dpr);
    var h = Math.round(rect.height * dpr);
    if (canvas.width === w && canvas.height === h) return;
    canvas.width = w;
    canvas.height = h;
    gl.viewport(0, 0, w, h);
    draw();
  }

  /* ---------- interaction ----------------------------------------------- */
  var pointer = { x: 0, y: 0 };
  var target = { x: 0, y: 0 };

  function onPointer(event) {
    var rect = stage.getBoundingClientRect();
    var px = (event.clientX - rect.left) / rect.width - 0.5;
    var py = (event.clientY - rect.top) / rect.height - 0.5;
    target.x = Math.max(-0.5, Math.min(0.5, px)) * 0.55;
    target.y = Math.max(-0.5, Math.min(0.5, py)) * 0.4;
  }

  /* ---------- draw ------------------------------------------------------ */
  var angle = 0.55;
  var tilt = -0.22;

  function draw() {
    var aspect = canvas.width / canvas.height || 1;
    var proj = perspective(0.72, aspect, 0.1, 20);

    pointer.x += (target.x - pointer.x) * 0.06;
    pointer.y += (target.y - pointer.y) * 0.06;

    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    var base = multiply(
      multiply(translation(-2.72), rotateX(identity(), tilt + pointer.y)),
      rotateY(identity(), angle + pointer.x)
    );

    gl.useProgram(faceProgram);
    gl.uniformMatrix4fv(faceLoc.uProj, false, proj);

    gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
    gl.enableVertexAttribArray(faceLoc.aPos);
    gl.vertexAttribPointer(faceLoc.aPos, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
    gl.enableVertexAttribArray(faceLoc.aNormal);
    gl.vertexAttribPointer(faceLoc.aNormal, 3, gl.FLOAT, false, 0, 0);

    /* back facets, then front facets: the classic two-pass glass look */
    gl.depthMask(false);

    gl.enable(gl.CULL_FACE);
    gl.cullFace(gl.FRONT);
    gl.uniformMatrix4fv(faceLoc.uModel, false, base);
    gl.uniformMatrix3fv(faceLoc.uNormalMat, false, normalMatrix(base));
    gl.uniform3fv(faceLoc.uBase, new Float32Array(violetRgb));
    gl.uniform3fv(faceLoc.uRim, new Float32Array(accentRgb));
    gl.uniform1f(faceLoc.uAlpha, 0.2);
    gl.drawArrays(gl.TRIANGLES, 0, geo.positions.length / 3);

    gl.cullFace(gl.BACK);
    gl.uniform1f(faceLoc.uAlpha, 0.27);
    gl.drawArrays(gl.TRIANGLES, 0, geo.positions.length / 3);
    gl.disable(gl.CULL_FACE);

    /* inner solid, slightly smaller and warmer */
    var inner = multiply(
      multiply(translation(-2.72), rotateX(identity(), tilt + pointer.y)),
      rotateY(identity(), angle * -0.7 + pointer.x)
    );
    var scaleInner = identity();
    scaleInner[0] = 0.52; scaleInner[5] = 0.52; scaleInner[10] = 0.52;
    inner = multiply(inner, scaleInner);

    gl.uniformMatrix4fv(faceLoc.uModel, false, inner);
    gl.uniformMatrix3fv(faceLoc.uNormalMat, false, normalMatrix(inner));
    gl.uniform3fv(faceLoc.uBase, new Float32Array(accentRgb));
    gl.uniform3fv(faceLoc.uRim, new Float32Array(violetRgb));
    gl.uniform1f(faceLoc.uAlpha, 0.72);
    gl.drawArrays(gl.TRIANGLES, 0, geo.positions.length / 3);

    /* edges */
    gl.useProgram(lineProgram);
    gl.uniformMatrix4fv(lineLoc.uProj, false, proj);
    gl.uniformMatrix4fv(lineLoc.uModel, false, base);
    gl.bindBuffer(gl.ARRAY_BUFFER, edgeBuffer);
    gl.enableVertexAttribArray(lineLoc.aPos);
    gl.vertexAttribPointer(lineLoc.aPos, 3, gl.FLOAT, false, 0, 0);
    gl.uniform4f(
      lineLoc.uColor,
      accentRgb[0] * 1.15,
      accentRgb[1] * 1.15,
      accentRgb[2] * 1.15,
      0.5
    );
    gl.drawArrays(gl.LINES, 0, geo.edges.length / 3);

    gl.depthMask(true);
  }

  /* ---------- loop ------------------------------------------------------ */
  var running = false;
  var frame = 0;
  var visible = true;
  var last = 0;

  function tick(now) {
    if (!running) return;
    var dt = last ? Math.min((now - last) / 1000, 0.05) : 0.016;
    last = now;
    angle += dt * 0.26;
    draw();
    frame = requestAnimationFrame(tick);
  }

  function start() {
    if (running || reduceMotion.matches) return;
    running = true;
    last = 0;
    frame = requestAnimationFrame(tick);
  }

  function stop() {
    running = false;
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
  }

  function sync() {
    if (visible && !document.hidden && !reduceMotion.matches) start();
    else stop();
  }

  /* ---------- boot ------------------------------------------------------ */
  resize();
  draw();
  stage.classList.add("is-live");

  if ("ResizeObserver" in window) {
    new ResizeObserver(function () {
      resize();
      if (!running) draw();
    }).observe(stage);
  } else {
    window.addEventListener("resize", function () {
      resize();
      if (!running) draw();
    });
  }

  if (!reduceMotion.matches) {
    stage.addEventListener("pointermove", onPointer, { passive: true });
    stage.addEventListener("pointerleave", function () {
      target.x = 0;
      target.y = 0;
    });
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(
      function (entries) {
        visible = entries[0].isIntersecting;
        sync();
      },
      { threshold: 0.01 }
    ).observe(stage);
  }

  document.addEventListener("visibilitychange", sync);

  if (reduceMotion.addEventListener) {
    reduceMotion.addEventListener("change", function () {
      if (reduceMotion.matches) {
        stop();
        angle = 0.6;
        draw();
      } else {
        sync();
      }
    });
  }

  /* the palette or theme changed: repaint from the new tokens */
  function readPalette() {
    var computed = getComputedStyle(document.documentElement);
    accent = computed.getPropertyValue("--accent").trim() || accent;
    violet = computed.getPropertyValue("--violet").trim() || violet;
    accentRgb = hexToRgb(accent);
    violetRgb = hexToRgb(violet);
    draw();
  }

  document.addEventListener("silica:palette", function () {
    window.setTimeout(readPalette, 20);
  });

  sync();
})();
