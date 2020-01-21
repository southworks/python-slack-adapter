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

    @staticmethod
    def deserialize_body(request_body: str) -> SlackRequestBody:
        """ Deserializes the request's body as a SlackRequestBody object.
        Args:
            str requestBody: The query string to convert.
        Returns:
            A dictionary with the query values.
        """

        if not request_body:
            return None

        if "command=%2F" in request_body:
            command_body = SlackHelper.query_string_to_dictionary(request_body)
            # TODO: See a replacement for Newtonsoft Json
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
        Args:
            str query: The query string to convert.
        Returns:
            A dictionary with the query values.
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
    def command_to_activity_async(slack_body: SlackRequestBody, client: SlackClientWrapper, cancellation_token):
        """ Creates an activity based on a slack event related to a slash command
        Args:
            slack_body: The data of the slack event.
            client: The Slack client.
            cancellation_token: A cancellation token for the task.
        Returns: An activity containing the event data.
        """
        if not slack_body:
            # TODO: Mimic .net intention using
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
                            type="event")

        activity.recipient.id = client.get_bot_user_by_team(activity, cancellation_token)
        activity.conversation["team"] = slack_body.team_id

        return activity
