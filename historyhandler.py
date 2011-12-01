from basehandler import BaseHandler
from google.appengine.api import users
from model import Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized

class HistoryHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None or election.owner != users.get_current_user():
      raise HTTPUnauthorized("You are not the owner of this election.")
    vote_count, history = election.GetElectionHistory()
    candidates = election.GetCandidateNamesAsJson()
    self.render_template("history.html",
                         history=history,
                         candidates=candidates,
                         vote_count=vote_count - 1,
                         title=election.title)