class SlackMessage:
    @property
    def type(self) -> str:
        return self._type

    @property
    def subtype(self) -> str:
        return self._subtype

    @property
    def text(self) -> str:
        return self._text

    @property
    def time_stamp(self) -> str:
        return self._time_stamp

    @property
    def username(self) -> str:
        return self.username

    @property
    def bot_id(self) -> str:
        return self._bot_id

    @property
    def thread_time_stamp(self) -> str:
        return self._thread_time_stamp
