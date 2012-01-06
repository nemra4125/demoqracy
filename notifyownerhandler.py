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
             (election.title, election.GetWinners())
      )