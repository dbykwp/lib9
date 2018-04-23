import requests
from js9 import j

from .GiteaPublicKey import GiteaPublicKey

JSBASE = j.application.jsbase_get_class()


class GiteaPublicKeys(JSBASE):

    def __init__(self, user):
        JSBASE.__init__(self)
        self.user = user

    def new(self):
        return GiteaPublicKey(self.user)

    __str__ = __repr__ = lambda self: "Gitea PublicKeys for user: {0}".format(self.user.username)

