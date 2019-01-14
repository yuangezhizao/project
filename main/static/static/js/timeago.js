/* https://www.biliplus.com/js/timeago.min.js */

!function (e, t) {
    "object" == typeof module && module.exports ? (module.exports = t(e), module.exports.default = module.exports) : e.timeago = t(e)
}("undefined" != typeof window ? window : this, function () {
    function e(e) {
        return e instanceof Date ? e : isNaN(e) ? /^\d+$/.test(e) ? new Date(t(e)) : (e = (e || "").trim().replace(/\.\d+/, "").replace(/-/, "/").replace(/-/, "/").replace(/(\d)T(\d)/, "$1 $2").replace(/Z/, " UTC").replace(/([\+\-]\d\d)\:?(\d\d)/, " $1$2"), new Date(e)) : new Date(t(e))
    }

    function t(e) {
        return parseInt(e)
    }

    function n(e, n, r) {
        n = c[n] ? n : c[r] ? r : "en";
        for (var o = 0, a = 0 > e ? 1 : 0, u = e = Math.abs(e); e >= f[o] && s > o; o++) e /= f[o];
        return e = t(e), o *= 2, e > (0 === o ? 9 : 1) && (o += 1), c[n](e, o, u)[a].replace("%s", e)
    }

    function r(t, n) {
        return n = n ? e(n) : new Date, (n - e(t)) / 1e3
    }

    function o(e, t) {
        this.nowDate = e, this.defaultLocale = t || "en"
    }

    function a(e, t) {
        return new o(e, t)
    }

    var u = "second_minute_hour_day_week_month_year".split("_"), i = "秒_分钟_小时_天_周_月_年".split("_"), c = {
        en: function (e, t) {
            if (0 === t) return ["just now", "right now"];
            var n = u[parseInt(t / 2)];
            return e > 1 && (n += "s"), [e + " " + n + " ago", "in " + e + " " + n]
        }, zh_CN: function (e, t) {
            if (0 === t) return ["刚刚", "片刻后"];
            var n = i[parseInt(t / 2)];
            return [e + n + "前", e + n + "后"]
        }
    }, f = [60, 60, 24, 7, 365 / 7 / 12, 12], s = 6;
    return o.prototype.format = function (e, t) {
        return n(r(e, this.nowDate), t, this.defaultLocale)
    }, o.prototype.setLocale = function (e) {
        this.defaultLocale = e
    }, a
});/*end*/
