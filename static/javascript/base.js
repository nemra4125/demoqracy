(function() {
  var TECH_URL_BASE = 'https://code.google.com/a/google.com/p/demoqracy/source/browse/';

  function techNameToId(name) {
    return name.replace(' ', '-');
  }

  function bindResizeHandler() {
    $(window).bind('resize', function() {
      var newSize = $(window).width() / 20;
      $('#header').css('font-size', newSize);
    }).trigger('resize');
  }

  function bindTechInfoHandlers() {
    $('#toggle-tech').click(function() {
      $('#tech-info').toggle();
    });

    var lis = [];
    $('[data-tech-name]').each(function () {
      var liId = techNameToId($(this).data('tech-name'));
      var li = $.sprintf('<li id="%s"><a target="_blank" href="%s%s">%s</a></li>',
          liId, TECH_URL_BASE, $(this).data('tech-url'), $(this).data('tech-name'));
      lis.push(li);

      $(this).hover(function(event) {
        $('#' + liId).css('list-style', 'disc outside none');
      }, function(event) {
        $('#' + liId).css('list-style', 'none');
      });
    });
    $('#tech-info').append($.sprintf('<ul>%s</ul>', lis.sort().join('')));
  }

  function addPlusOneButton() {
    var po = document.createElement('script');
    po.type = 'text/javascript';
    po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(po, s);
  }

  $(function() {
    bindResizeHandler();
    bindTechInfoHandlers();
    addPlusOneButton();
  });
})();