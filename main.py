from createelectionhandler import CreateElectionHandler
from generatechanneltokenhandler import GenerateChannelTokenHandler
from historyhandler import HistoryHandler
from indexhandler import IndexHandler
from printcandidateshandler import PrintCandidatesHandler
from purgetokenshandler import PurgeTokensHandler
from viewelectionhandler import ViewElectionHandler
from myelectionshandler import MyElectionsHandler
from webvotehandler import WebVoteHandler
from statichandler import StaticHandler
from votehandler import VoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/tasks/purge_tokens', PurgeTokensHandler),
    ('/elections', MyElectionsHandler),
    ('/(terms)', StaticHandler),
    ('/(privacy)', StaticHandler),
    ('/(about)', StaticHandler),
    ('/(how-it-works)', StaticHandler),
    ('/vote/(\d+)', WebVoteHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/(\d+)/print', PrintCandidatesHandler),
    ('/elections/(\d+)/view', ViewElectionHandler),
    ('/elections/(\d+)/history', HistoryHandler),
    ('/elections/(\d+)/generate_channel_token', GenerateChannelTokenHandler),
    ('/(\d+)/(\d+)/vote', VoteHandler),
], debug=True)