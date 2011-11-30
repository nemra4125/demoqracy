from basehandler import BaseHandler
from google.appengine.api import channel, users
from model import Vote, Candidate, Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized, HTTPBadRequest

class VoteHandler(BaseHandler):
  @login_required
  def get(self, election_id, candidate_id):
    election, candidate = self.ValidateElectionAndCandidate(
      election_id, candidate_id)
    
    message = ""
    canvote = True
    
    if election.HasAlreadyVoted(users.get_current_user()):
      message = "You've already voted in this election."
      canvote = False
      #raise HTTPBadRequest("You've already voted in this election.")
    
    self.render_template("vote.html", title=election.title, 
                         name=candidate.name, message=message, 
                         canvote=canvote)

  def post(self, election_id, candidate_id):
    if self.request.get("cancel_button") == "True":
       self.render_template("vote.html", message="Your vote has been discarded")
       return
    current_user = users.get_current_user()
    if current_user is None:
      raise HTTPUnauthorized("You must be logged in to vote.")
    election, candidate = self.ValidateElectionAndCandidate(
      election_id, candidate_id, current_user)
    voter_id = election.GenerateVoterId(current_user)
    Vote(parent=candidate, voter=voter_id, election=str(election.key())).put()
    self.NotifyChannels(election)
    self.render_template("vote.html", canvote=False, message="Thanks! Your vote for %s has been registered." % candidate.name)

  def NotifyChannels(self, election):
    message = election.GetElectionStateAsJson()
    for channel_id in election.GetActiveChannelIds():
      channel.send_message(channel_id, message)

  def ValidateElectionAndCandidate(self, election_id, candidate_id, voter=None):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Couldn't find election with id '%s'." %
                           election_id)
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Couldn't find candidate with id '%s' "
                           "in election id '%s'." % (candidate_id, election_id))
  
    return election, candidate