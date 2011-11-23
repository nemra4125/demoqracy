from createelectionhandler import CreateElectionHandler
from generatechanneltokenhandler import GenerateChannelTokenHandler
from indexhandler import IndexHandler
from printcandidateshandler import PrintCandidatesHandler
from viewelectionhandler import ViewElectionHandler
from votehandler import VoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/([^/]+)/print', PrintCandidatesHandler),
    ('/elections/([^/]+)/view', ViewElectionHandler),
    ('/elections/([^/]+)/generate_channel_token', GenerateChannelTokenHandler),
    ('/([^/]+)/([^/]+)/vote', VoteHandler)
], debug=True)