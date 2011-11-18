import webapp2
from indexhandler import IndexHandler
from createelectionhandler import CreateElectionHandler

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/create', CreateElectionHandler)
], debug=True)