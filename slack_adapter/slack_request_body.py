class SlackRequestBody:

    @property
    def challenge(self):
        return self._challenge

    @challenge.setter
    def challenge(self, challenge):
        self._challenge = challenge

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, team_id):
        self._team_id = team_id

    @property
    def api_app_id(self):
        return self._api_app_id

    @api_app_id.setter
    def api_app_id(self, api_app_id):
        self._api_app_id = api_app_id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        self._event_id = event_id

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, event_time):
        self._event_time = event_time

    @property
    def authed_users(self):
        return self._authed_users

    @property
    def trigger_id(self):
        return self._trigger_id

    @trigger_id.setter
    def trigger_id(self, trigger_id):
        self._trigger_id = trigger_id

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self._channel_id = channel_id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, event):
        self._event = event

    def __init__(self, challenge=None, token=None, team_id=None, api_app_id=None, type=None, event_id=None, event_time=None, trigger_id=None, channel_id=None, user_id=None, text=None, command=None, payload=None, event=None):
        self._challenge = challenge
        self._token = token
        self._team_id = team_id
        self._api_app_id = api_app_id
        self._type = type
        self._event_id = event_id
        self._event_time = event_time
        self._trigger_id = trigger_id
        self._channel_id = channel_id
        self._user_id = user_id
        self._text = text
        self._command = command
        self._payload = payload
        self._event = event
