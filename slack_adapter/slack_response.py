class SlackResponse:
    @property
    def ok(self):
        return self._ok

    @property
    def channel(self):
        return self._channel

    @property
    def time_stamp(self):
        return self._time_stamp

    @property
    def message(self):
        return self._message
