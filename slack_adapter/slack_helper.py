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
            message.time_stamp = activity.timestamp

        message.text = activity.text

        if activity.attachments:
            # attachments: List[type] = list()
            # self.item_list: List[Item] = list()
            attachments = list()

            for att in activity.attachments:
                if att.name == 'blocks':
                    message.blocks = [att.content]
                else:
                    new_attachment = Object(author_name=att.name, thumb_url=att.thumbnail_url)
                    attachments.append(new_attachment)

            if len(attachments) > 0:
                message.attachments = attachments

        message.channel = activity.conversation.id

        if activity.conversation["thread_ts"]:
            message.thread_time_stamp = str(activity.conversation["thread_ts"])

        # if channelData is specified, overwrite any fields in message object
        if activity.channel_data:
            message = activity.channel_data

        # should this message be sent as an ephemeral message
        if message.ephemeral:
            message.user = activity.recipient.id

        if message.icon_url or message.icons or message.username:
            message.as_user = False

        return message
