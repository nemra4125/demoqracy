(function() {
  addEventListener('message', function(message) {
    var state = {};
    var candidates = message.data.candidates;
    var electionHistory = message.data.electionHistory;

    var dataTable = {
      cols: [
        { label: 'Candidate', type: 'string' },
        { label: 'Votes', type: 'number' }
      ],
      rows: []
    };

    var candidateToRowNumber = {};
    candidates.forEach(function(candidate, index) {
      dataTable.rows.push({c: [{v: candidate}, {v: 0}]});
      candidateToRowNumber[candidate] = index;
    });

    electionHistory.forEach(function(voteForCandidate, index) {
      var rowNumber = candidateToRowNumber[voteForCandidate];
      dataTable.rows[rowNumber].c[1].v++;
      postMessage({ index: index, dataTable: dataTable });
    });
  }, false);
})();