from js9 import j

from .GiteaMarkdowns import GiteaMarkdowns
from .GiteaRepos import GiteaRepos
from .GiteaOrgs import GiteaOrgs
from .GiteaAdmin import GiteaAdmin
from .GiteaVersion import GiteaVersion

from JumpScale9Lib.clients.gitea.client import Client


TEMPLATE = """
url = ""
gitea_token_ = ""
"""

JSConfigBase = j.tools.configmanager.base_class_config
JSBASE = j.application.jsbase_get_class()


class GiteaClient(JSConfigBase):

    def __init__(self, instance, data={}, parent=None,interactive=False):
        JSConfigBase.__init__(self, instance=instance, data=data, parent=parent, template=TEMPLATE,interactive=interactive)
        self._api = None

    def config_check(self):
        """
        check the configuration if not what you want the class will barf & show you where it went wrong
        """

        if self.config.data["url"] == "" or self.config.data["gitea_token_"] == "":
            return "url and gitea_token_ are not properly configured, cannot be empty"

        base_uri = self.config.data["url"]
        if "/api" not in base_uri:
            self.config.data_set("url", "%s/api/v1" % base_uri)
            self.config.save()

        # TODO:*1 need to do more checks that url is properly formated

    @property
    def api(self):
        if not self._api:
            self._api = Client(base_uri=self.config.data["url"])
            self._api.security_schemes.passthrough_client_token.set_authorization_header(
                'token {}'.format(self.config.data["gitea_token_"]))
        return self._api

    @property
    def version(self):
        return GiteaVersion(self).get()

    @property
    def admin(self):
        return GiteaAdmin(self)

    @property
    def markdowns(self):
        return GiteaMarkdowns(self)

    @property
    def orgs(self):
        return GiteaOrgs(self)

    @property
    def repos(self):
        return GiteaRepos(self)

    def __repr__(self):
        return "gitea client"

    __str__ = __repr__
