from basehandler import BaseHandler
from google.appengine.api import users
from model import Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized

class ViewElectionHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election.owner != users.get_current_user():
      raise HTTPUnauthorized("You are not the owner of this election.")
    candidates = []
    for candidate in election.GetCandidates():
      candidates.append(dict(
        name=candidate.name,
        votes=candidate.GetVoteCount()
      ))
    self.render_template("view.html", candidates=candidates,
                         title=election.title)