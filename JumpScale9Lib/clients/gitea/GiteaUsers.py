from js9 import j

from .GiteaUser import GiteaUser

JSBASE = j.application.jsbase_get_class()


class GiteaUsers(JSBASE):
    def __init__(self,client):
        JSBASE.__init__(self)
        self.client = client

    def new(self):
        return GiteaUser(self.client)

    def __repr__(self):
        return "Gitea users: "

    __str__ = __repr__
