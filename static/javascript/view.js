(function() {
  var liveChart;
  var dataTables = [];
  var queuedIndex = 0;
  var historyChart;

  function updateHistoryChart(index) {
    index = parseInt(index);

    if (historyChart == null) {
      historyChart = new google.visualization.PieChart(document.getElementById("history-chart"));
    }

    if (dataTables[index] != null) {
      queuedIndex = null;
      historyChart.draw(dataTables[index], {title: $.sprintf('Vote percentage after %d vote%s.', index + 1, index == 0 ? '' : 's')});
    } else {
      queuedIndex = index;
    }
  }

  function initializeWebWorker(electionHistory, candidates) {
    var worker = new Worker('/static/javascript/view-web-worker.js');
    $(worker).on('message', function(event) {
      var data = event.originalEvent.data;

      dataTables[data.index] = new google.visualization.DataTable(data.dataTable);

      if (data.index == 0) {
        $('#history-range').removeAttr('disabled');
        $('#play').removeAttr('disabled');
      }

      if (data.index == queuedIndex) {
        updateHistoryChart(0);
      }
    });

    worker.postMessage({electionHistory: electionHistory, candidates: candidates});
  }

  function play(index) {
    $('#history-range').val(index);

    updateHistoryChart(index);

    if (index < $('#history-range').attr('max')) {
      setTimeout(function() {
        play(index + 1);
      }, 1000);
    }
  }

  window.updateLiveChart = function(electionState) {
    if (liveChart == null) {
      liveChart = new google.visualization.ColumnChart(document.getElementById("bar-chart"));
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
      liveChart.draw(data, {colors: ["#caeefc"]});
    }
  }

  window.initializeHistoryChart = function() {
    initializeWebWorker(window.electionHistory, window.candidates);

    $('#history-range').change(function() {
      updateHistoryChart($(this).val());
    });

    $('#play').click(function() {
      play(0);
    });
  }

  function openChannelConnection(electionId) {
    $.ajax({
      dataType: 'json',
      url: ($.sprintf('/elections/%s/generate_channel_token', encodeURIComponent(electionId))),
      success: function(json) {
        var channel = new goog.appengine.Channel(json.channelToken);
        var socket = channel.open();
        socket.onmessage = function(message) {
          window.updateLiveChart($.parseJSON(message.data));
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

    if (window.countdownTime != null) {
      $('#countdown').countdown({
        until: new Date(window.countdownTime),
        description: "Election Countdown",
        onExpiry: function() {
          window.location.reload(true);
        }
      });
    }
  });
})();

