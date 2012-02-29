# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Helper methods and classes for using the App Engine Channel API.

The Python App Engine API (documented at
http://code.google.com/appengine/docs/python/channel/overview.html)
provides a way of communicating from a web server to browser clients in near
real time. There's significant overheard involved in saving state and keeping
track of which clients need to be notified of which messages, though. The goal
of this module is to help with some common tasks related to that.

The module takes care of generating new channel tokens which can be returned to
a browser client. The corresponding channel id and a unique "channel key" (used
to determine what's being listened to) is stored in both the datastore and
memcache. Custom namespaces are used to prevent any collisions with existing
datastore or memcache entries.
"""

__author__ = 'jeffy@google.com (Jeffrey Posnick)'

from datetime import datetime, timedelta
from uuid import uuid4
from google.appengine.api import channel, memcache, namespace_manager
from google.appengine.ext import db


DATASTORE_NAMESPACE = "channelapihelper"
# This corresponds to the current lifetime of a given channel connection.
CHANNEL_LIFETIME_HOURS = 2
CHANNEL_LIFETIME_SECONDS = CHANNEL_LIFETIME_HOURS * 60 * 60


# Set up a default SendChannelMessage method for when threading isn't supported.
SendChannelMessage = lambda channel_id, message: channel.send_message(
  channel_id, message)
# The Python 2.7 App Engine runtime supports threading, so let's see if we can
# use it.
try:
  import threading
  SendChannelMessage = lambda channel_id, message: threading.Thread(
    target=channel.send_message, args=(channel_id, message)).start()
except ImportError:
  pass


def customnamespace(original_method):
  """Decorator to use a custom App Engine namespace temporarily.

  The namespace applies to all memcache and datastore calls.
  See http://code.google.com/appengine/docs/python/multitenancy/overview.html
  """
  def wrapped_method(*args, **kwargs):
    original_namespace = namespace_manager.get_namespace()
    try:
      namespace_manager.set_namespace(DATASTORE_NAMESPACE)
      return original_method(*args, **kwargs)
    finally:
      namespace_manager.set_namespace(original_namespace)
  return wrapped_method


def EarliestActiveTimestamp():
  """Calculates the earliest timestamp of an active channel.

  Returns:
    A DateTime representing the earliest possible timestamp of an active
    channel.
  """
  return datetime.now() - timedelta(hours=CHANNEL_LIFETIME_HOURS)


@customnamespace
def GetExpiredChannels():
  """Gets all Channel objects that are expired.

  The list of expired Channel objects doesn't depend on a specific channel_key.

  Returns:
    A list of Channel objects whose created timestamp indicates that they're old
    enough to be expired.
  """
  query = Channel.all().filter("created <=", EarliestActiveTimestamp())
  return [channel for channel in query]


class ChannelApiHelper(object):
  """Methods to help with creating and keeping track of Channel API channels.

  Attributes:
    channel_key: A string used to identify what an instance is keeping track of.
      The exact value to use here is domain-specific; however, as a shortcut,
      you can pass in a db.Model instance to the constructor and its key will be
      used.
  """

  def __init__(self, channel_key):
    """Creates a new ChannelApiHelper to track the resource channel_key.

    Args:
      channel_key: A string or db.Model instance.
    """
    if isinstance(channel_key, db.Model):
      channel_key = str(channel_key.key())
    self.channel_key = channel_key

  @customnamespace
  def CreateChannel(self):
    """Creates a new channel with a given key.

    This should be called when a browser client wants to receive updates about a
    given resource (identified by self.channel_key).

    A new Channel object is saved to the datastore and memcache.

    Returns:
      A string that can be used by browser clients as a token for connecting to
      the new channel. This corresponds to the "token" value which is passed to
      the JavaScript goog.appengine.Channel() constructor, documented at
      http://code.google.com/appengine/docs/python/channel/javascript.html
    """
    channel_id = uuid4().get_hex()
    new_channel = Channel(channel_key=self.channel_key,
                          channel_id=channel_id)
    new_channel.put()
    current_channels = self.GetActiveChannels()
    already_in_memcache = False
    for current_channel in current_channels:
      if current_channel.channel_id == channel_id:
        already_in_memcache = True
    if not already_in_memcache:
      current_channels.append(new_channel)
      memcache.set(self.channel_key, current_channels)
    return channel.create_channel(channel_id)

  @customnamespace
  def GetActiveChannels(self):
    """Gets a list of active channels for a given key.

    Returns:
      A list of Channel objects, each of which has self.channel_key as their
      channel_key attribute. The list should normally only contain channels that
      haven't expired, but if read from memcache it's possible that a few
      expired channels could sneak in.
    """
    channels = memcache.get(self.channel_key)
    if channels is not None:
      return channels
    query = Channel.all().filter("channel_key =", self.channel_key).filter(
      "created >", EarliestActiveTimestamp())
    channels = [channel for channel in query]
    memcache.set(self.channel_key, channels, time=CHANNEL_LIFETIME_SECONDS)
    return channels

  def NotifyChannels(self, message):
    """Sends a message to all active channels with a given key.

    If threading is enabled (e.g. because the App Engine instance is using the
    Python 2.7 runtime) then new threads will be created to send the message
    to each connected client.

    Otherwise, the clients will be notified sequentially.

    Args:
      message: A string to send to all active browser clients. A best-practice
        is to use a JSON-encoded string to represent a complex Python object.
    """
    active_channels = self.GetActiveChannels()
    for active_channel in active_channels:
      SendChannelMessage(active_channel.channel_id, message)


class Channel(db.Model):
  """A class to keep track of relevant channel info in the datastore.

  Attributes:
    channel_id: A globally-unique string that identifies a particular connection
      with a browser client. Using a uuid or similar is recommended.
    channel_key: A string that uniquely identifies what the channel is keeping
      track of. Use something that makes sense for your application, like the
      key corresponding to a particular db.Model instance.
    created: A DateTime that is automatically set to the current time upon
      creation. It is used to keep track of whether a given Channel is expired.
  """
  channel_id = db.StringProperty(required=True)
  channel_key = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)