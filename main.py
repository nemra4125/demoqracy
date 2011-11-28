from createelectionhandler import CreateElectionHandler
from generatechanneltokenhandler import GenerateChannelTokenHandler
from indexhandler import IndexHandler
from printcandidateshandler import PrintCandidatesHandler
from purgetokenshandler import PurgeTokensHandler
from viewelectionhandler import ViewElectionHandler
from myelectionshandler import MyElectionsHandler
from votehandler import VoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/tasks/purge_tokens', PurgeTokensHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/([^/]+)/print', PrintCandidatesHandler),
    ('/elections/([^/]+)/view', ViewElectionHandler),
    ('/([^/]+)/([^/]+)/vote', VoteHandler),
    ('/elections', MyElectionsHandler),
], debug=True)