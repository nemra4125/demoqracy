(function() {
  var dataTables = [];
  var queuedIndex = 0;
  var chart;

  function drawChart(index) {
    index = parseInt(index);
    
    if (chart == null) {
      chart = new google.visualization.PieChart(document.getElementById("chart"));
    }

    if (dataTables[index] != null) {
      queuedIndex = null;
      chart.draw(dataTables[index], {title: $.sprintf('History after %d vote%s.', index + 1, index == 0 ? '' : 's')});
    } else {
      queuedIndex = index;
    }
  }

  function initializeWebWorker(electionHistory, candidates) {
    var worker = new Worker('/static/javascript/history-worker.js');
    $(worker).on('message', function(event) {
      var data = event.originalEvent.data;

      dataTables[data.index] = new google.visualization.DataTable(data.dataTable);

      if (data.index == 0) {
        $('#history-range').removeAttr('disabled');
        $('#play').removeAttr('disabled');
      }

      if (data.index == queuedIndex) {
        drawChart(0);
      }
    });

    worker.postMessage({electionHistory: electionHistory, candidates: candidates});
  }

  function play(index) {
    $('#history-range').val(index);

    drawChart(index);

    if (index < $('#history-range').attr('max')) {
      setTimeout(function() {
        play(index + 1);
      }, 1000);
    }
  }

  window.onLoadCallback = function() {
    initializeWebWorker(window.electionHistory, window.candidates);

    $('#history-range').change(function() {
      drawChart($(this).val());
    });

    $('#play').click(function() {
      play(0);
    });
  };
})();