class SlackEvent:
    @property
    def client_msg_id(self):
        return self._client_msg_id

    @client_msg_id.setter
    def client_msg_id(self, client_msg_id):
        self._client_msg_id = client_msg_id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def subtype(self):
        return self._subtype

    @subtype.setter
    def subtype(self, subtype):
        self._subtype = subtype

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        self._time_stamp = time_stamp

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self._channel_id = channel_id

    @property
    def event_time_stamp(self):
        return self._event_time_stamp

    @event_time_stamp.setter
    def event_time_stamp(self, event_time_stamp):
        self._event_time_stamp = event_time_stamp

    @property
    def channel_type(self):
        return self._channel_type

    @channel_type.setter
    def channel_type(self, channel_type):
        self._channel_type = channel_type

    @property
    def thread_time_stamp(self):
        return self._thread_time_stamp

    @thread_time_stamp.setter
    def thread_time_stamp(self, thread_time_stamp):
        self._thread_time_stamp = thread_time_stamp

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def bot_id(self):
        return self._bot_id

    @bot_id.setter
    def bot_id(self, bot_id):
        self._bot_id = bot_id

    @property
    def actions(self):
        return self._actions

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def item_channel(self):
        return self._item_channel

    @item_channel.setter
    def item_channel(self, item_channel):
        self._item_channel = item_channel

    @property
    def files(self):
        return self._files

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
