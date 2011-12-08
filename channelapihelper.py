from datetime import datetime, timedelta
from google.appengine.api import channel, memcache, namespace_manager
from google.appengine.ext import db
import uuid

def customnamespace(original_method):
  def wrapped_method(*args, **kwargs):
    original_namespace = namespace_manager.get_namespace()
    try:
      namespace_manager.set_namespace("channelapihelper")
      return original_method(*args, **kwargs)
    finally:
      namespace_manager.set_namespace(original_namespace)
  return wrapped_method

class ChannelApiHelper():
  channel_lifetime_hours = 2
  channel_lifetime_seconds = channel_lifetime_hours * 60 * 60

  def __init__(self, channel_key):
    if isinstance(channel_key, db.Model):
      channel_key = str(channel_key.key())
    self.channel_key = channel_key

  @customnamespace
  def CreateChannel(self):
    channel_id = uuid.uuid4().get_hex()
    new_channel = Channel(channel_key=self.channel_key,
                          channel_id=channel_id).put()
    current_channels = self.GetActiveChannels()
    already_in_memcache = False
    for current_channel in current_channels:
      if current_channel.channel_id == channel_id:
        already_in_memcache = True
    if not already_in_memcache:
      current_channels.append(new_channel)
      memcache.set(self.channel_key, current_channels)
    return channel.create_channel(channel_id)

  def EarliestActiveTimestamp(self):
    return datetime.now() - timedelta(hours=self.channel_lifetime_hours)

  @customnamespace
  def GetExpiredChannels(self):
    query = Channel.all().filter("created <=", self.EarliestActiveTimestamp())
    return [channel for channel in query]

  @customnamespace
  def GetActiveChannels(self):
    import logging
    channels = memcache.get(self.channel_key)
    if channels is not None:
      logging.info("memcache channels is %s" % channels)
      return channels
    query = Channel.all().filter("channel_key =", self.channel_key).filter(
      "created >", self.EarliestActiveTimestamp())
    channels = [channel for channel in query]
    logging.info("channels is %s" % channels)
    memcache.set(self.channel_key, channels, time=self.channel_lifetime_seconds)
    return channels

  def NotifyChannels(self, message):
    for active_channel in self.GetActiveChannels():
      channel.send_message(active_channel.channel_id, message)


class Channel(db.Model):
  channel_id = db.StringProperty(required=True)
  channel_key = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)