var Common = {}

//提取图片的src,可能是base64编码，可能是http
Common.getPicsSrc = function ( selector ) {
    return Common.getElementsAttr(selector,"src");
}

//获取某个选择器的某个属性值列表
Common.getElementsAttr = function (selector,attrStr) {
    var e = selector;
    if(e==null) throw "selector不得为null!";
	if(e.constructor == String) e = $(e);
    ret = new Array();
	e.each(function () {
        ret.push($(this).attr(attrStr))
    });
    return ret;
}