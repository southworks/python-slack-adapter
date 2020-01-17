from typing import List
from botbuilder.schema import Activity, ConversationReference, ResourceResponse
from botbuilder.core import TurnContext
from botframework.connector.models import ActivityTypes, ConversationAccount
from .activity_resource_response import ActivityResourceResponse
from .slack_client_wrapper import SlackClientWrapper
from .slack_helper import SlackHelper
from slack_adapter import NewSlackMessage
from logging import Logger

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
    def slack_client(self) -> SlackClientWrapper:
        return self._slack_client

    @property
    def logger(self):
        return self._logger

    # def __init__(self, options):
    #     self._slack = slack.web

    def __init__(self, slack_client: SlackClientWrapper, logger: Logger):
        self._slack_client = slack_client if slack_client else ValueError(type(slack_client))
        self._logger = logger

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

    #def continue_conversation(self, reference: ConversationReference):

    async def send_activities(self, turn_context: TurnContext, activities: list[Activity], cancellation_token):
        if turn_context is None:
            ValueError(type(turn_context))

        if activities is None:
            ValueError(type(activities))

        responses : List[ResourceResponse] = list()

        for activity in activities:
            if type(activity) != ActivityTypes.Message:
                self._logger.propagate(f'Unsupported Activity Type: {activity.type}. Only Activities of type ‘Message’ are supported.')

        message = slack_helper.activity_to_slack(activity)

        slack_response = await self._slack_client.post_message(message, cancellation_token)

        if slack_response is None and slack_response.ok:
            resource_response = ActivityResourceResponse()
            resource_response.id = slack_response.time_stamp
            resource_response.activity_id = slack_response.time_stamp

            conversation = ConversationAccount()
            conversation.conversation_id = slack_response.channel,

            responses.append(resource_response)

        return responses


    async def update_activity(self, turn_context: TurnContext, activity: Activity, cancellation_token):
        if turn_context is None:
            ValueError(type(turn_context))

        if activity is None:
            ValueError(type(activity))

        if activity.id is None:
            ValueError(type(activity.id))

        if activity.id is None:
            ValueError(type(activity.timestamp))

        if activity.conversation is None:
            ValueError(type(activity.channel_id))

        message = Sla

    def delete_activity(self, turn_context: TurnContext, reference: ConversationReference):