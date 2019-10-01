export const setMarkdown = (id) => {
    const markdown = editormd(id, {
        syncScrolling: "single",
        saveHTMLToTextarea: true,
        height: 700,
        // width:960,
        path: "{{url_for('static',filename='mdeditor/lib/')}}",
        //启动本地图片上传功能
        imageUpload: true,
        imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        imageUploadURL: "{{url_for('common.markdown_upload')}}"
    });
    return markdown
}