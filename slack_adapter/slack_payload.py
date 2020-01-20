class SlackPayload:
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def thread_time_stamp(self):
        return self._thread_time_stamp

    @thread_time_stamp.setter
    def thread_time_stamp(self, thread_time_stamp):
        self._thread_time_stamp = thread_time_stamp

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team):
        self._team = team

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, actions):
        self._actions = actions

    def __init__(self, type=None, token=None, channel=None, thread_time_stamp= None, team=None,
                 message=None, user=None, actions=None):
        self._type = type
        self._token = token
        self._channel = channel
        self._thread_time_stamp = thread_time_stamp
        self._team = team
        self._message = message
        self._user = user
        self._actions = actions
