import slack
from botbuilder.schema import Activity

from slack_adapter import NewSlackMessage

class SlackAdapterOptions:
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

    @property
    def slackBotToken(self, fget, fset):
        return self._slackBotToken
    def __get__(self, instance, owner):
        return

    @property
    def SlackClientId(self, fget, fset):
        return self._slackCientId

    @property
    def SlackClientSecret(self, fget, fset):
        return self._SlackClientSecret

    @property
    def slackClientSinginSecret(self):
        return self._slackClientSinginSecret

    @property
    def activity_to_slack(activity: Activity):

        virtual Task<string> GetBotUserByTeamAsync(string teamId, CancellationToken cancellationToken)
        {throw new NotImplementedException();
        public Task<string> GetTokenForTeamAsync(string teamId, CancellationToken cancellationToken)
        {throw new NotImplementedException();Uri SlackRedirectUri{get;set;}
        List < string > SlackScopes {get;} = new List < string > ();
        slackVerificationToken = activity.conversation


    @property
    def SlackClientId(self):
        return self.

