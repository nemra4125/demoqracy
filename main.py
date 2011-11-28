from createelectionhandler import CreateElectionHandler
from indexhandler import IndexHandler
from printcandidateshandler import PrintCandidatesHandler
from viewelectionhandler import ViewElectionHandler
from myelectionshandler import MyElectionsHandler
from votehandler import VoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/([^/]+)/print', PrintCandidatesHandler),
    ('/elections/([^/]+)/view', ViewElectionHandler),
    ('/([^/]+)/([^/]+)/vote', VoteHandler),
    ('/elections', MyElectionsHandler),
], debug=True)