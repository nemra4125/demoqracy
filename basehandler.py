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

from google.appengine.api import users
from webapp2_extras import jinja2
import traceback
import webapp2


class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def handle_exception(self, exception, debug):
    stacktrace = ""
    if debug:
      stacktrace = traceback.format_exc()
    if isinstance(exception, webapp2.HTTPException):
      self.response.set_status(exception.code)
      self.render_template("error.html", message=exception.message,
                           stacktrace=stacktrace)
    else:
      self.response.set_status(500)
      self.render_template("error.html", message=exception,
                           stacktrace=stacktrace)

  def render_template(self, filename, **template_args):
    handler_source_file = "%s.py" % self.__class__.__module__
    user = {}
    if users.get_current_user() is None:
      user = {"login_url": users.create_login_url(self.request.uri)}
    else:
      user = {"email": users.get_current_user().email(),
              "user_id": users.get_current_user().user_id(),
              "nickname": users.get_current_user().nickname(),
              "logout_url": users.create_logout_url("/")}
    self.response.write(self.jinja2.render_template(filename,
      handler_source_file=handler_source_file, user=user, **template_args))