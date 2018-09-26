$(function () {
    var delBtn = $(".del-btn");

    delBtn.click(function (event) {
        event.preventDefault();
        var current_btn = $(this);
        // 获取tr标签
        var trTag = current_btn.parent().parent();  //父亲节点的父亲节点
        // 获取id属性
        var id = trTag.attr("data-id");
        $.post({
            'url':'/delete_news',
            'data':{
                "id":id
            },
            'success':function (result) {
                if(result['code'] === 200){
                    alert(result['message']);
                    window.location.reload();  //重新下载
                }else {
                    alert("删除失败")
                }
            },
            "fail":function (err) {
                alert(err);
            }
        })
    })
});