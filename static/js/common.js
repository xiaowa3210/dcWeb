const setMarkdown = (id, value) => {
  const markdown = editormd(id, {
    syncScrolling: "single",
    saveHTMLToTextarea: true,
    height: 400,
    // width:960,
    value: value,
    path: "/static/vendor/mdeditor/lib/",
    //启动本地图片上传功能
    imageUpload: true,
    imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
    imageUploadURL: "{{url_for('common.markdown_upload')}}"
  });
  return markdown
}