from basehandler import BaseHandler
from webapp2_extras.appengine.users import login_required

class IndexHandler(BaseHandler):
  @login_required
  def get(self):
    self.render_template("index.html")