from js9 import j

from .GiteaMarkdown import GiteaMarkdown

JSBASE = j.application.jsbase_get_class()


class GiteaMarkdownsNonRaw():
    def __init__(self, client):
        JSBASE.__init__(self)
        self.client = client

    def new(self):
        return  GiteaMarkdown(self.client)
