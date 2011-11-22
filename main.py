from createelectionhandler import CreateElectionHandler
from indexhandler import IndexHandler
from printcandidateshandler import PrintCandidatesHandler
from votehandler import VoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/([^/]+)/print', PrintCandidatesHandler),
    ('/([^/]+)/([^/]+)/vote', VoteHandler)
], debug=True)