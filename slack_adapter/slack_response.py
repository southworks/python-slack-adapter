from .slack_message import SlackMessage


class SlackResponse:
    @property
    def ok(self) -> bool:
        return self._ok

    @property
    def channel(self) -> str:
        return self._channel

    @property
    def time_stamp(self) -> str:
        return self._time_stamp

    @property
    def message(self) -> SlackMessage:
        return self._message
