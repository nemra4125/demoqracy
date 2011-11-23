(function() {
  window.openChannelConnection = function(electionId) {
//TODO: Uncomment when http://code.google.com/p/googleappengine/issues/detail?id=6267 is fixed in SDK 1.6.1.
//    $.ajax({
//      dataType: 'json',
//      url: ($.sprintf('/elections/%s/generate_channel_token', encodeURIComponent(electionId))),
//      success: function(json) {
//        var channel = new goog.appengine.Channel(json.channelToken);
//        var socket = channel.open();
//        socket.onerror = function() { console.log('Channel connection error.') };
//        socket.onmessage = function(message) { handleChannelMessage(message); };
//      }
//    });
  }
})();