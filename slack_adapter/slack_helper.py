from datetime import datetime
from typing import List, Dict
import json
import unicodedata
from http.client import HTTPResponse
from http import HTTPStatus
from slack.web.classes.attachments import Attachment
from requests import status_codes
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
                    new_attachment = Object(author_name=att.name, thumb_url=att.thumbnail_url)
    
    @staticmethod
    def payload_to_activity(slack_payload: SlackPayload) -> Activity:
        """ Creates an activity based on the slack event payload.
        :param slack_payload: The payload of the slack event.
        :return An activity containing the event data.
        """
        if not slack_payload:
            raise Exception("slack_payload")

        new_conversation_account = ConversationAccount(id=slack_payload.channel.id)
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
    async def command_to_activity_async(slack_body: SlackRequestBody, client: SlackClientWrapper, cancellation_token):
        """ Creates an activity based on a slack event related to a slash command
        :param slack_body: The data of the slack event.
        :param client: The Slack client.
        :param cancellation_token: A cancellation token for the task.
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

        activity.recipient.id = await client.get_bot_user_by_team(activity, cancellation_token)
        activity.conversation["team"] = slack_body.team_id

        return activity


    @staticmethod
    def write(response: HTTPResponse, text: str, code: HTTPStatus, encoding: unicodedata, cancellation_token):
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
    def event_to_activity(self, slack_event: SlackEvent, client: SlackClientWrapper, cancellation_token):
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

        activity.recipient.id = await client.get_bot_user_by_team(activity, cancellation_token)

        # If this is conclusively a message originating from a user, we'll mark it as such
        if slack_event.type == 'message' and slack_event.subtype is None:
            if slack_event.item is not None and slack_event.item_channel is not None:
                activity.type = ActivityTypes.message
                activity.text= slack_event.text

        return activity
