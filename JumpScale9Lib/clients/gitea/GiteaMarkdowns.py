from js9 import j

from .GiteaMarkdownsNonRaw import GiteaMarkdownsNonRaw
from .GiteaMarkdownsRaw import GiteaMarkdownsRaw

JSBASE = j.application.jsbase_get_class()


class GiteaMarkdowns():
    def __init__(self, client):
        JSBASE.__init__(self)
        self.client = client

    @property
    def markdown(self):
        return GiteaMarkdownsNonRaw(self.client)

    @property
    def raw(self):
        return GiteaMarkdownsRaw(self.client)
