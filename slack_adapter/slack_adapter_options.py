class SlackAdapterOptions:

    def get_bot_user_by_team(self, team_id, cancellation_token):
        raise NotImplementedError

    def get_token_for_team(self, team_id, cancellation_token):
        raise NotImplementedError

    @property
    def __options(self):
        return self._options

    @property
    def __identity(self):
        return self._identity

    @property
    def name(self):
        return 'Slack Adapter Options'

    @property
    def middlewares(self):
        return self._middlewares

    @property
    def slack_bot_token(self):
        return self._slack_bot_token

    @slack_bot_token.setter
    def slack_bot_token(self, slack_bot_token):
        self._slack_bot_token = slack_bot_token

    @property
    def slack_client_id(self):
        return self._slack_client_id

    @slack_client_id.setter
    def slack_client_id(self, slack_client_id):
        self._slack_client_id = slack_client_id

    @property
    def slack_client_secret(self):
        return self._slack_client_secret

    @slack_client_secret.setter
    def slack_client_secret(self, slack_client_secret):
        self._slack_client_secret = slack_client_secret

    @property
    def slack_client_sign_in_secret(self):
        return self._slack_client_sign_in_secret

    @slack_client_sign_in_secret.setter
    def slack_client_sign_in_secret(self, slack_client_sign_in_secret):
        self._slack_client_sign_in_secret = slack_client_sign_in_secret

    @property
    def slack_redirect_uri(self):
        return self._slack_redirect_uri

    @slack_redirect_uri.setter
    def slack_redirect_uri(self, slack_redirect_uri):
        self._slack_redirect_uri = slack_redirect_uri

    @property
    def slack_verification_token(self):
        return self._slack_verification_token

    @slack_verification_token.setter
    def slack_verification_token(self, slack_verification_token):
        self._slack_verification_token = slack_verification_token

    @property
    def slack_scopes(self):
        return self._slack_scopes

    def __init__(self, slack_bot_token=None, slack_client_id=None, slack_client_secret=None,
                 slack_client_sign_in_secret=None, slack_redirect_uri=None, slack_verification_token=None):
        self._slack_bot_token = slack_bot_token
        self._slack_client_id = slack_client_id
        self._slack_client_secret = slack_client_secret
        self._slack_client_sign_in_secret = slack_client_sign_in_secret
        self.slack_redirect_uri = slack_redirect_uri
        self._slack_verification_token = slack_verification_token
