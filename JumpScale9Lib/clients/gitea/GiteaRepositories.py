import requests
from js9 import j

from .GiteaUser import GiteaUser
from .GiteaRepo import GiteaRepo

JSBASE = j.application.jsbase_get_class()


class GiteaRepositories(JSBASE):
    def __init__(self, client, user):
        JSBASE.__init__(self)
        self.user = user
        self.client = client

    def search(self, query, user_id=None, page_number=1, page_size=150, mode="", exclusive=False):
        if page_size > 150 or page_size <= 0:
            page_size = 150

        if mode not in ["fork", "source", "mirror", "collaborative"]:
            return [], 'Only modes allowed [fork, source, mirror, collaborative]'

        result = []
        items = self.user.client.api.repos.repoSearch(
            exclusive=exclusive,
            limit=page_size,
            mode=mode,
            page=page_number,
            uid=user_id,
            q=query
        ).json()

        if not items['ok']:
            return False, ''

        for item in items['data']:
            repo = GiteaRepo(self.user)
            for k, v in item.items():
                setattr(repo, k, v)
            result.append(repo)
        return result

    def migrate(
            self,
            auth_username,
            auth_password,
            clone_addr,
            repo_name,
            uid,
            description='',
            mirror=True,
            private=True
    ):
        d = {
            'auth_username':auth_username,
            'auth_password':auth_password,
            'clone_addr':clone_addr,
            'description':description,
            'mirror':mirror,
            'repo_name':repo_name,
            'uid':uid,
            'private': private
        }
        r = self.user.client.api.repos.repoMigrate(d).json()
        repo = GiteaRepo(self.user)
        for k, v in r.items():
            setattr(repo, k, v)
        return repo

    def get(self, owner, repo, fetch=False):
        user = GiteaUser(username=owner, client=self.user.client)
        r = GiteaRepo(user)
        r.name = repo
        if fetch:
            resp = self.user.client.api.repos.repoGet(repo=repo, owner=owner).json()
            for k, v in resp.items():
                setattr(r, k, v)
        return r

    def get_by_id(self, id):
        r = GiteaRepo(user=None)
        resp = self.user.client.api.repositories.repoGetByID(id=str(id)).json()
        for k, v in resp.items():
            setattr(r, k, v)
        return r

    __str__ = __repr__ = lambda self: "Gitea Repos"
