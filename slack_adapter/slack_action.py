class SlackAction:
    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, action_id):
        self._action_id = action_id

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, block_id):
        self._block_id = block_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def action_time_stamp(self):
        return self._action_time_stamp

    @action_time_stamp.setter
    def action_time_stamp(self, action_time_stamp):
        self._action_time_stamp = action_time_stamp

    def __init__(self, action_id=None, block_id=None, text=None, value=None, type=None, action_time_stamp=None):
        self._action_id = action_id
        self._block_id = block_id
        self._text = text
        self._value = value
        self._type = type
        self._action_time_stamp = action_time_stamp
