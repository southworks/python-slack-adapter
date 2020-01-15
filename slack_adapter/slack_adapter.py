from typing import List
from botbuilder.schema import Activity, ConversationReference, ResourceResponse
from botbuilder.core import TurnContext
from botframework.connector.models import ActivityTypes, ConversationAccount
from .activity_resource_response import ActivityResourceResponse
from .slack_client_wrapper import SlackClientWrapper
from slack_adapter import NewSlackMessage, slack_helper


class SlackAdapter:
    @property
    def __options(self):
        return self._options

    @property
    def __slack(self):
        return self._slack

    @property
    def __identity(self):
        return self._identity

    @property
    def name(self):
        return 'Slack Adapter'

    @property
    def middlewares(self):
        return self._middlewares

    @property
    def slack_client(self):
        return self._slack_client

    # def __init__(self, options):
    #     self._slack = slack.web

    def __init__(self, slack_client: SlackClientWrapper):
        self._slack_client = slack_client if slack_client else ValueError(type(slack_client))

    @staticmethod
    def activity_to_slack(activity:Activity):
        channel_id = activity.conversation.id
        thread_time_stamp = activity.conversation.thread_time_stamp

        message = NewSlackMessage(time_stamp=activity.timestamp, text=activity.text, attachments=activity.attachments,
                                  channel=channel_id, thread_time_stamp=thread_time_stamp)

        if message.ephemeral:
            message.user = activity.recipient.id

        if not message.icon_url or message.icons or not message.username:
            message.as_user = False

        return message

    def continue_conversation(self, reference: ConversationReference):

    async def send_activities(self, turn_context: TurnContext, activities: list[Activity]):
        if turn_context is None:
            ValueError(type(turn_context))

        if activities is None:
            ValueError(type(activities))

        responses : List[ResourceResponse] = list()

        for activity in activities:
            if type(activity) != ActivityTypes.Message:
                ValueError("Unsupported Activity Type. Only Activities of type ‘Message’ are supported.", type(activities))

        message = slack_helper.activity_to_slack(activity)

        # ToDo
        slack_response = await _slackClient.PostMessageAsync(message, cancellationToken).ConfigureAwait(false)

        if slack_response is None and slack_response.Ok:
            resource_response = ActivityResourceResponse()

        id = slack_response.Ts
        activity_id = slack_response.Ts
        conversation = ConversationAccount()

        id = slack_response.Channel,

        responses.append(resource_response)

        return responses.ToArray()

    def update_activity(self, turn_context: TurnContext, activity: Activity):

    def delete_activity(self, turn_context: TurnContext, reference: ConversationReference):