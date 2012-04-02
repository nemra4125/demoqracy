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

class PrintCandidatesHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None or election.owner != users.get_current_user():
      raise HTTPUnauthorized("You are not the owner of this election.")
    candidates = []
    for candidate in election.GetCandidates():
      candidates.append(dict(
        name=candidate.name,
        url="%s://%s/%s/%s/vote" % (self.request.environ["wsgi.url_scheme"],
                                    self.request.environ["HTTP_HOST"],
                                    election.key().id(),
                                    candidate.key().id())))
    self.render_template("print.html", candidates=candidates,
                         title=election.title)