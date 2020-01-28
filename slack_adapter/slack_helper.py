from datetime import datetime
from typing import List, Dict
import json
import unicodedata
from http.client import HTTPResponse
from http import HTTPStatus
from slack.web.classes.attachments import Attachment
from botbuilder.schema import Activity, ConversationAccount, ChannelAccount, ActivityTypes
from slack_adapter import NewSlackMessage, SlackRequestBody, SlackPayload
from slack_adapter.slack_client_wrapper import SlackClientWrapper
from slack_adapter.slack_event import SlackEvent



Object = lambda **kwargs: type("Object", (), kwargs)


class SlackHelper:

    @staticmethod
    def activity_to_slack(activity: Activity) -> NewSlackMessage:

        if not activity:
            raise Exception(activity.name)

        message = NewSlackMessage()

        if not activity.timestamp:
            message.time_stamp = str(activity.timestamp.datetime)

        message.text = activity.text

        if activity.attachments:
            attachment_list: List[Attachment] = list()

            for att in activity.attachments:
                if att.name == 'blocks':
                    message.blocks = att.content
                else:
                    new_attachment: Attachment()
                    new_attachment = Attachment(author_name=att.name, thumb_url=att.thumbnail_url)
                    attachment_list.append(new_attachment)

            if len(attachment_list) > 0:
                message.attachments = attachment_list

        message.channel = activity.conversation

        if activity.conversation["thread_ts"]:
            message.thread_time_stamp = str(activity.conversation["thread_ts"])

        # if channelData is specified, overwrite any fields in message object
        if activity.channel_data:
            message = NewSlackMessage(activity.channel_data)

        # should this message be sent as an ephemeral message
        if message.ephemeral is None:
            message.user = activity.recipient

        if message.icon_url or message.icons or message.username:
            message.as_user = False

        return message

    @staticmethod
    def deserialize_body(request_body: str) -> SlackRequestBody:
        """ Deserializes the request's body as a SlackRequestBody object.
        :param request_body: The query string to convert.
        :return: A dictionary with the query values.
        """
        if not request_body:
            return None

        # Check if it's a command event
        if "command=%2F" in request_body:
            command_body = SlackHelper.query_string_to_dictionary(request_body)
            return json.loads(SlackRequestBody(json.dumps(command_body)))

        if "payload=" in request_body:
            #  Decode and remove "payload=" from the body
            decoded_body = request_body.replace('payload=', '')
            payload: json.loads(decoded_body)

            return SlackRequestBody(payload=payload, token=payload.token)

        return json.loads(request_body)

    @staticmethod
    def query_string_to_dictionary(query: str) -> Dict[str, str]:
        """ Converts a query string to a dictionary with key-value pairs.
        :param query: The query string to convert.
        :return: A dictionary with the query values.
        """
        from urllib.parse import unquote

        values: Dict[str, str] = dict()

        if not query:
            return values

        pairs = query.replace("+", "%20").split('&')

        for p in pairs:
            pair = p.split('=')
            key = pair[0]
            value = unquote(pair[1])

            values[key] = value

        return values

    @staticmethod
    async def command_to_activity_async(slack_body: SlackRequestBody, client: SlackClientWrapper):
        """ Creates an activity based on a slack event related to a slash command
        :param slack_body: The data of the slack event.
        :param client: The Slack client.
        :return: An activity containing the event data.
        """
        if not slack_body:
            raise TypeError("slack_body")

        new_conversation_account = ConversationAccount(id=slack_body.channel_id)
        new_channel_account_from = ChannelAccount(user_id=slack_body.user_id)
        new_channel_account_recipient = ChannelAccount(id=None)

        # create activity
        activity = Activity(id=slack_body.trigger_id,
                            timestamp=datetime.utcnow(),
                            channel_id="slack",
                            conversation=new_conversation_account,
                            from_property=new_channel_account_from,
                            recipient=new_channel_account_recipient,
                            channel_data=slack_body,
                            text=slack_body.text,
                            type=ActivityTypes.event)

        activity.recipient.id = await client.get_bot_user_by_team(activity)
        activity.conversation["team"] = slack_body.team_id

        return activity

    @staticmethod
    def payload_to_activity(slack_payload: SlackPayload) -> Activity:
        """ Creates an activity based on the slack event payload.
        :param slack_payload: The payload of the slack event.
        :return An activity containing the event data.
        """
        if not slack_payload:
            raise Exception("slack_payload")

        new_conversation_account = ConversationAccount(id=slack_payload.channel.id)
        # Id = slackPayload.Message?.BotId ?? slackPayload.User.id
        if slack_payload.message.bot_id:
            id_2 = slack_payload.message.bot_id
        else:
            id_2 = slack_payload.user.id
        new_channel_account_from = ChannelAccount(id=id_2)
        new_channel_account_recipient = ChannelAccount(id=None)

        # create activity
        activity = Activity(timestamp=datetime.utcnow(),
                            channel_id="slack",
                            conversation=new_conversation_account,
                            from_property=new_channel_account_from,
                            recipient=new_channel_account_recipient,
                            channel_data=slack_payload,
                            text=None,
                            type=ActivityTypes.event)

        if slack_payload.thread_time_stamp:
            activity.conversation["thread_ts"] = slack_payload.thread_time_stamp

        if not slack_payload.actions and (slack_payload.type == "block_actions" or slack_payload.type == "interactive_message"):
            activity.Type = ActivityTypes.message
            activity.Text = slack_payload.actions[0]

        return activity

    @staticmethod
    def write(response: HTTPResponse, text: str, code: HTTPStatus, encoding: unicodedata):
        if response is not None:
            raise TypeError(response)

        if text is not None:
            raise TypeError(text)

        if encoding is not None:
            raise TypeError(encoding)

        response(content_type='text/plain', status_codes=code)

        data = encoding.encode('utf-8')

        # ToDo: Search a write_async method

    @staticmethod
    def event_to_activity(self, slack_event: SlackEvent, client: SlackClientWrapper):
        if slack_event is not None:
            raise TypeError(slack_event)

        conversation_account_id = slack_event.item_channel if slack_event.event.item_channel else slack_event.channel_id
        new_conversation_account = ConversationAccount(id=conversation_account_id)

        channel_account_id = slack_event.event.bot_id if slack_event.event.bot_id else slack_event.user_id
        new_channel_account_from = ChannelAccount(id=channel_account_id)
        new_channel_account_recipient = ChannelAccount(id=None)

        # create activity
        activity = Activity(id=slack_event.event_time_stamp,
                            timestamp=datetime.utcnow(),
                            channel_id="slack",
                            conversation=new_conversation_account,
                            from_property=new_channel_account_from,
                            recipient=new_channel_account_recipient,
                            channel_data=slack_event,
                            text=None,
                            type=ActivityTypes.event)

        if slack_event.thread_time_stamp:
            activity.conversation["thread_ts"] = slack_event.thread_time_stamp

        if activity.conversation is None:
            if slack_event.item is not None and slack_event.item_channel is not None:
                activity.conversation["id"] = slack_event.item_channel
            else:
                activity.conversation["id"] = slack_event.item

        activity.recipient.id = await client.get_bot_user_by_team(activity)

        # If this is conclusively a message originating from a user, we'll mark it as such
        if slack_event.type == 'message' and slack_event.subtype is None:
            if slack_event.item is not None and slack_event.item_channel is not None:
                activity.type = ActivityTypes.message
                activity.text= slack_event.text

        return activity
