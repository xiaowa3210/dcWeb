$(function() {
  /**
   * 导航栏高亮active
   */
  $('.nav li').find('a').each(function() {
    if (this.href === location.href || location.search && location.href.includes(this.href)) {
      $(this).parent().siblings('li').removeClass('active');
      $(this).parent().addClass('active');
    }
  });

  /**
   * 去掉新闻/项目时间的小时， 只保留年月日
   */
  $(".time").each(function() {
    $(this).text($(this).text().slice(0, 10));
  });

  /**
   * markdown设置
   */
  // editormd("markdown", {
  //   syncScrolling: "single",
  //   saveHTMLToTextarea: true,
  //   height: 700,
  //   // width:960,
  //   path: "{{url_for('static',filename='mdeditor/lib/')}}",
  //   //启动本地图片上传功能
  //   imageUpload: true,
  //   imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
  //   imageUploadURL: "{{url_for('common.markdown_upload')}}"
  // });
});