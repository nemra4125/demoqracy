from basehandler import BaseHandler
from google.appengine.api import channel, users
from model import Vote, Candidate, Election
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized, HTTPBadRequest
import simplejson
import utils

class VoteHandler(BaseHandler):
  @login_required
  def get(self, election_id, candidate_id):
    election, candidate = self.ValidateElectionAndCandidate(
      election_id, candidate_id)
    self.render_template("vote.html", name=candidate.name)

  def post(self, election_id, candidate_id):
    curret_user = users.get_current_user()
    if curret_user is None:
      raise HTTPUnauthorized("You must be logged in to vote.")
    election, candidate = self.ValidateElectionAndCandidate(
      election_id, candidate_id, curret_user)
    if election.record_voter_email:
      voter = curret_user.email()
    else:
      voter = utils.MungeEmailToId(curret_user)
    Vote(parent=candidate, voter=voter, election=str(election.key())).put()
    self.NotifyChannels(election, candidate)
    self.render_template("thanks.html", name=candidate.name)

  def NotifyChannels(self, election, candidate):
    channel_ids = election.GetActiveChannelIds()
    message = simplejson.dumps(dict(election=election.key().id(),
                                    candidate=candidate.key().id()))
    for channel_id in channel_ids:
     channel.send_messge(channel_id, message)

  def ValidateElectionAndCandidate(self, election_id, candidate_id, voter=None):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Couldn't find election with id '%s'." %
                           election_id)
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Couldn't find candidate with id '%s' "
                           "in election id '%s'." % (candidate_id, election_id))
    if voter is None:
      voter = users.get_current_user()
    if election.HasAlreadyVoted(voter):
      raise HTTPBadRequest("You've already voted in this election.")
    return election, candidate