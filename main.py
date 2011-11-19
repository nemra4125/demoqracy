import webapp2
from indexhandler import IndexHandler
from createelectionhandler import CreateElectionHandler
from votehandler import VoteHandler

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/elections/create', CreateElectionHandler),
    ('/([^/]+)/vote', VoteHandler)
], debug=True)