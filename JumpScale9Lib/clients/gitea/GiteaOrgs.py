from js9 import j

from .GiteaOrg import GiteaOrg


JSBASE = j.application.jsbase_get_class()


class GiteaOrgs(JSBASE):
    def __init__(self, user):
        JSBASE.__init__(self)
        self.user = user

    def new(self):
        return GiteaOrg(self.user)

    __str__ = __repr__ = lambda self: "Gitea Organizations for user: {0}".format(self.user.username)
