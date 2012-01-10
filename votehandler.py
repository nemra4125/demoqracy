from basehandler import BaseHandler
from channelapihelper import ChannelApiHelper
from google.appengine.api import users
from model import Vote, Candidate, Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized, HTTPBadRequest

class VoteHandler(BaseHandler):
  @login_required
  def get(self, election_id, candidate_id):
    election, candidate = self.ValidateElectionAndCandidate(election_id,
                                                            candidate_id)
    message = ""
    canvote = True
    # TODO: All this is ugly, and needs to be a) refactored and b) not rely
    # on a poorly named method that returns strings representing the election
    # state.
    election_active_state = election.CheckStartEndTime()
    if election_active_state == "NOT_STARTED":
      message = "This election has not started yet."
      canvote = False
    elif election_active_state == "ENDED":
      message = "This election has ended."
      canvote = False
    if election.HasAlreadyVoted(users.get_current_user()):
      message = "You've already voted in this election."
      canvote = False
    self.render_template("vote.html", title=election.title, 
                         name=candidate.name, message=message, 
                         canvote=canvote, show_ads=election.ads_enabled)

  def post(self, election_id, candidate_id):
    if self.request.get("cancel_button") == "True":
       self.render_template("vote.html", message="Your vote has been discarded")
       return
    election, candidate = self.ValidateElectionAndCandidate(election_id,
                                                            candidate_id)
    current_user = users.get_current_user()
    if current_user is None:
      raise HTTPUnauthorized("You must be logged in to vote.")
    if election.HasAlreadyVoted(current_user):
      raise HTTPUnauthorized("You've already voted in this election.")
    election_active_state = election.CheckStartEndTime()
    if election_active_state == "NOT_STARTED":
      raise HTTPBadRequest("This election has not started yet.")
    elif election_active_state == "ENDED":
      raise HTTPBadRequest("This election has ended.")
    voter_id = election.GenerateVoterId(current_user)
    Vote(parent=candidate, voter=voter_id, election=str(election.key())).put()
    self.NotifyChannels(election)
    self.render_template("vote.html", canvote=False,
        message="Thanks! Your vote for %s was registered." % candidate.name)

  def NotifyChannels(self, election):
    message = election.GetElectionStateAsJson()
    ChannelApiHelper(election).NotifyChannels(message)

  def ValidateElectionAndCandidate(self, election_id, candidate_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Couldn't find election with id '%s'." %
                           election_id)
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Couldn't find candidate with id '%s' "
                           "in election id '%s'." % (candidate_id, election_id))
  
    return election, candidate