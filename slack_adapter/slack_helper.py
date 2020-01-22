from datetime import datetime
from typing import List, Dict

import slack
from botbuilder.schema import Activity, ConversationAccount, ChannelAccount, ActivityTypes, Attachment

from slack_adapter import NewSlackMessage, SlackRequestBody, SlackPayload
from slack_adapter.slack_client_wrapper import SlackClientWrapper

from slack.web.classes import attachments


Object = lambda **kwargs: type("Object", (), kwargs)


class SlackHelper:

    @staticmethod
    def activity_to_slack(activity: Activity) -> NewSlackMessage:
        # attachments = List[slack.web.classes.attachments.Attachment]

        if not activity:
            raise Exception(activity.name)

        message = NewSlackMessage()

        if not activity.timestamp:
            message.time_stamp = activity.timestamp

        message.text = activity.text

        if activity.attachments:
            attachment_list: List[slack.web.classes.attachments.Attachment] = list()

            for att in activity.attachments:
                if att.name == 'blocks':
                    message.blocks = [att.content]
                else:
                    new_attachment: slack.web.classes.attachments.Attachment
                    new_attachment = slack.web.classes.attachments.Attachment(author_name=att.name, thumb_url=att.thumbnail_url)
                    attachment_list.append(new_attachment)

            if len(attachment_list) > 0:
                message.attachments = attachment_list

        # TODO: Verify that the id field exists
        message.channel = activity.conversation.id

        if activity.conversation["thread_ts"]:
            message.thread_time_stamp = str(activity.conversation["thread_ts"])

        # if channelData is specified, overwrite any fields in message object
        if activity.channel_data:
            # TODO: Implement activity.GetChannelData()
            message = NewSlackMessage(activity.channel_data)

        # should this message be sent as an ephemeral message
        if message.ephemeral:
            message.user = activity.recipient.id

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
            # return JsonConvert.DeserializeObject<SlackRequestBody>(JsonConvert.SerializeObject(command_body));
            # return JsonConvert.DeserializeObject()

        if "payload=" in request_body:
            #  Decode and remove "payload=" from the body
            # decodedBody = Uri.UnescapeDataString(requestBody).Remove(0, 8)

            # TODO: Resolve the Json library issue
            # payload = JsonConvert.DeserializeObject<SlackPayload>(decodedBody);
            payload: SlackPayload

            # TODO: The SlackRequestBody init needs the properties passed below
            return SlackRequestBody(payload=payload, token=payload.token)

        # return JsonConvert.DeserializeObject<SlackRequestBody>(requestBody, new UnixDateTimeConverter())
        return ""

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
