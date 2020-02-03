import struct
import json
from .file_types import FileTypes
from botbuilder.schema import Activity
from .slack_adapter_options import SlackAdapterOptions
from .presence import Presence
from slack_adapter import NewSlackMessage
import slack
import http.client
from multipledispatch import dispatch
import unicodedata
import hmac
import hashlib


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

            :param options: An object containing API credentials, a webhook verification token and other options.
        """
        self._options = options if options else ValueError(type(options))
        if not options.slack_verification_token and not options.slack_client_sign_in_secret:
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
        self._api = slack.WebClient(options.slack_bot_token)
        # self.login_with_slack(default).wait()

    async def add_reaction(self, name=None, channel=None, time_stamp=None, cancellation_token=None):
        """
            Wraps Slack API's AddReactionAsync method.
            @param name: The optional name.
            @param channel: The optional channel.
            @param time_stamp: The optional timestamp.
            @param cancellation_token: A cancellation token for the task.
            @rtype: SlackResponse
            @returns: The SlackResponse representing the response to the reaction added.
        """
        return await self._api.reactions_add(name=name)

    async def api_request_with_token(self, cancellation_token=None, *post_parameters):
        """
            Wraps Slack API's APIRequestWithTokenAsync method.
            @param cancellation_token: A cancellation token for the task.
            @param post_parameters: The parameters to the POST request.
            @rtype: SlackResponse
            @returns: The SlackResponse representing the response to the reaction added.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.API_request_with_token(post_parameters).configure_await(False) \
            if not post_parameters else \
            await self._api.API_request_with_token().configure_await(False)

    async def channels_set_topic(self, channel_id, new_topic, cancellation_token):
        """
            Wraps Slack API's ChannelSetTopicAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.channels_setTopic(channel=channel_id, topic=new_topic)

    async def channel_is_invite(self, user_id, channel_id, cancellation_token):
        """
            Wraps Slack API's ChannelsInviteAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.channels_invite(channel=channel_id, user=user_id)

    async def connect(self, cancellation_token):
        """
            Wraps Slack API's ConnectAsync method.
        """
        return await self._api.rtm_connect()

    async def delete_message(self, channel_id, ts, cancellation_token):
        """
            Wraps Slack API's DeleteMessageAsync method.
            @param channel_id: The channel to delete the message from.
            @param ts: The timestamp of the message.
            @param cancellation_token: A cancellation token for the task.
            @rtype: SlackResponse
            @returns: The SlackResponse to the posting operation.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.chat_delete(channel_id, ts)

    async def dialog_open(self, trigger_id, dialog, cancellation_token):
        """
            Wraps Slack API's DialogOpenAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.dialog_open(dialog=dialog, trigger_id=trigger_id)

    async def emit_login(self, agent='Inumedia.SlackAPI', cancellation_token=None):
        """
            Wraps Slack API's EmitLoginAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.emit_login(agent).configure_await(False)

    async def emit_presence(self, status: Presence, cancellation_token):
        """
            Wraps Slack API's EmitPresence method.
        """
        # ToDo check what should be pass to the signature
        return await self._api.users_setPresence(presence=status)

    async def get_channel_history(self, channel_info, latest=None, oldest=None, count=0, cancellation_token=None):
        """
            Wraps Slack API's GetChannelHistoryAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.channels_history(channel=channel_info)

    async def get_channel_list(self, cancellation_token=None):
        """
            Wraps Slack API's GetChannelListAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.channels_list()

    async def get_counts(self, cancellation_token):
        """
            Wraps Slack API's GetCountsAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.get_counts()

    async def get_direct_message_history(self, conversation_info, latest, oldest, count, cancellation_token):
        """
            Wraps Slack API's GetDirectMessageHistoryAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.get_direct_message_history(conversation_info, latest, oldest, count)

    async def get_direct_message_list(self, cancellation_token):
        """
            Wraps Slack API's GetDirectMessageListAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.get_direct_message_list()

    async def get_file_info(self, file_id, page=None, count=None, cancellation_token=None):
        """
            Wraps Slack API's GetFileInfoAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.files_info(file=file_id)

    async def get_files(self, user_id=None, date_from=None, date_to=None, count=None, page=None, types=FileTypes.All,
                        cancellation_token=None):
        """
            Wraps Slack API's GetFilesAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.search_files(query=page)

    async def get_group_history(self, group_info, latest=None, oldest=None, count=None, cancellation_token=None):
        """
            Wraps Slack API's GetGroupHistoryAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.groups_history(channel=group_info)

    async def get_groups_list(self, exclude_archived=True, cancellation_token=None):
        """
            Wraps Slack API's GetGroupsListAsync method.
        """
        return await self._api.groups_list()

    async def get_preferences(self, cancellation_token):
        """
            Wraps Slack API's GetPreferencesAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.get_preferences().configure_await(False)

    async def get_stars(self, user_id=None, count=None, page=None, cancellation_token=None):
        """
            Wraps Slack API's GetStarsAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.stars_list()

    async def get_user_list(self, cancellation_token):
        """
            Wraps Slack API's GetUserListAsync method.
        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.users_list()

    async def groups_archive(self, channel_id, cancellation_token):
        """
            Wraps Slack API's GroupsArchiveAsync method.
        """
        # ToDo: Check method's signature variables
        return await self._api.groups_archive(channel=channel_id)

    async def groups_close(self, channel_id, cancellation_token):
        """
            Wraps Slack API's GroupsCloseAsync method.
        """
        return await self._api.groups_close(channel_id).configure_await(False)

    async def groups_create(self, name):
        """
            Wraps Slack API's GroupsCreateAsync method.
        """
        return await self._api.groups_create(name=name)

    async def groups_create_child(self, channel_id):
        """

        """
        return await self._api.groups_createChild(channel=channel_id)

    async def groups_invite(self, channel, user):
        """

        """
        return await self._api.groups_invite(channel=channel, user=user)

    async def groups_kick(self, channel, user):
        """

        """
        return await self._api.groups_kick(channel=channel, user=user)

    async def groups_leave(self, channel):
        """

        """
        return await self._api.groups_leave(channel=channel)

    async def groups_mark(self, channel, ts):
        """

        """
        return await self._api.groups_mark(channel=channel, ts=ts)

    async def groups_open(self, channel):
        """

        """
        return await self._api.groups_open(channel=channel)

    async def groups_rename(self, channel, name):
        """

        """
        return await self._api.groups_rename(channel=channel, name=name)

    async def groups_set_purpose(self, channel, purpose):
        """

        """
        return await self._api.groups_setPurpose(channel=channel, purpose=purpose)

    async def groups_set_topic(self, channel, topic):
        """

        """
        return await self._api.groups_setTopic(channel=channel, topic=topic)

    async def groups_unarchive(self, channel):
        """

        """
        return await self._api.groups_unarchive(channel=channel)

    async def join_direct_message_channel(self):
        """

        """
        # ToDo: look for this method's equivalent in slack client por Python
        return await self._api.JoinDirectMessageChannelAsync()

    async def mark_channel(self, channel, ts):
        """

        """
        return await self._api.channels_mark(channel=channel, ts=ts)

    async def post_ephemeral_message(self, channel, user):
        """

        """
        # ToDo: look for this method's equivalent in slack client for Python
        return await self._api.chat_postEphemeral(channel=channel, user=user)

    @dispatch(str, str, str, str, bool, )
    async def post_message(self, channel_id: str, text: str, bot_name: str, parse: str, link_names: bool, blocks,
                           attachments, unfurl_links: bool, icon_url, icon_emoji, as_user: bool, cancellation_token):
        """
            Wraps Slack API's PostMessageAsync method.
            @param channel_id: The channel id.
            @param text: The text of the message.
            @param bot_name: The bot name.
            @param parse: Change how messages are treated.
            @param link_names: If to find and link channel names and username.
            @param blocks: A JSON-based array of structured blocks, presented as a URL-encoded string.
            @param attachments: The attachments, if any.
            @param unfurl_links: True to enable unfurling of primarily text-based content.
            @param icon_url: The url of the icon with the message, if any.
            @param icon_emoji: The emoji icon, if any.
            @param as_user: If the message is being sent as user instead of as a bot.
            @param cancellation_token: A cancellation token for the task.
            @rtype: SlackResponse
            @returns: The SlackResponse to the posting operation.
        """
        return await self._api.chat_postMessage(channel=channel_id, text=text, bot_name=bot_name, parse=parse,
                                                link_names=link_names, blocks=blocks, attachments=attachments,
                                                unfurl_links=unfurl_links, icon_url=icon_url, icon_emoji=icon_emoji,
                                                as_user=as_user, cancellation_token=cancellation_token)

    @dispatch(object, str)
    async def post_message(self, message: NewSlackMessage, cancellation_token: str):
        """
            Wraps Slack API's PostMessageAsync method.
            @param message: The channel id.
            @param cancellation_token: A cancellation token for the task.
            @rtype: SlackResponse
            @returns: The SlackResponse to the posting operation.
        """
        if message is None:
            return None

        data = dict([
            ('token', self.options.slack_bot_token),
            ('channel', message.channel),
            ('text', message.text),
            ('thread_ts', message.thread_time_stamp),
        ])

        if message.blocks is not None:
            data["blocks"] = json.dumps(message.blocks)

        if message.ephemeral is not None:
            url = self.post_ephemeral_message_url
        else:
            url = self.post_message_url

        conn = http.client.HTTPConnection(url)
        response = conn.request("POST", data)

        return json.loads(response)

    async def search_all(self, query):
        """

        """
        return await self._api.search_all(query=query)

    async def search_files(self, query):
        """

        """
        return await self._api.search_files(query=query)

    async def search_messages(self, query):
        """

        """
        return await self._api.search_messages(query=query)

    async def test_auth(self, cancellation_token):
        """

        """
        return await self._api.auth_test().user_id

    async def update(self, ts: str, channel_id: str, text: str = '', bot_name: str = '', parse: str = '',
                     link_names: bool = False, attachments=None, as_user: bool = False):
        """
            Wraps Slack API's UpdateAsync method
            @param ts: The timestamp of the message.
            @param channel_id: The channel to delete the message from.
            @param text: The text to update with.
            @param bot_name: The optional bot name.
            @param parse: Change how messages are treated.Defaults to 'none'.
            @param link_names: f to find and link channel names and username.
            @param attachments: The attachments, if any.
            @param as_user: If the message is being sent as user instead of as a bot.
            @param cancellation_token: A cancellation token for the task.
            @rtype: SlackResponse
            @returns: The SlackResponse to the posting operation.
        """
        return await self._api.chat_update(channel='', ts=ts, channel_id=channel_id, bot_name=bot_name, parse=parse,
                                           link_names=link_names, attachments=attachments, as_user=as_user)

    async def upload_file(self, file, content):
        """

        """
        return await self._api.files_upload(file=file, content=content)

    async def get_bot_user_by_team(self, activity: Activity, cancellation_token):
        if self.identity:
            return self.identity
        if not activity.conversation["team"]:
            return None
        # multi-team mode
        user_id = await self.options.get_bot_user_by_team(str(activity.conversation["team"]), cancellation_token)
        return user_id if not user_id else Exception('Missing credentials for team.')

    @staticmethod
    def verify_signature(self, request, body):
        if not request or not body:
            return False

        time_stamp = request.Headers["X-Slack-Request-Timestamp"]
        signature = ['v0=', str(time_stamp), body]
        base_str = str.join(':', signature)

        # Todo: Research how to port Bit Converter

        first_hmac = hmac.new(self.options.slack_client_secret.encode('UTF-8'))
        hash_array = first_hmac.digest_size(base_str.encode('UTF-8'))
        new_hash = ("v0=" + bytearray(hash_array).hex()).upper()
        retrieved_signature = request.Headers["X-Slack-Signature"].str().upper()
        return new_hash == retrieved_signature

    async def login_with_slack(self, cancellation_token):
        if not self.options.slack_bot_token:
            identity = await self.test_auth(cancellation_token)
        elif not self.options.slack_client_id or not \
                self.options.slack_client_secret or not \
                self.options.slack_redirect_uri or \
                len(self.options.slack_scopes) == 0:
            raise Exception('Missing Slack API credentials! Provide SlackClientId, SlackClientSecret, scopes and'
                            ' SlackRedirectUri as part of the SlackAdapter options.')
