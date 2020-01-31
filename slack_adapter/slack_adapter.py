from logging import Logger
from typing import List

from botbuilder.core import TurnContext, BotAdapter, Bot
from botbuilder.schema import Activity, ConversationReference, ResourceResponse
from botframework.connector.models import ActivityTypes, ConversationAccount

from slack_adapter import NewSlackMessage, slack_helper
from .activity_resource_response import ActivityResourceResponse
from .slack_client_wrapper import SlackClientWrapper
from .slack_helper import SlackHelper

from http import HTTPStatus
from asyncio import StreamReader

import unicodedata

class SlackAdapter(BotAdapter):

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
        super().__init__()
        self._slack_client = slack_client if slack_client else ValueError(type(slack_client))
        self._logger = logger

    @staticmethod
    def activity_to_slack(activity: Activity):
        channel_id = activity.conversation.id
        thread_time_stamp = activity.conversation.thread_time_stamp

        message = NewSlackMessage(time_stamp=activity.timestamp, text=activity.text, attachments=activity.attachments,
                                  channel=channel_id, thread_time_stamp=thread_time_stamp)

        if message.ephemeral:
            message.user = activity.recipient.id

        if not message.icon_url or message.icons or not message.username:
            message.as_user = False

        return message

    async def send_activities(self, context: TurnContext, activities: List[Activity]) -> List[ResourceResponse]:
        if context is None:
            ValueError(type(context))

        if activities is None:
            ValueError(type(activities))

        responses : List[ResourceResponse] = list()

        for activity in activities:
            if type(activity) != ActivityTypes.Message:
                self._logger.propagate(f'Unsupported Activity Type: {activity.type}. Only Activities of type ‘Message’ are supported.')

        message = slack_helper.activity_to_slack(activity)

        slack_response = await self._slack_client.post_message(message)

        if slack_response is None and slack_response.ok:
            resource_response = ActivityResourceResponse()
            resource_response.id = slack_response.time_stamp
            resource_response.activity_id = slack_response.time_stamp

            conversation = ConversationAccount()
            conversation.conversation_id = slack_response.channel,

            responses.append(resource_response)

        return responses

    async def update_activity(self, turn_context: TurnContext, activity: Activity):
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

        message = SlackHelper.activity_to_slack();

        results = await self._slack_client.update(message.time_stamp, message.channel, message.text)

        if results is None:
            raise Exception(f'Error updating activity on Slack:{results}')

        resource_response = ResourceResponse()
        resource_response.id = activity.id

        return resource_response

    async def delete_activity(self, turn_context: TurnContext, reference: ConversationReference):
        if turn_context is None:
            ValueError(type(turn_context))

        if reference is None:
            ValueError(type(reference))

        if reference.channel_id is None:
            ValueError(type(reference.channel_id))

        if turn_context.activity.timestamp is None:
            ValueError(type(turn_context.activity.timestamp))

        await self._slack_client.delete_message(reference.channel_id, turn_context.activity.timestamp.datetime)

    @staticmethod
    async def process(self, request, response, bot: Bot):
        if request is None:
            ValueError(type(request))

        if response is None:
            ValueError(type(response))

        if bot is None:
            ValueError(type(bot))

        sr = StreamReader(request.body)
        body = sr.read()

        slack_body = SlackHelper.deserialize_body(body)

        if slack_body.type == "url_verification":
            text = slack_body.challenge

            await SlackHelper.write(response, HTTPStatus.OK, text, 'utf-8')
            raise Exception(text)

        if self._slack_client.options.slack_verification_token is not None and slack_body.token != self._slack_client.options.slack_verification_token:
            text = 'Rejected due to mismatched verificationToken:{slackBody}'

            await SlackHelper.write(response, HTTPStatus.FORBIDDEN, text, 'utf-8')

            raise Exception(text)

        activity = Activity

        if slack_body.payload is not None:
            # handle interactive_message callbacks and block_actions
            activity = slack_helper.payload_to_activity(slack_body.payload)
        elif slack_body.type == 'event_callback':
            # this is an event api post
            activity = await SlackHelper.event_to_activity(slack_body.event, self._slack_client)
        elif slack_body.command is not None:
            activity = await SlackHelper.CommandToActivityAsync(slack_body, self._slack_client)
        else:
            raise Exception(f'Unknown Slack event type {slack_body.type}')

        context = TurnContext(self, activity)
        context.turn_state.add("httpStatus", HTTPStatus.OK)

        await BotAdapter.run_pipeline(context, bot.on_turn())

        code = context.turn_state.get("httpStatus")
        status_code = HTTPStatus(code)
        text = context.turn_state.get("httpBody") if context.turn_state.get("httpBody") is not None else None

        await slack_helper.write(response, status_code, text, unicodedata.encoding.encode('utf-8'))
