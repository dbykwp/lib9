import requests
from js9 import j

from .GiteaRepo import GiteaRepo

JSBASE = j.application.jsbase_get_class()


class GiteaRepos(JSBASE):

    def __init__(self, user):
        JSBASE.__init__(self)
        self.user = user

    def new(self):
        return GiteaRepo(self.user)

    __str__ = __repr__ = lambda self: "Gitea Repos for user: {0}".format(self.user.username)
