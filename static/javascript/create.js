(function() {
  
  /**
   * Shared vars
   */
  var long_date_format = "MM d, yy"  
  
  /**
   * Handle create election submissions
   */ 
  $(function() {
    $('#finish_create_election_button')
        .click(
            function() {
              var form = $(this).closest('form');
              
              // Start date timestamp 
              var start_ts = $("#start_date_field").val() != "" ? 
                  Date.parse($("#start_date_field").val()) / 1000 : 0;
              // End date timestamp
              var end_ts = $("#end_date_field").val() != "" ? 
                  Date.parse($("#end_date_field").val()) / 1000 : 0;
              
              // Validate
              var errors = [];
              if (end_ts < start_ts) {
                errors.push("End date cannot come before start date");
              }
              if ($("#title_field").val() == "") {
                errors.push("Title must not be blank");
              }
              var valid_candidate_count = 0;
              $('.candidate').each(function() {
                if ($(this).val() != "") {
                  valid_candidate_count++;
                }
              });
              if (valid_candidate_count < 2) {
                errors.push("You must provide at least two candidates");
              }
              // Add errors to page
              if (errors.length > 0) {
                $("#create_errors").empty();
                for (i=0; i<errors.length; i++) {
                  $("#create_errors").append("<li>" + errors[i] + "</li>");
                }
                $("#create_errors").css("display", "block");
                window.location = "#create_errors";
                return false;
              }

              // Concatenate candidates and put them in a hidden field
              var candidates = [];
              $('.candidate').each(function(index, candidate) {
                candidates.push(candidate.value);
              });

              var hiddenCandidatesInput = $
              .sprintf(
                  '<input type="hidden" name="candidates" id="candidates" value="%s">',
                  candidates.join('||'));
              $('#candidates').remove();
              $(hiddenCandidatesInput).appendTo(form);
              
              // Convert dates to timestamps and put them in hidden fields
              
              var hiddenStartTimestamp = $
              .sprintf(
                  '<input type="hidden" name="start_ts" id="start_ts" value="%s">',
                  start_ts);
              $(hiddenStartTimestamp).appendTo(form);
          
              var hiddenEndTimestamp = $
              .sprintf(
                  '<input type="hidden" name="end_ts" id="end_ts" value="%s">',
                  end_ts);
              $(hiddenEndTimestamp).appendTo(form);
              
              form.submit();
              
              // Cancel click prop
              return false;
            });
  });

  /**
   * Add new candidate link
   */ 
  $(function() {
    $('#add_new_candidate_form_row').click(function() {
      var last_li = $('.candidate:last').parent();
      last_li.after(last_li.clone());
      $('.candidate:last').val("");
      $('.candidate_remove:last').bind("click", remove_candidate_row);
      // Show remove buttons. No need to check for minimum since
      // adding a new row should always be the third or more row
      $('.candidate_remove').css('display', 'inline');
      // cancel click prop
      return false;
    });
  });
  
  /**
   * Handler for removing candidate rows 
   */ 
  function remove_candidate_row(event) {
    $(this).parent().remove();
    // If only two remaining, hide remove buttons
    if ($('.candidate_remove').length == 2) {
      $('.candidate_remove').css('display', 'none');
    }
  }
  
  /**
   * Set up initial handlers for removing candidate rows
   */ 
  $(function() {
    $('.candidate_remove').click(remove_candidate_row);
  });
  
  /**
   * Set up date pickers
   */
  $(function() {
    $('#start_date_field').datepicker({
      inline: true,
      dateFormat: long_date_format
    });
    
    $('#end_date_field').datepicker({
      inline: true,
      dateFormat: long_date_format
    });
  });
  
})();