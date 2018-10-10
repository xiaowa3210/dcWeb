// $(function () {
//     var delBtn = $(".del-btn");
//     //console.log("xxxxxxxxxxxxxxx");
//     var trTag = delBtn.parent().parent().parent().parent();  //父亲节点的父亲节点
//     // 获取id属性
//
//     var id = trTag.attr("data-id");
//     delBtn.click(function (event) {
//         event.preventDefault();
//         var current_btn = $(this);
//         // 获取tr标签
//         // console.log("zzzzzzzzzzzz");
//         console.log(id);
//         $.post({
//             'url':'/deluser/',
//             'data':{
//                 "id":id
//             },
//             'success':function (result) {
//                 if(result['code'] === 200){
//                     alert(result['message']);
//                     window.location.reload();  //重新下载
//                 }else {
//                     alert("删除失败")
//                 }
//             },
//             "fail":function (err) {
//                 alert(err);
//             }
//         })
//     })
// });
$(function () {
   $(".del-btn").click(function (event) {
       event.preventDefault();
       var self = $(this);
       var divTag = self.parent().parent();
       var id = divTag.attr('data-id');
       $.post({
           'url':'/back01/delete',
           'data':{
               'id':id
           },
           'success':function (data) {
               if(data['code'] === 200){
                   console.log('Success')
               }else {
                   console.log('Fail')
               }
           },
           'fail':function (error) {
               console.log(error)
           }
       })
   })
});