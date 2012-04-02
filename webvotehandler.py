# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from basehandler import BaseHandler
from channelapihelper import ChannelApiHelper
import constants
from google.appengine.api import users
from model import Candidate, Election, Vote
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized, HTTPBadRequest

class WebVoteHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Invalid election.")
    message = ""
    canvote = True
    # TODO: All this is ugly, and needs to be a) refactored and b) not rely
    # on a poorly named method that returns strings representing the election
    # state.
    election_active_state = election.CheckStartEndTime()
    if election_active_state == constants.NOT_STARTED:
      message = "This election has not started yet."
      canvote = False
    elif election_active_state == constants.ENDED:
      message = "This election has ended."
      canvote = False

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
                         candidates=candidates,
                         canvote=canvote,
                         message=message,
                         show_ads=election.ads_enabled)
    
  def post(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("Invalid election id provided.")
    current_user = users.get_current_user()
    if current_user is None:
      raise HTTPUnauthorized("You must be logged in to vote.")
    if election.HasAlreadyVoted(current_user):
      raise HTTPUnauthorized("You've already voted in this election.")
    election_active_state = election.CheckStartEndTime()
    if election_active_state == constants.NOT_STARTED:
      raise HTTPBadRequest("This election has not started yet.")
    elif election_active_state == constants.ENDED:
      raise HTTPBadRequest("This election has ended.")
    candidate_id = self.request.get("candidate")
    if candidate_id is None:
      raise HTTPBadRequest("No candidate was provided.")
    candidate = Candidate.get_by_id(long(candidate_id), parent=election)
    if candidate is None:
      raise HTTPBadRequest("Invalid candidate id provided.")
    voter_id = election.GenerateVoterId(current_user)
    Vote(parent=candidate, voter=voter_id, election=str(election.key())).put()
    self.NotifyChannels(election)
    self.render_template("webvote.html",
                         canvote=False,
                         message="Thanks! Your vote has been recorded",
                         show_ads=election.ads_enabled)

  def NotifyChannels(self, election):
    message = election.GetElectionStateAsJson()
    ChannelApiHelper(election).NotifyChannels(message)