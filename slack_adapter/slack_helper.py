from datetime import datetime
from typing import List, Dict

import slack
from botbuilder.schema import Activity, ConversationAccount, ChannelAccount, ActivityTypes

from slack_adapter import NewSlackMessage, SlackRequestBody, SlackPayload
from slack_adapter.slack_client_wrapper import SlackClientWrapper

Object = lambda **kwargs: type("Object", (), kwargs)


class SlackHelper:
    @staticmethod
    def activity_to_slack(activity: Activity) -> NewSlackMessage:
        if not activity:
            raise Exception

        message = NewSlackMessage()
        if not activity.timestamp:
            attachments = []

            for att in activity.attachments:
                if att.name == 'blocks':
                    message.blocks = [att.content]
                else:
                    new_attachment = Object(author_name=att.name, thumb_url=att.thumbnail_url)
    @staticmethod
    def payload_to_activity(slack_payload: SlackPayload) -> Activity:
        """ Creates an activity based on the slack event payload.
        :param slack_payload: The payload of the slack event.
        :return An activity containing the event data.
        """
        if not slack_payload:
            raise TypeError("slack_payload")

        new_conversation_account = ConversationAccount(id=slack_payload.channel.id)
        channel_account_id = slack_payload.message.bot_id if slack_payload.message.bot_id else slack_payload.user.id

        new_channel_account_from = ChannelAccount(id=channel_account_id)
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

        if slack_payload.actions and \
                (slack_payload.type == "block_actions" or slack_payload.type == "interactive_message"):
            activity.Type = ActivityTypes.message
            activity.Text = slack_payload.actions[0]

        return activity
        
    @staticmethod
    def command_to_activity_async(slack_body: SlackRequestBody, client: SlackClientWrapper, cancellation_token):
        """ Creates an activity based on a slack event related to a slash command
        :param slack_body: The data of the slack event.
        :param client: The Slack client.
        :param cancellation_token: A cancellation token for the task.
        :return: An activity containing the event data.
        """
        if not slack_body:
            raise Exception("slack_body")

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

        activity.recipient.id = client.get_bot_user_by_team(activity, cancellation_token)
        activity.conversation["team"] = slack_body.team_id

        return activity
