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

from createelectionhandler import CreateElectionHandler
from generatechanneltokenhandler import GenerateChannelTokenHandler
from indexhandler import IndexHandler
from myelectionshandler import MyElectionsHandler
from notifyownerhandler import NotifyOwnerHandler
from postbackverifyhandler import PostbackVerifyHandler
from printcandidateshandler import PrintCandidatesHandler
from purgetokenshandler import PurgeTokensHandler
from statichandler import StaticHandler
from updateelectionhandler import UpdateElectionHandler
from viewelectionhandler import ViewElectionHandler
from votehandler import VoteHandler
from webvotehandler import WebVoteHandler
import webapp2

application = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/tasks/purge_tokens', PurgeTokensHandler),
    ('/elections', MyElectionsHandler),
    ('/(terms)', StaticHandler),
    ('/(privacy)', StaticHandler),
    ('/(about)', StaticHandler),
    ('/(how-it-works)', StaticHandler),
    ('/(postback-verify)', PostbackVerifyHandler),
    ('/vote/(\d+)', WebVoteHandler),
    ('/elections/create', CreateElectionHandler),
    ('/elections/(\d+)/print', PrintCandidatesHandler),
    ('/elections/(\d+)/view', ViewElectionHandler),
    ('/elections/(\d+)/update', UpdateElectionHandler),
    ('/elections/(\d+)/generate_channel_token', GenerateChannelTokenHandler),
    ('/elections/(\d+)/notify_owner', NotifyOwnerHandler),
    ('/(\d+)/(\d+)/vote', VoteHandler),
], debug=False)