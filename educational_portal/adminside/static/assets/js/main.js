"use strict";
let isRtl = window.Helpers.isRtl(),
    isDarkStyle = window.Helpers.isDarkStyle(),
    menu,
    animate,
    isHorizontalLayout = !1;
document.getElementById("layout-menu") && (isHorizontalLayout = document.getElementById("layout-menu").classList.contains("menu-horizontal")),
    (function () {
        setTimeout(function () {
            window.Helpers.initCustomOptionCheck();
        }, 1e3),
            document.querySelectorAll("#layout-menu").forEach(function (e) {
                (menu = new Menu(e, {
                    orientation: isHorizontalLayout ? "horizontal" : "vertical",
                    closeChildren: !!isHorizontalLayout,
                    showDropdownOnHover: localStorage.getItem("templateCustomizer-" + templateName + "--ShowDropdownOnHover")
                        ? "true" === localStorage.getItem("templateCustomizer-" + templateName + "--ShowDropdownOnHover")
                        : void 0 === window.templateCustomizer || window.templateCustomizer.settings.defaultShowDropdownOnHover,
                })),
                    window.Helpers.scrollToActive((animate = !1)),
                    (window.Helpers.mainMenu = menu);
            }),
            document.querySelectorAll(".layout-menu-toggle").forEach((e) => {
                e.addEventListener("click", (e) => {
                    if ((e.preventDefault(), window.Helpers.toggleCollapsed(), config.enableMenuLocalStorage && !window.Helpers.isSmallScreen()))
                        try {
                            localStorage.setItem("templateCustomizer-" + templateName + "--LayoutCollapsed", String(window.Helpers.isCollapsed()));
                            var t,
                                o = document.querySelector(".template-customizer-layouts-options");
                            o && ((t = window.Helpers.isCollapsed() ? "collapsed" : "expanded"), o.querySelector(`input[value="${t}"]`).click());
                        } catch (e) {}
                });
            }),
            window.Helpers.swipeIn(".drag-target", function (e) {
                window.Helpers.setCollapsed(!1);
            }),
            window.Helpers.swipeOut("#layout-menu", function (e) {
                window.Helpers.isSmallScreen() && window.Helpers.setCollapsed(!0);
            });
        let e = document.getElementsByClassName("menu-inner"),
            t = document.getElementsByClassName("menu-inner-shadow")[0];
        0 < e.length &&
            t &&
            e[0].addEventListener("ps-scroll-y", function () {
                this.querySelector(".ps__thumb-y").offsetTop ? (t.style.display = "block") : (t.style.display = "none");
            }),
            (window.onscroll = function () {
                document.getElementById("layout-navbar") &&
                    (10 < document.body.scrollTop || 10 < document.documentElement.scrollTop
                        ? document.getElementById("layout-navbar").classList.add("navbar-elevated")
                        : document.getElementById("layout-navbar").classList.remove("navbar-elevated"));
            });
        var o,
            a = document.querySelector(".dropdown-style-switcher"),
            n = localStorage.getItem("templateCustomizer-" + templateName + "--Style") || (window.templateCustomizer?.settings?.defaultStyle ?? "light"),
            a =
                (window.templateCustomizer &&
                    a &&
                    ([].slice.call(a.children[1].querySelectorAll(".dropdown-item")).forEach(function (e) {
                        e.addEventListener("click", function () {
                            var e = this.getAttribute("data-theme");
                            "light" === e ? window.templateCustomizer.setStyle("light") : "dark" === e ? window.templateCustomizer.setStyle("dark") : window.templateCustomizer.setStyle("system");
                        });
                    }),
                    (a = a.querySelector("i")),
                    "light" === n
                        ? (a.classList.add("bx-sun"), new bootstrap.Tooltip(a, { title: "Light Mode", fallbackPlacements: ["bottom"] }))
                        : "dark" === n
                        ? (a.classList.add("bx-moon"), new bootstrap.Tooltip(a, { title: "Dark Mode", fallbackPlacements: ["bottom"] }))
                        : (a.classList.add("bx-desktop"), new bootstrap.Tooltip(a, { title: "System Mode", fallbackPlacements: ["bottom"] }))),
                "system" === (o = n) && (o = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"),
                [].slice.call(document.querySelectorAll("[data-app-" + o + "-img]")).map(function (e) {
                    var t = e.getAttribute("data-app-" + o + "-img");
                    e.src = assetsPath + "img/" + t;
                }),
                "undefined" != typeof i18next &&
                    "undefined" != typeof i18NextHttpBackend &&
                    i18next
                        .use(i18NextHttpBackend)
                        .init({ lng: window.templateCustomizer ? window.templateCustomizer.settings.lang : "en", debug: !1, fallbackLng: "en", backend: { loadPath: assetsPath + "json/locales/{{lng}}.json" }, returnObjects: !0 })
                        .then(function (e) {
                            l();
                        }),
                document.getElementsByClassName("dropdown-language"));
        if (a.length) {
            var s = a[0].querySelectorAll(".dropdown-item");
            for (let e = 0; e < s.length; e++)
                s[e].addEventListener("click", function () {
                    let o = this.getAttribute("data-language"),
                        a = this.getAttribute("data-text-direction");
                    for (var e of this.parentNode.children)
                        for (var t = e.parentElement.parentNode.firstChild; t; ) 1 === t.nodeType && t !== t.parentElement && t.querySelector(".dropdown-item").classList.remove("active"), (t = t.nextSibling);
                    this.classList.add("active"),
                        i18next.changeLanguage(o, (e, t) => {
                            if (
                                (window.templateCustomizer && window.templateCustomizer.setLang(o),
                                "rtl" === a
                                    ? "true" !== localStorage.getItem("templateCustomizer-" + templateName + "--Rtl") && window.templateCustomizer && window.templateCustomizer.setRtl(!0)
                                    : "true" === localStorage.getItem("templateCustomizer-" + templateName + "--Rtl") && window.templateCustomizer && window.templateCustomizer.setRtl(!1),
                                e)
                            )
                                return console.log("something went wrong loading", e);
                            l();
                        });
                });
        }
        function l() {
            var e = document.querySelectorAll("[data-i18n]"),
                t = document.querySelector('.dropdown-item[data-language="' + i18next.language + '"]');
            t && t.click(),
                e.forEach(function (e) {
                    e.innerHTML = i18next.t(e.dataset.i18n);
                });
        }
        n = document.querySelector(".dropdown-notifications-all");
        function i(e) {
            "show.bs.collapse" == e.type || "show.bs.collapse" == e.type ? e.target.closest(".accordion-item").classList.add("active") : e.target.closest(".accordion-item").classList.remove("active");
        }
        const r = document.querySelectorAll(".dropdown-notifications-read");
        n &&
            n.addEventListener("click", (e) => {
                r.forEach((e) => {
                    e.closest(".dropdown-notifications-item").classList.add("marked-as-read");
                });
            }),
            r &&
                r.forEach((t) => {
                    t.addEventListener("click", (e) => {
                        t.closest(".dropdown-notifications-item").classList.toggle("marked-as-read");
                    });
                }),
            document.querySelectorAll(".dropdown-notifications-archive").forEach((t) => {
                t.addEventListener("click", (e) => {
                    t.closest(".dropdown-notifications-item").remove();
                });
            }),
            [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).map(function (e) {
                return new bootstrap.Tooltip(e);
            });
        [].slice.call(document.querySelectorAll(".accordion")).map(function (e) {
            e.addEventListener("show.bs.collapse", i), e.addEventListener("hide.bs.collapse", i);
        });
        window.Helpers.setAutoUpdate(!0), window.Helpers.initPasswordToggle(), window.Helpers.initSpeechToText(), window.Helpers.initNavbarDropdownScrollbar();
        let d = document.querySelector("[data-template^='horizontal-menu']");
        if (
            (d && (window.innerWidth < window.Helpers.LAYOUT_BREAKPOINT ? window.Helpers.setNavbarFixed("fixed") : window.Helpers.setNavbarFixed("")),
            window.addEventListener(
                "resize",
                function (e) {
                    window.innerWidth >= window.Helpers.LAYOUT_BREAKPOINT &&
                        document.querySelector(".search-input-wrapper") &&
                        (document.querySelector(".search-input-wrapper").classList.add("d-none"), (document.querySelector(".search-input").value = "")),
                        d &&
                            (window.innerWidth < window.Helpers.LAYOUT_BREAKPOINT ? window.Helpers.setNavbarFixed("fixed") : window.Helpers.setNavbarFixed(""),
                            setTimeout(function () {
                                window.innerWidth < window.Helpers.LAYOUT_BREAKPOINT
                                    ? document.getElementById("layout-menu") && document.getElementById("layout-menu").classList.contains("menu-horizontal") && menu.switchMenu("vertical")
                                    : document.getElementById("layout-menu") && document.getElementById("layout-menu").classList.contains("menu-vertical") && menu.switchMenu("horizontal");
                            }, 100));
                }
            ),
            window.addEventListener(
                "resize",
                function (e) {
                    var t = document.querySelector(".dropdown-notifications-all");
                    t &&
                        (setTimeout(function () {
                            new bootstrap.Tooltip(t, { title: "Mark all as read", fallbackPlacements: ["bottom"] });
                        }, 300),
                        new bootstrap.Tooltip(document.querySelector(".dropdown-notifications-read"), { title: "Mark as read", fallbackPlacements: ["bottom"] }));
                },
                { once: !0 }
            ),
            window.templateCustomizer)
        ) {
            if (window.templateCustomizer.settings.defaultRtl) {
                var c = document.createElement("link");
                (c.rel = "stylesheet"), (c.href = assetsPath + "vendor/libs/bootstrap-datepicker-bs5/bootstrap-datepicker.rtl.css"), document.head.appendChild(c);
            }
            if (window.templateCustomizer.settings.defaultMenuCollapse)
                try {
                    localStorage.setItem("templateCustomizer-" + templateName + "--LayoutCollapsed", "true"), window.Helpers.setCollapsed(!0, !1);
                } catch (e) {}
        }
    })();
