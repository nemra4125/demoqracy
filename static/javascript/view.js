(function() {
  var barChart;
  var pieChart;

  window.drawChart = function(electionState) {
    $('#charts').hide();

    if (barChart == null) {
      barChart = new google.visualization.ColumnChart(document.getElementById("bar-chart"));
    }
    if (pieChart == null) {
      pieChart = new google.visualization.PieChart(document.getElementById("pie-chart"));
    }

    var numTotalVotes = 0;

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Candidate');
    data.addColumn('number', 'Votes');
    data.addRows(electionState.length);

    $.each(electionState, function(index, candidate) {
      data.setValue(index, 0, candidate.name);
      data.setValue(index, 1, candidate.votes);
      numTotalVotes += candidate.votes;
    });

    if (numTotalVotes > 0) {
      barChart.draw(data, {colors: ["#caeefc"]});
      pieChart.draw(data);

      $('#charts').fadeIn('slow');
    }
  }

  function openChannelConnection(electionId) {
    $.ajax({
      dataType: 'json',
      url: ($.sprintf('/elections/%s/generate_channel_token', encodeURIComponent(electionId))),
      success: function(json) {
        var channel = new goog.appengine.Channel(json.channelToken);
        var socket = channel.open();
        socket.onmessage = function(message) {
          drawChart($.parseJSON(message.data));
        };
        socket.onerror = function(error) {
          console.log('Channel connection error:');
          console.dir(error);
        };
      }
    });
  }

  $(function() {
    if (window.electionId != null) {
      openChannelConnection(window.electionId);
    }
  });
})();

