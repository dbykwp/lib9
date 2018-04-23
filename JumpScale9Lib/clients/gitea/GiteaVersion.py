import requests
from js9 import j


JSBASE = j.application.jsbase_get_class()


class GiteaVersion(JSBASE):

    def __init__(self,client, **kwargs):
        JSBASE.__init__(self)
        self.client = client

    def get(self):
        try:
            res = self.client.api.version.getVersion()
            if res.status_code == 200:
                return res.json()['version']
            j.logger.logger.error('Couldn not fetch API version .. ' + res.content)
        except Exception as e:
            j.logger.logger.error('Couldn not fetch API version .. ' + str(e.args))
        return ''

    def __repr__(self):
        return "API version: %s" % self.get()

    __str__ = __repr__
