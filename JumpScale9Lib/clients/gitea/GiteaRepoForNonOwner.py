import json
from js9 import j

from .GiteaRepo import GiteaRepo

JSBASE = j.application.jsbase_get_class()


class GiteaRepoForNonOwner(GiteaRepo):
    pass
