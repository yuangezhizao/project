"use strict";
(function() {
    function t(t) {
        return t.preventDefault(),
        t.stopPropagation(),
        !1
    }
    function e(e) {
        var n = this
          , o = null
          , r = function(t) {
            "td" == this.nodeName.toLowerCase() && t.target != this || (null != o && o.abort(),
            a.zoomObj.destroy(),
            s.remove(),
            document.body.style.overflow = "")
        }
          , s = document.body.appendChild(_("div", {
            className: "container",
            style: {
                opacity: 1,
                overflowX: "hidden",
                overflowY: "auto",
                left: 0,
                top: 0
            }
        }, [_("table", {
            className: "white_container",
            style: {
                display: "table",
                textAlign: "center",
                position: "initial",
                background: "rgba(0,0,0,.7)"
            },
            event: {
                touchmove: t
            }
        }, [_("tbody", {}, [_("tr", {}, [_("td", {
            event: {
                click: r
            }
        }, [_("span", {}, [_("img", {
            src: this.src,
            style: {
                maxWidth: "100%",
                verticalAlign: "bottom"
            },
            event: {
                click: function() {
                    window.open(this.hasAttribute("original-src") ? this.getAttribute("original-src") : this.src)
                }
            }
        })])])])])]), _("div", {
            style: {
                position: "fixed",
                top: "25px",
                right: "25px",
                zIndex: 1,
                background: "rgba(255,255,255,.3)",
                borderRadius: "10px"
            },
            event: {
                click: r
            }
        })]));
        s.children[1].innerHTML = '<svg width="30" height="30" style="display:block;fill:#000;stroke:#000"><path d="M8,6L24,22L22,24L6,8" /><path d="M22,6L6,22L8,24L24,8" /></svg>';
        var a = s.querySelector("img");
        if (a.zoomObj = new i(a),
        n.hasAttribute("original-src")) {
            var c = s.appendChild(_("div", {
                className: "img-progress",
                style: {
                    width: "5px"
                }
            }))
              , u = n.getAttribute("original-src");
            setTimeout(function() {
                if (/https:\/\/(i\d\.hdslb\.com|[\w\.]+\.biliplus\.com)\//.test(u)) {
                    var t = new XMLHttpRequest;
                    o = t,
                    t.open("GET", u, !0),
                    t.onprogress = function(t) {
                        c.style.width = t.loaded / t.total * 100 + "%"
                    }
                    ,
                    t.onload = function() {
                        o = null,
                        u = URL.createObjectURL(t.response),
                        a.src = u,
                        a.setAttribute("original-src", n.getAttribute("original-src")),
                        c.style.width = "100%",
                        c.style.opacity = 0
                    }
                    ,
                    t.responseType = "blob",
                    t.send()
                } else
                    a.src = n.getAttribute("original-src")
            }, 100),
            a.addEventListener("load", function() {
                this.currentSrc == u && (c.style.width = "100%",
                c.style.opacity = 0,
                this.sizeChanged = !0,
                this.zoomObj.reset(),
                "blob:" == u.substr(0, 5) && URL.revokeObjectURL(u))
            })
        }
        document.body.style.overflow = "hidden",
        e.stopPropagation()
    }
    function n(t, e) {
        this.A = t,
        this.b = e
    }
    function i(t, e, i) {
        this.mayBeDoubleTap = null,
        this.isAnimationRunning = !1,
        this.runningRequest = null,
        this.curTouch = 0,
        this.elem = t,
        this.activeZoom = T,
        this.resultantZoom = T,
        this.srcCoords = [0, 0],
        this.destCoords = [0, 0];
        var o = this;
        this.config = k(e, {
            pan: !1,
            rotate: !0
        }),
        this.wnd = i || window,
        t.style["transform-origin"] = "center";
        var r, s, a, c = function(e) {
            var n = t.offsetLeft + P[0] / 2
              , i = t.offsetTop + P[1] / 2;
            return [[e[0].clientX - n, e[0].clientY - i], [e[1].clientX - n, e[1].clientY - i]]
        }, u = function(e) {
            var n = t.offsetLeft
              , i = t.offsetTop
              , o = e[0].clientX - n
              , r = e[0].clientY - i;
            return [[o, r], [o + 1, r + 1]]
        }, p = function(t) {
            return t.length > 1 ? c(t) : u(t)
        }, g = function(t) {
            o.srcCoords = p(t),
            o.destCoords = o.srcCoords
        }, v = function(t) {
            o.destCoords = p(t)
        }, w = function(t) {
            return function(e) {
                e.preventDefault(),
                o.isAnimationRunning && (o.runningRequest && cancelAnimationFrame(o.runningRequest),
                o.runningRequest = null,
                o.isAnimationRunning = !1);
                var n = e.touches;
                return !!n && void t(n)
            }
        }, y = !1, b = !0, A = !0, E = !1, x = w(function(t) {
            var e = t.length;
            if (e != o.curTouch)
                o.curTouch = e,
                o.finalize(),
                0 != e && g(t);
            else if (t.length) {
                if (v(t),
                y && (A && (o.destCoords[0][0] = o.srcCoords[0][0],
                o.destCoords[1][0] = o.srcCoords[1][0]),
                b && (o.destCoords[0][1] = o.srcCoords[0][1],
                o.destCoords[1][1] = o.srcCoords[1][1])),
                z) {
                    var n = m(L(o.srcCoords, o.destCoords, !0).A[0]);
                    n < Math.PI / 12 || n > 23 * Math.PI / 12 ? o.config.rotate = !1 : (z = !1,
                    o.config.rotate = !0)
                }
                o.previewZoom()
            }
            1 == t.length && (r = [t[0].clientX, t[0].clientY])
        }), C = function() {
            var t = Date.now();
            if (t != s.time) {
                var e = f(r, s.vec);
                s.speed = l(200 / (t - s.time), e),
                s.vec = r,
                s.time = t
            }
        }, P = null, R = null, Z = null, z = !0, W = w(function(e) {
            if (y = 1 == e.length,
            null == P || t.sizeChanged) {
                P = [t.offsetWidth, t.offsetHeight],
                A = P[0] < innerWidth,
                b = P[1] < innerHeight;
                var n = t.getBoundingClientRect();
                R = [n.left, n.top],
                t.sizeChanged = !1
            }
            if (a || (a = setInterval(C, 50),
            r = [e[0].clientX, e[0].clientY],
            s = {
                speed: [0, 0],
                vec: r,
                time: Date.now()
            }),
            null == Z) {
                var i = o.resultantZoom.A[0][0]
                  , c = o.resultantZoom.A[0][1];
                Z = (i ? i > 0 ? 0 : 2 : c > 0 ? 1 : 3) * Math.PI / 2,
                z = !0
            }
            1 === e.length && (null != o.mayBeDoubleTap ? E = !0 : o.mayBeDoubleTap = o.wnd.setTimeout(function() {
                o.mayBeDoubleTap = null
            }, 300))
        }), N = w(function(t) {
            if (y = !1,
            1 === t.length && (r = [t[0].clientX, t[0].clientY],
            s.vec = r),
            0 === t.length) {
                clearInterval(a),
                a = null,
                Z = null;
                var e = h(o.activeZoom.A[0])
                  , i = m(o.activeZoom.A[0])
                  , c = i / Math.PI * 2
                  , u = (m(P),
                [R[0] + P[0] / 2, R[1] + P[1] / 2])
                  , l = !1;
                c % 1 != 0 && (l = !0),
                c = Math.round(c) % 4;
                var f = [1, 0, -1, 0]
                  , p = [0, 1, 0, -1]
                  , g = d(o.activeZoom.b, s.speed);
                e < 1 && (e = 1),
                A = !1,
                b = !1,
                c % 2 ? (P[1] * e < window.innerWidth ? (g[0] = innerWidth / 2 - u[0],
                A = !0) : 2 * Math.abs(g[0] + innerWidth / 2 - u[0]) + innerWidth > P[1] * e && (g[0] = (P[1] * e - innerWidth) / (g[0] > 0 ? 2 : -2) + innerWidth / 2 - u[0]),
                P[0] * e < window.innerHeight ? (g[1] = innerHeight / 2 - u[1],
                b = !0) : g[1] > P[0] * e / 2 - u[1] ? g[1] = P[0] * e / 2 - u[1] : g[1] < innerHeight - u[1] - P[0] * e / 2 && (g[1] = innerHeight - u[1] - P[0] * e / 2)) : (P[0] * e < window.innerWidth ? (g[0] = innerWidth / 2 - u[0],
                A = !0) : 2 * Math.abs(g[0]) + innerWidth > P[0] * e && (g[0] = (P[0] * e - innerWidth) / (g[0] > 0 ? 2 : -2)),
                P[1] * e < window.innerHeight ? (g[1] = innerHeight / 2 - u[1],
                b = !0) : g[1] > P[1] * e / 2 - u[1] ? g[1] = P[1] * e / 2 - u[1] : g[1] < innerHeight - u[1] - P[1] * e / 2 && (g[1] = innerHeight - u[1] - P[1] * e / 2)),
                g[0] == o.activeZoom.b[0] && g[1] == o.activeZoom.b[1] || (l = !0),
                l ? o.reset(new n([[e * f[c], e * p[c]], [-e * p[c], e * f[c]]],g)) : E && (o.reset(),
                E = !1)
            }
        });
        t.parentNode.addEventListener("touchstart", W),
        t.parentNode.addEventListener("touchstart", x),
        t.parentNode.addEventListener("touchmove", x),
        t.parentNode.addEventListener("touchend", x),
        t.parentNode.addEventListener("touchend", N);
        var X = !1
          , _ = !0;
        t.addEventListener("touchstart", function(t) {
            return t.touches.length > 1 ? void (_ = !1) : void (X = !1)
        }),
        t.addEventListener("touchmove", function(t) {
            t.touches.length > 1 || (X = !0)
        }),
        t.addEventListener("touchend", function(e) {
            e.touches.length > 0 || (X && (clearTimeout(o.mayBeDoubleTap),
            o.mayBeDoubleTap = null),
            !X && _ && 1 == h(o.activeZoom.A[0]) && window.open(t.hasAttribute("original-src") ? t.getAttribute("original-src") : t.src),
            _ = !0)
        });
        var B = function() {
            t.sizeChanged = !0,
            o.setZoom(T)
        };
        window.addEventListener("resize", B),
        this.destroy = function() {
            window.removeEventListener("resize", B)
        }
    }
    var o = [].slice;
    Array.from = function(t) {
        return o.call(t)
    }
    ,
    !window.requestAnimationFrame && (window.requestAnimationFrame = webkitRequestAnimationFrame || mozRequestAnimation || function(t) {
        return setTimeout(t, 1e3 / 60)
    }
    ),
    window.gEle = function(t) {
        return document.getElementById(t)
    }
    ,
    window.blankImg = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==";
    var r = []
      , s = function(t) {
        t.parentNode && (t.style.transition = "top .5s",
        t.style.top = "-100px",
        setTimeout(function() {
            a(t)
        }, 510))
    }
      , a = function(t) {
        var e = r.indexOf(t);
        return e !== -1 && (r.splice(e, 1),
        void t.remove())
    };
    window.createUpdateNotice = function(t, e, n, i) {
        e = "#" + e;
        var o = _("div", {
            class: "Biliplus-Notice",
            style: {
                background: e
            },
            event: {
                click: function() {
                    a(this)
                }
            }
        });
        "string" == typeof t && (o.innerHTML = t),
        document.body.appendChild(o);
        var c = r.length ? r[r.length - 1].nextTop : 50
          , u = o.offsetHeight;
        o.style.top = c + "px",
        o.nextTop = c + u + 20,
        o.appendChild(_("div", {
            className: "after",
            style: {
                borderWidth: "calc(" + u + "px / 2) 5px",
                borderRightColor: e,
                borderBottomColor: e
            }
        })),
        r.push(o),
        n !== !0 ? setTimeout(function() {
            s(o)
        }, 5e3) : "function" == typeof i && (o.addEventListener("click", i),
        o.style.cursor = "pointer")
    }
    ,
    window.removeUpdateNotice = function() {
        r.forEach(function(t) {
            s(t)
        })
    }
    ,
    window.getjson = function(t, e, n) {
        var i = new XMLHttpRequest;
        return i.onreadystatechange = function() {
            4 == i.readyState && (200 == i.status ? e(JSON.parse(i.response), n) : e({
                code: -502,
                message: "网络错误"
            }, n))
        }
        ,
        i.open("GET", t, !0),
        i.withCredentials = !0,
        i.send(),
        i
    }
    ,
    window.postjson = function(t, e, n, i, o) {
        var r = new XMLHttpRequest;
        return r.onreadystatechange = function() {
            4 == i.readyState && (200 == i.status ? e(JSON.parse(i.response), n) : e({
                code: -502,
                message: "网络错误"
            }, i))
        }
        ,
        r.open("POST", t, !0),
        r.withCredentials = !0,
        "string" == typeof n && r.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"),
        !o && r.send(n),
        r
    };
    var Z = timeago();
    Z.setLocale({
        en: "en",
        zh: "zh_CN"
    }[pageConfig.lang]),
    window.timeagoRun = function() {
        var t = Array.from(document.getElementsByClassName("timeago"));
        t.forEach(function(t) {
            t.hasAttribute("datetime") && (t.textContent = Z.format(t.getAttribute("datetime")))
        })
    },
    setInterval(timeagoRun, 6e4),
    timeagoRun();
}
)();
