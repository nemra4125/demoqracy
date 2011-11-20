import webapp2
from indexhandler import IndexHandler
from createelectionhandler import CreateElectionHandler
from votehandler import VoteHandler
from printcandidateshandler import PrintCandidatesHandler

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/([^/]+)/print', PrintCandidatesHandler),
    ('/([^/]+)/([^/]+)/vote', VoteHandler)
], debug=True)