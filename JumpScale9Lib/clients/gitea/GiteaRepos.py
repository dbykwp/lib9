import requests
from js9 import j

from .GiteaRepo import GiteaRepo

JSBASE = j.application.jsbase_get_class()


class GiteaRepos(JSBASE):

    def __init__(self, client, user):
        JSBASE.__init__(self)
        self.user = user
        self.client = client
        self.position = 0

    def new(self):
        return GiteaRepo(self.client, self.user)

    def get(self, name, fetch=True):
        r = self.new()
        r.name = name
        if fetch:
            resp = self.user.client.api.repos.repoGet(repo=name, owner=self.user.username).json()
            for k, v in resp.items():
                setattr(r, k, v)
        return r

    @property
    def owned(self):
        result = []
        if self.user.is_current:
            items = self.user.client.api.user.userCurrentListRepos().json()
        else:
            items = self.user.client.api.users.userListRepos(username=self.user.username).json()

        for item in items:
            repo = self.new()
            for k, v in item.items():
                setattr(repo, k, v)
            result.append(repo)
        return result

    @property
    def stared(self):
        result = []
        if self.user.is_current:
            items = self.user.client.api.user.userCurrentListStarred().json()
        else:
            items = self.user.client.api.users.userListStarred(username=self.user.username).json()

        for item in items:
            repo = self.new()
            for k, v in item.items():
                setattr(repo, k, v)
            result.append(repo)
        return result

    @property
    def subscriptions(self):
        result = []
        if self.user.is_current:
            items = self.user.client.api.user.userCurrentListSubscriptions().json()
        else:
            items = self.user.client.api.users.userListSubscriptions(username=self.user.username).json()

        for item in items:
            repo = self.new()
            for k, v in item.items():
                setattr(repo, k, v)
            result.append(repo)
        return result

    def star(self, owner, repo):
        if not self.user.is_current:
            self.logger.debug('Only current user can star repos')
            return False
        try:
            self.user.client.api.user.userCurrentPutStar(data={}, owner=owner, repo=repo)
        except Exception as e:
            if e.response.status_code == 404:
                self.logger.debug('Owner does not exist')
                return False
        return True

    def unstar(self, owner, repo):
        if not self.user.is_current:
            self.logger.debug('Only current user can unstar repos')
            return False
        try:
            self.user.client.api.user.userCurrentDeleteStar(owner=owner, repo=repo)
        except Exception as e:
            if e.response.status_code == 404:
                self.logger.debug('Owner does not exist')
                return False
        return True

    def has_starred(self, owner, repo):
        if not self.user.is_current:
            self.logger.debug('Only current user can check if a a repo is starred')
        try:
            self.user.client.api.user.userCurrentCheckStarring(owner=owner, repo=repo)
        except Exception as e:
            if e.response.status_code == 404:
                self.logger.debug('Owner does not exist')
                return False
        return True

    def migrate(
            self,
            auth_username,
            auth_password,
            clone_addr,
            repo_name,
            description='',
            mirror=True,
            private=True
    ):
        try:
            # user is not fetched
            if not self.user.id:
                self.user = self.client.users.get(username=self.user.username, fetch=True)

            d = {
                'auth_username': auth_username,
                'auth_password': auth_password,
                'clone_addr': clone_addr,
                'description': description,
                'mirror': mirror,
                'repo_name': repo_name,
                'uid': self.user.id,
                'private': private
            }

            r = self.user.client.api.repos.repoMigrate(d).json()
            repo = self.new()
            for k, v in r.items():
                setattr(repo, k, v)
            return repo
        except Exception as e:
            self.logger.debug(e.response.content)

    def search(
            self,
            query,
            page_number=1,
            page_size=150,
            mode="",
            exclusive=False
    ):

        return self.client.repos.search(query, page_number, page_size, mode, exclusive)

    def __next__(self):
        if self.position < len(self._items):
            item = self._items[self.position]
            self.position += 1
            repo = self.new()
            for k, v in item.items():
                setattr(repo, k, v)
            return repo
        else:
            self.position = 0
            raise StopIteration()

    def __iter__(self):
        if self.user.is_current:
            self._items = self.client.api.user.userCurrentListRepos().json()
        else:
            self._items = self.client.api.users.userListRepos(username=self.user.username).json()

        return self

    def __repr__ (self):
        return "<Repos Iterator for user: {0}>".format(self.user.username)

    __str__ = __repr__
