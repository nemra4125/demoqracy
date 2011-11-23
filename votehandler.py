from basehandler import BaseHandler
from google.appengine.api import users
from model import Vote, Candidate, Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized, HTTPBadRequest

class VoteHandler(BaseHandler):
  @login_required
  def get(self, election_id, candidate_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Couldn't find election with id '%s'." %
                           election_id)
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Couldn't find candidate with id '%s' "
                           "in election id '%s'." % (candidate_id, election_id))
    if self.HasAlreadyVoted(election, users.get_current_user()):
      raise HTTPBadRequest("You've already voted in this election.")
    self.render_template("vote.html", name=candidate.name)

  def post(self, election_id, candidate_id):
    voter = users.get_current_user()
    if voter is None:
      raise HTTPUnauthorized("You must be logged in to vote.")
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Couldn't find election with id '%s'." %
                           election_id)
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Couldn't find candidate with id '%s' "
                           "in election id '%s'." % (candidate_id, election_id))
    if self.HasAlreadyVoted(election, voter):
      raise HTTPBadRequest("You've already voted in this election.")
    vote = Vote(parent=candidate, voter=voter, election=str(election.key()))
    vote.put()
    self.render_template("thanks.html", name=candidate.name)

  def HasAlreadyVoted(self, election, voter):
    query = Vote.all().filter("election =", str(election.key())).filter(
      "voter =", voter)
    return query.get() is not None