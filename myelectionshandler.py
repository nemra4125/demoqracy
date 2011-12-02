from basehandler import BaseHandler
from google.appengine.api import users
from model import Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized

class MyElectionsHandler(BaseHandler):
  @login_required
  def get(self):
    if users.get_current_user() is None:
      raise HTTPUnauthorized("You must be logged in to view this page.")
    elections = Election.GetElections(users.get_current_user())
    for election in elections:
      election.id = election.key().id()
      election.candidates = election.GetCandidates()
      for candidate in election.candidates:
        candidate.vote_count = candidate.GetVoteCount()
    self.render_template("myelections.html", elections=elections)