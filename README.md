# python-slack-adapter
## Publish a package

### Test env

Right now, the workflow publishes a test package every time a PR is created. Thi worflow takes @Aliandi's credentials, to change them you have to go to the Secrets settings and create them again using the new values.

_NOTE: for this to work, the PR should update the package version on the setup.py file. This being vX.y where X is the version that's being worked on and y would be the feature number_

### Prod env
This is not configured right now. To do so:

1. Set the MANX credentials (saved on 1Password). To do this refer to [this article](https://help.github.com/es/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets)
2. Create a [release](https://help.github.com/en/enterprise/2.16/user/github/administering-a-repository/creating-releases)
3. Done! The workflow should be executed and the new package should be published.

_NOTE: for this to work, the setup.py has to update the version, for example from 1.0 to 2.0._
