// 对象，封装了标签相关的功能。
var tag = $("#x1");
var text = tag.text();

window.setTimeout(function () {
    var target = $("#x2")
    target.text(text);
}, 5000);
