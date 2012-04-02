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
from google.appengine.api import mail
from model import Election

class NotifyOwnerHandler(BaseHandler):
  def post(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is not None:
      mail.send_mail(
        sender="demoQRacy <no-reply@demoqracy.appspotmail.com>",
        to=election.owner.email(),
        subject="The election '%s' has ended!" % election.title,
        body="The election '%s' has ended, and '%s' has won!" %
             (election.title,
              ", ".join([winner.name for winner in election.GetWinners()]))
      )