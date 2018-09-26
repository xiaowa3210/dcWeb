
$(function () {
    var ue = UE.getEditor('editor');
    var origin_content = $("#data-content").attr("data-content");
    console.log("xxxxx")
    ue.ready(function () {      //为什么要ready？
        ue.setContent(origin_content);
    });
    window.ue = ue;
});
