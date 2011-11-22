(function() {
  $(function() {
    $('#finish_create_election_button').click(function() {
      var form = $(this).closest('form');

      var candidates = [];
      $('.candidate').each(function(index, candidate) {
        candidates.push(candidate.value);
      });

      var hiddenInput = $.sprintf('<input type="hidden" name="candidates" id="candidates" value="%s">', candidates.join('||'));
      $('#candidates').remove();
      $(hiddenInput).appendTo(form);

      form.submit();
    });
  });
})();