class SlackAdapterOptions:
    slackVerificationToken = SlackVerificationToken
    slackBotToken = SlackBotToken
    slackClientSigningSecret = SlackClientSigningSecret

    # ToDo
    # public virtual Task<string> GetBotUserByTeamAsync(string teamId, CancellationToken cancellationToken)