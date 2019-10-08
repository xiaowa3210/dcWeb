(function(window, $) {
  /**
   * 将form表单序列化为json对象
   */
  $.fn.serializeJson = function() {
    let serializeObj = {};
    let array = this.serializeArray();
    $(array).each(
      function() {
        if (serializeObj[this.name]) {
          if ($.isArray(serializeObj[this.name])) {
            serializeObj[this.name].push(this.value);
          } else {
            serializeObj[this.name] = [
              serializeObj[this.name], this.value
            ];
          }
        } else {
          serializeObj[this.name] = this.value;
        }
      });
    return serializeObj;
  };

  /**
   * 下拉框回显数据
   */

  $.fn.echoSelect = function(value) {
    this.val(value)
  }

})(window, jQuery);