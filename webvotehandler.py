from basehandler import BaseHandler
from google.appengine.api import channel, users
from model import Vote, Candidate, Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized, HTTPBadRequest

class WebVoteHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPUnauthorized("Invalid election.")
    
    message = ""
    canvote = True
    show_ads = True

    if election.ads_enabled == False:
      show_ads = False
    
    if election.HasAlreadyVoted(users.get_current_user()):
      message = "You've already voted in this election."
      canvote = False
      
    election_state = election.GetElectionStateAsJson()
    candidates = election.GetCandidates()
    for candidate in candidates:
      candidate.id = candidate.key().id()
    self.render_template("webvote.html",
                         election_state=election_state,
                         title=election.title,
                         election_id=election_id,
                         election_is_active=election.IsActive(),
                         candidates=candidates,
                         canvote=canvote,
                         message=message,
                         show_ads=show_ads)
  
  # Should be abstracted into a common class
  def NotifyChannels(self, election):
    message = election.GetElectionStateAsJson()
    for channel_id in election.GetActiveChannelIds():
      channel.send_message(channel_id, message)
    
  def post(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Invalid election provided")
    
    try:
      candidate_id = self.request.get("candidate")
    except AttributeError:
      raise HTTPBadRequest("No candidate provided")
    
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Invalid candidate provided")
    
    # Get current voter
    voter_id = election.GenerateVoterId(users.get_current_user())
      
    # Register the vote
    Vote(parent=candidate, voter=voter_id, election=str(election.key())).put()
    
    # Notify the channels
    self.NotifyChannels(election)
    
    # Show a confirmation message
    self.render_template("webvote.html",
                         canvote=False,
                         message="Thanks! Your vote has been recorded",
                         show_ads=election.ads_enabled)
    
     
    