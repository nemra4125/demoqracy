from basehandler import BaseHandler

class StaticHandler(BaseHandler):
  def get(self, page):
    self.render_template("%s.html" % page)
    