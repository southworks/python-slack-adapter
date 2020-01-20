from typing import List

import slack
from botbuilder.schema import Activity

from slack_adapter import NewSlackMessage

Object = lambda **kwargs: type("Object", (), kwargs)


class SlackHelper:

    @staticmethod
    def activity_to_slack(activity: Activity) -> NewSlackMessage:
        """ Formats a BotBuilder activity into an outgoing Slack message.
        :parameters
            Activity activity: A BotBuilder Activity object.
        :returns:
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
                    # TODO: Object definition, what class should it be? SlackAPI.Attachment
                    new_attachment = Object(author_name=att.name, thumb_url=att.thumbnail_url)
                    attachments.append(new_attachment)

            if len(attachments) > 0:
                # TODO: Property attachments cannot be set
                message.attachments = attachments

        # TODO: Property channel cannot be set
        # TODO: Verify that the id field exists
        message.channel = activity.conversation.id

        if activity.conversation["thread_ts"]:
            # TODO: Property thread_time_stamp cannot be set
            message.thread_time_stamp = str(activity.conversation["thread_ts"])

        # if channelData is specified, overwrite any fields in message object
        if activity.channel_data:
            # TODO: Implement activity.GetChannelData()
            message = NewSlackMessage(activity.channel_data)

        # should this message be sent as an ephemeral message
        if message.ephemeral:
            # TODO: Verify that the id field exists
            message.user = activity.recipient.id

        if message.icon_url or message.icons or message.username:
            message.as_user = False

        return message
