const setMarkdown = (id) => {
  const markdown = editormd(id, {
    syncScrolling: "single",
    saveHTMLToTextarea: true,
    height: 600,
    // width:960,
    path: "/static/vendor/mdeditor/lib/",
    //启动本地图片上传功能
    imageUpload: true,
    imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
    imageUploadURL: "/markdown/upload/"
  });
  return markdown
}