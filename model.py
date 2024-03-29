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

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import db
import constants
import hashlib
import json

class Election(db.Model):
  owner = db.UserProperty(required=True)
  title = db.StringProperty(required=True)
  start = db.DateTimeProperty()
  end = db.DateTimeProperty()
  ads_enabled = db.BooleanProperty(default=True)

  @staticmethod
  def GetElections(owner):
    query = Election.all().filter("owner =", owner).order("title")
    return [election for election in query]

  def GetCandidates(self):
    query = Candidate.all().ancestor(self).order("name")
    return [candidate for candidate in query]

  def GetWinners(self):
    max_votes = -1
    winners = []
    for candidate in Candidate.all().ancestor(self):
      votes = candidate.GetVoteCount()
      if votes > max_votes:
        max_votes = votes
        winners = [candidate]
      elif votes == max_votes:
        winners.append(candidate)
    return winners

  def GetCandidateNamesAsJson(self):
    query = Candidate.all().ancestor(self).order("name")
    candidates = [candidate.name for candidate in query]
    return json.dumps(candidates)

  def CheckStartEndTime(self):
    now = datetime.now()
    if self.start is not None and self.start >= now:
      return constants.NOT_STARTED
    elif self.end is not None and self.end <= now:
      return constants.ENDED
    return constants.ACTIVE

  def HasAlreadyVoted(self, voter):
    voter_id = voter
    if isinstance(voter, users.User):
      voter_id = self.GenerateVoterId(voter)
    query = Vote.all().ancestor(self).filter("voter =", voter_id)
    return query.get() is not None

  def GenerateVoterId(self, user):
    return hashlib.md5(str(self.key()) + user.user_id()).hexdigest()

  def GetElectionStateAsJson(self):
    election_state = [dict(name=candidate.name, votes=candidate.GetVoteCount(),
                           id=candidate.key().id())
                      for candidate
                      in self.GetCandidates()]
    return json.dumps(election_state)

  def GetElectionHistory(self):
    query = Vote.all().filter("election =", str(self.key())).order("vote_time")
    history = [vote.parent().name for vote in query]
    return len(history), json.dumps(history)


class Candidate(db.Model):
  name = db.StringProperty(required=True)

  def GetVoteCount(self):
    query = Vote.all().ancestor(self)
    return query.count()


class Vote(db.Model):
  voter = db.StringProperty(required=True)
  election = db.StringProperty(required=True)
  vote_time = db.DateTimeProperty(auto_now_add=True)