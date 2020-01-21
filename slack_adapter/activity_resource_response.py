from botbuilder.schema import ResourceResponse


class ActivityResourceResponse(ResourceResponse):

    @property
    def activity_id(self):
        return self._activity_id

    @activity_id.setter
    def activity_id(self, activity_id):
        self._activity_id = activity_id

    @property
    def conversation(self):
        return self._conversation

    @conversation.setter
    def conversation(self, conversation):
        self._conversation = conversation

    def __init__(self, activity_id=None, conversation=None):

        self._activity_id = activity_id
        self._conversation = conversation
