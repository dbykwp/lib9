from js9 import j

from .GiteaMarkdownRaw import GiteaMarkdownRaw

JSBASE = j.application.jsbase_get_class()


class GiteaMarkdownsRaw():
    def __init__(self, client):
        JSBASE.__init__(self)
        self.client = client

    def new(self):
        return  GiteaMarkdownRaw(self.client)
