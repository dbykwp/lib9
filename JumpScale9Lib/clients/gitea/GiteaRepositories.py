from js9 import j

from .GiteaRepo import GiteaRepo

JSBASE = j.application.jsbase_get_class()


class GiteaReposForClient(JSBASE):
    def __init__(self, client, user):
        JSBASE.__init__(self)
        self.user = user
        self.client = client

    def search(
        self,
        query,
        user_id=None,
        page_number=1,
        page_size=150,
        mode="",
        exclusive=False
    ):
        if page_size > 150 or page_size <= 0:
            page_size = 150

        if mode not in ["fork", "source", "mirror", "collaborative"]:
            self.logger.error('Only modes allowed [fork, source, mirror, collaborative]')
            return []

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
            self.logger.error('Response error')
            return []

        for item in items['data']:
            repo = GiteaRepo(self.client, None)
            for k, v in item.items():
                setattr(repo, k, v)
            # Search results are general, they don't have their proper user set
            # so we fix this
            u = self.client.users.new()
            for k, v in repo.owner.items():
                setattr(u, k, v)
            repo.user = u
            result.append(repo)
        return result

    def get(self, id):
        r = GiteaRepo(self.client, user=None)
        try:
            resp = self.user.client.api.repositories.repoGetByID(id=str(id)).json()

            for k, v in resp.items():
                setattr(r, k, v)
            u = self.client.users.new()
            for k, v in r.owner.items():
                setattr(u, k, v)
            r.user = u
            return r
        except Exception as e:
            if e.response.status_code == 404:
                self.logger.error('id not found')
            else:
                self.logger.error(e.response.content)

    def __repr__ (self):
        return "<General Repos finder and getter (by ID)>"
