/******************************************************************************
Copyright 2012 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
******************************************************************************/

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