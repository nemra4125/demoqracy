(function() {
  $(function() {
    $(window).bind('resize', function() {
      var newSize = $(window).width() / 20;
      $('#header').css('font-size', newSize);
    }).trigger('resize');

    var po = document.createElement('script');
    po.type = 'text/javascript';
    po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(po, s);
  });
})();