(function() {
  var TECH_URL_BASE = 'https://code.google.com/a/google.com/p/demoqracy/source/browse/';

  function bindTechInfoHandlers() {
    $('#toggle-tech').click(function() {
      $('#tech-info').toggle();
    });

    var lis = [];
    $('[data-tech-name]').each(function () {
      var li = $($.sprintf('<li><a target="_blank" href="%s%s">%s</a></li>',
          TECH_URL_BASE, $(this).data('tech-url'), $(this).data('tech-name')));
      var elementToHighlight = $(this);
      if (this.tagName.toLowerCase() != 'body') {
        li.hover(function() {
          $('#translucent-overlay').show();
          elementToHighlight.addClass('highlighted');
        }, function() {
          $('#translucent-overlay').hide();
          elementToHighlight.removeClass('highlighted');
        });
      }
      $('#tech-info-list').append(li);
    });
  }

  function addPlusOneButton() {
    var po = document.createElement('script');
    po.type = 'text/javascript';
    po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(po, s);
  }

  function addButtonRoles() {
    $('.button').attr('role', 'button');
  }

  $(function() {
    bindTechInfoHandlers();
    addPlusOneButton();
    addButtonRoles();
  });
})();