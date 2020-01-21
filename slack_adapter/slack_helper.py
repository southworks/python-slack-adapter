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
        """ Formats a BotBuilder activity into an outgoing Slack message.
        Args:
            Activity activity: A BotBuilder Activity object.
        Returns:
            A Slack message object with {text, attachments, channel, thread ts}
            as well as any fields found in activity.channelData.
        """
        attachments = []

        if not activity:
            raise Exception(activity.name)

        message = NewSlackMessage()
        if not activity.timestamp:
            # TODO: Property time_stamp cannot be set
            message.time_stamp = activity.timestamp

        # TODO: Property text cannot be set
        message.text = activity.text

        if activity.attachments:
            # TODO: Define a class that is similar to SlackAPI.Attachment (.net)
            """ 
            namespace SlackAPI
            {
                public class Attachment
                {
                    public string callback_id;
                    public string footer;
                    public AttachmentAction[] actions;
                    public string[] mrkdwn_in;
                    public string thumb_url;
                    public string image_url;
                    public IBlock[] blocks;
                    public Field[] fields;
                    public string footer_icon;
                    public string text;
                    public string title;
                    public string author_icon;
                    public string author_link;
                    public string author_name;
                    public string pretext;
                    public string color;
                    public string fallback;
                    public string title_link;
            
                    public Attachment();
                }
            }
            """
            # attachments: List[type] = list()
            attachments = list()

            for att in activity.attachments:
                if att.name == 'blocks':
                    message.blocks = [att.content]
                else:
                    new_attachment = Object(author_name= att.name, thumb_url=att.thumbnail_url)

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

        # TODO: Review values
        new_conversation_account = ConversationAccount()
        new_channel_account_from = ChannelAccount()
        new_channel_account_recipient = ChannelAccount()

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
