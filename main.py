from createelectionhandler import CreateElectionHandler
from generatechanneltokenhandler import GenerateChannelTokenHandler
from indexhandler import IndexHandler
from myelectionshandler import MyElectionsHandler
from notifyownerhandler import NotifyOwnerHandler
from postbackverifyhandler import PostbackVerifyHandler
from printcandidateshandler import PrintCandidatesHandler
from purgetokenshandler import PurgeTokensHandler
from statichandler import StaticHandler
from updateelectionhandler import UpdateElectionHandler
from viewelectionhandler import ViewElectionHandler
from votehandler import VoteHandler
from webvotehandler import WebVoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/tasks/purge_tokens', PurgeTokensHandler),
    ('/elections', MyElectionsHandler),
    ('/(terms)', StaticHandler),
    ('/(privacy)', StaticHandler),
    ('/(about)', StaticHandler),
    ('/(how-it-works)', StaticHandler),
    ('/(postback-verify)', PostbackVerifyHandler),
    ('/vote/(\d+)', WebVoteHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/(\d+)/print', PrintCandidatesHandler),
    ('/elections/(\d+)/view', ViewElectionHandler),
    ('/elections/(\d+)/update', UpdateElectionHandler),
    ('/elections/(\d+)/generate_channel_token', GenerateChannelTokenHandler),
    ('/elections/(\d+)/notify_owner', NotifyOwnerHandler),
    ('/(\d+)/(\d+)/vote', VoteHandler),
], debug=True)