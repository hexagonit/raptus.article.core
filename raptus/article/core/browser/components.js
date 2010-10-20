jQuery(document).ready(function() {
  jQuery('#components li').each(function() {
    var li = jQuery(this);
    var label = li.find('label');
    var img = li.find('img');
    var span = li.find('span');
    jQuery('<span class="information clearfix"></span>').appendTo(label);
    var info = label.find('.information');
    img.appendTo(info);
    span.appendTo(info);
    li.hover(
      function() {
        jQuery(this).addClass('hover');
      },
      function() {
        jQuery(this).removeClass('hover');
      });
  });
});
