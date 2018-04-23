import json
from js9 import j

JSBASE = j.application.jsbase_get_class()


class GiteaRepo(JSBASE):

    def __init__(
            self,
            user,
            clone_url=None,
            created_at=None,
            default_branch=None,
            description=None,
            empty=False,
            fork=False,
            forks_count=None,
            full_name=None,
            html_url=None,
            id=None,
            mirror=None,
            name=None,
            open_issues_count=None,
            owner=None

    ):
        JSBASE.__init__(self)
        self.user = user
        self.clone_url = clone_url
        self.description = description
        self.full_name = full_name
        self.id = id
        self.created_at = created_at
        self.default_branch = default_branch
        self.empty = empty
        self.fork = fork
        self.forks_count = forks_count
        self.html_url = html_url
        self.mirror = mirror
        self.name = name
        self.open_issues_count = open_issues_count
        self.owner = owner

    @property
    def data(self):
        d = {}

        for attr in [
            'id',
            'clone_url',
            'description',
            'full_name',
            'created_at',
            'default_branch',
            'empty',
            'fork',
            'forks_count',
            'html_url',
            'mirror',
            'name',
            'open_issues_count',
            'owner'
        ]:

            v = getattr(self, attr)
            if v:
                d[attr] = v
        return d

    def validate(self, create=False, update=False, delete=False):
        """
            Validate required attributes are set before doing any operation
        """
        errors = {}
        is_valid = True

        operation = 'create'

        if update or delete:
            raise NotImplementedError()

        elif create:
            if self.id:
                is_valid = False
                errors['id'] = 'Already existing'
            else:
                if not self.user.username:
                    is_valid = False
                    errors['user'] = {'username':'Missing'}

                if not self.name:
                    is_valid = False
                    errors['name'] = 'Missing'
        else:
            raise RuntimeError('You must choose operation to validate')

        if is_valid:
            return True, ''

        return False, '{0} Error '.format(operation) + json.dumps(errors)

    def save(self, update=False):
        is_valid, err = self.validate(update=update, create=not update)

        if not is_valid:
            raise Exception(err)

        if not update:
            resp = self.user.client.api.admin.adminCreateRepo(data=self.data, username=self.user.username)
            user = resp.json()
            for k, v in user.items():
                setattr(self, k, v)

        elif update:
                raise NotImplementedError()

    __str__ = __repr__ = lambda self: json.dumps(self.data)
