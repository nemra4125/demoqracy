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
    query = Election.all()
    #query.filter("owner = ", users.get_current_user())
    elections = query.fetch(10)
    self.render_template("myelections.html", elections=elections)