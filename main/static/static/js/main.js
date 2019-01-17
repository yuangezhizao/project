// base.html 页面底部 js 全部移至本 main.js 文件

$('.ui.dropdown').dropdown();

$('.message .close').on('click', function () {
    $(this).closest('.message').transition('fade');
});

moment.locale("zh-CN");

_t = function (s) {
    return s
};

function gEle(a) {
    return document.getElementById(a)
}

function _(e, t, i) {
    var a = null;
    if ("text" === e) return document.createTextNode(t);
    a = document.createElement(e);
    for (var n in t) if ("style" === n) for (var o in t.style) a.style[o] = t.style[o]; else if ("className" === n) a.className = t[n]; else if ("event" === n) for (var o in t.event) a.addEventListener(o, t.event[o]); else a.setAttribute(n, t[n]);
    if (i) if ("string" == typeof i) a.innerHTML = i; else if (Array.isArray(i)) for (var l = 0; l < i.length; l++) null != i[l] && a.appendChild(i[l]);
    return a
}

pageConfig = {"lang": "zh"};

auth = {
    logout: function () {
        var msg = confirm("确认注销吗？");
        console.log(msg);
        if (msg) {
            createUpdateNotice(_t("正在注销……"), "00F");
        } else {
            return false;
        }
    },
}