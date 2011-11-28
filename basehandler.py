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
    self.response.write(self.jinja2.render_template(filename, user=users.get_current_user(), **template_args))