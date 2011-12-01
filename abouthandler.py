from basehandler import BaseHandler

class AboutHandler(BaseHandler):
  def get(self):
    self.render_template("about.html")
    