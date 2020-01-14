import slack
from botbuilder.schema import Activity

from slack_adapter import NewSlackMessage

class SlackAdapterOptions:
    @property
    def activity_to_slack(activity:Activity):
        slackVerificationToken = activity.conversation
        slackBotToken = activity.conversation.id
        slackClientSinginSecret = activity.conversation.thread_time_stamp

    @property
    def __options(self):
        return self._options

    @property
    def __identity(self):
        return self._identity

    @property
    def name(self):
        return 'Slack Adapter Options'
    @property
    def middlewares(self):
        return self._middlewares

    def __init__(self, options):
        self._slack = slack.web
        