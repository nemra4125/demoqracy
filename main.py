import webapp2
from indexhandler import IndexHandler

application = webapp2.WSGIApplication([('/', IndexHandler)], debug=True)