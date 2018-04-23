from js9 import j
from datetime import datetime
import calendar

JSBASE = j.application.jsbase_get_class()


class GiteaOrgHook(JSBASE):
    def __init__(self):
        JSBASE.__init__(self)



    def new(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def save(self, update=False, delete=False):
        pass

    def validate(self, update=False, delete=False):
        pass

    def __repr__(self):
        return "users: "

    __str__ = __repr__
