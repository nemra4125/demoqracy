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