from .slack_adapter_options import SlackAdapterOptions


class SlackClientWrapper:
    post_message_url = "https://slack.com/api/chat.postMessage"
    post_ephemeral_message_url = "https://slack.com/api/chat.postEphemeral"

    def __init__(self, options: SlackAdapterOptions):
        self._options = options if options else ValueError(type(options))
