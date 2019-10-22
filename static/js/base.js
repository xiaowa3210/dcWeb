$(function() {
  /**
   * 导航栏高亮active
   */
  $('.nav li').find('a').each(function() {
    if (this.href === location.href || location.href.includes(this.href)) {
      $(this).parent().siblings('li').removeClass('active');
      if(!location.href.includes('student')) {
        $(this).parent().addClass('active');
      }
    }
  });

  /**
   * 去掉新闻/项目时间的小时， 只保留年月日
   */
  $(".time").each(function() {
    $(this).text($(this).text().slice(0, 10));
  });
});