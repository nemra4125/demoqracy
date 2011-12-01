from basehandler import BaseHandler

class HowItWorksHandler(BaseHandler):
  def get(self):
    self.render_template("howitworks.html")
    