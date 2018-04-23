from js9 import j

from .GiteaOrgHook import GiteaOrgHook

JSBASE = j.application.jsbase_get_class()


class GiteaOrgHooks(JSBASE):
    def __init__(self, organization):
        JSBASE.__init__(self)
        self.organization = organization

    def new(self):
        return GiteaOrgHook()

    __str__ = __repr__ = lambda self: "Gitea Organization Hook for organization: {0}".format(self.organization.username)
