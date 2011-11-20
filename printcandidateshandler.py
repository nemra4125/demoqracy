import datetime
from basehandler import BaseHandler
from google.appengine.api import users
from model import Election
from model import Candidate
from utils import ProcessParams
from webob.exc import HTTPUnauthorized
from webapp2_extras.appengine.users import login_required
from google.appengine.ext import db

class PrintCandidatesHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    query = Candidate.all()
    query.ancestor(election.key())
    candidates = []
    for candidate in query.fetch(limit=100):
      candidates.append(dict(
        name=candidate.name,
        url="%s://%s/%s/%s/vote" % (self.request.environ["wsgi.url_scheme"],
                                    self.request.environ["HTTP_HOST"],
                                    election.key().id(),
                                    candidate.key().id())))
    self.render_template("print.html", candidates=candidates,
                         title=election.title)