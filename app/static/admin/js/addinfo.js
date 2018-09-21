$(function () {
    var ue = UE.getEditor('editor');
            //{"serverUrl":'/ueditor/upload/'});
    window.ue = ue;
});
$(function () {
    var submitBtn = $("#submit");
    submitBtn.click(function (event) {
        event.preventDefault();
        // 获取input标签内容
        var title = $("input[name='title']").val();
        // 获取富文本内容
        var content = ue.getContent();
        $.post({
            'url':'/upload_news',
            'data':{
                "content":content,
                "title":title,
            },
            'success':function (data) {
                // console.log(data);
                if(data['code'] == 200){
                    window.location = '/tmp01/news';
                }
            },
            'fail':function (error) {
                console.log(error)
            }
        })
    })
});