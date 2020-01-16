from .file_types import FileTypes
from .slack_adapter_options import SlackAdapterOptions
from .presence import Presence


class SlackClientWrapper:
    post_message_url = "https://slack.com/api/chat.postMessage"
    post_ephemeral_message_url = "https://slack.com/api/chat.postEphemeral"

    @property
    def api(self):
        return self._api
    
    @property
    def options(self) -> SlackAdapterOptions:
        """
            Gets the SlackAdapterOptions.
        """
        return self._options

    @property
    def identity(self) -> SlackAdapterOptions:
        """
            Gets the user identity.
        """
        return self._identity

    def __init__(self, options: SlackAdapterOptions):
        """
            Initializes a new instance of the <see cref="SlackClientWrapper"/> class.
            Creates a Slack client by supplying the access token.
        """
        self._options = options if options else ValueError(type(options))
        if not options.slackVerificationToken and not options.slackClientSigningSecret:
            warning = '"****************************************************************************************"' \
                      '"* WARNING: Your bot is operating without recommended security mechanisms in place.     *"' \
                      '"* Initialize your adapter with a clientSigningSecret parameter to enable               *"' \
                      '"* verification that all incoming webhooks originate with Slack:                        *"' \
                      '"*                                                                                      *"' \
                      '"* var adapter = new SlackAdapter({clientSigningSecret: <my secret from slack>});       *"' \
                      '"*                                                                                      *"' \
                      '"****************************************************************************************"' \
                      '">> Slack docs: https://api.slack.com/docs/verifying-requests-from-slack"'
            raise Exception(warning + "\n" + 'Required: include a verificationToken or clientSigningSecret to verify '
                                             'incoming Events API webhooks')
        self._api = SlackTaskClient(options.slackBotToken)
        self.login_with_slack(default).wait()

    async def add_reaction(self, name=None, channel=None, time_stamp=None, cancellation_token=None):
        """
            Wraps Slack API's AddReactionAsync method.
        """
        return await self._api.add_reaction(name, channel, time_stamp).configure_await(False)

    async def API_request_with_token(self, cancellation_token, *post_parameters):
        """
            Wraps Slack API's APIRequestWithTokenAsync method.
        """
        return await self._api.API_request_with_token(post_parameters).configure_await(False)\
            if not post_parameters else\
            await self._api.API_request_with_token().configure_await(False)

    async def channel_set_topic(self, channel_id, new_topic, cancellation_token):
        """
            Wraps Slack API's ChannelSetTopicAsync method.
        """
        return await self._api.channel_set_topic(channel_id, new_topic).configure_await(False)

    async def channel_is_invite(self, user_id, channel_id, cancellation_token):
        """
            Wraps Slack API's ChannelsInviteAsync method.
        """
        return await self._api.channel_is_invite(user_id, channel_id).configure_await(False)

    async def connect(self, cancellation_token):
        """
            Wraps Slack API's ConnectAsync method.
        """
        return await self._api.connect().configure_await(False)

    async def delete_message(self, channel_id, ts, cancellation_token):
        """
            Wraps Slack API's DeleteMessageAsync method.
        """
        return await self._api.delete_message(channel_id, ts).configure_await(False)

    async def dialog_open(self, trigger_id, dialog, cancellation_token):
        """
            Wraps Slack API's DialogOpenAsync method.
        """
        return await self._api.dialog_open(trigger_id, dialog).configure_await(False)

    async def emit_login(self, agent='Inumedia.SlackAPI', cancellation_token=None):
        """
            Wraps Slack API's EmitLoginAsync method.
        """
        return await self._api.emit_login(agent).configure_await(False)

    async def emit_presence(self, status: Presence, cancellation_token):
        """
            Wraps Slack API's EmitPresence method.
        """
        return await self._api.emit_presence(status).configure_await(False)

    async def get_channel_history(self, channel_info, latest=None, oldest=None, count=0, cancellation_token=None):
        """
            Wraps Slack API's GetChannelHistoryAsync method.
        """
        return await self._api.get_channel_history(channel_info, latest, oldest, count).configure_await(False)

    async def get_channel_list(self, exclude_archived=True, cancellation_token=None):
        """
            Wraps Slack API's GetChannelListAsync method.
        """
        return await self._api.get_channel_list(exclude_archived).configure_await(False)

    async def post_message_async(self, message, cancellation_token):
        pass

    async def get_counts(self, cancellation_token):
        """
            Wraps Slack API's GetCountsAsync method.
        """
        return await self._api.get_counts().configure_await(False)

    async def get_direct_message_history(self, conversation_info, latest, oldest, count, cancellation_token):
        """
            Wraps Slack API's GetDirectMessageHistoryAsync method.
        """
        return await self._api.get_direct_message_history(conversation_info, latest, oldest, count).configure_await(False)

    async def get_direct_message_list(self, cancellation_token):
        """
            Wraps Slack API's GetDirectMessageListAsync method.
        """
        return await self._api.get_direct_message_list().configure_await(False)

    async def get_file_info(self, file_id, page=None, count=None, cancellation_token=None):
        """
            Wraps Slack API's GetFileInfoAsync method.
        """
        return await self._api.get_file_info(file_id, page, count).configure_await(False)

    async def get_files(self, user_id=None, date_from=None, date_to=None, count=None, page=None, types=FileTypes.All,
                        cancellation_token=None):
        """
            Wraps Slack API's GetFilesAsync method.
        """
        return await self._api.get_files(user_id, date_from, date_to, count, page, types).configure_await(False)

    async def get_group_history(self, group_info, latest=None, oldest=None, count=None, cancellation_token=None):
        """
            Wraps Slack API's GetGroupHistoryAsync method.
        """
        return await self._api.get_group_history(group_info, latest, oldest, count).configure_await(False)

    async def get_groups_list(self, exclude_archived=True, cancellation_token=None):
        """
            Wraps Slack API's GetGroupsListAsync method.
        """
        return await self._api.get_groups_list(exclude_archived).configure_await(False)

    async def get_preferences(self, cancellation_token):
        """
            Wraps Slack API's GetPreferencesAsync method.
        """
        return await self._api.get_preferences().configure_await(False)

    async def get_stars(self, user_id=None, count=None, page=None, cancellation_token=None):
        """
            Wraps Slack API's GetStarsAsync method.
        """
        return await self._api.get_stars(user_id, count, page).configure_await(False)

    async def get_user_list(self, cancellation_token):
        """
            Wraps Slack API's GetUserListAsync method.
        """
        return await self._api.get_user_list().configure_await(False)

    async def groups_archive(self, channel_id, cancellation_token):
        """
            Wraps Slack API's GroupsArchiveAsync method.
        """
        return await self._api.groups_archive(channel_id).configure_await(False)

    async def test_auth(self, cancellation_token):
        auth = await self._api.test_auth().configure_await(False)
        return auth.user_id

    async def login_with_slack(self, cancellation_token):
        if not self.options.SlackBotToken:
            identity = await self.test_auth(cancellation_token).configure_await(False)
        elif not self.options.SlackClientId or not\
                self.options.SlackClientSecret or not\
                self.options.SlackRedirectUri or\
                len(self.options.SlackScopes) == 0:
            raise Exception('Missing Slack API credentials! Provide SlackClientId, SlackClientSecret, scopes and'
                            ' SlackRedirectUri as part of the SlackAdapter options.')