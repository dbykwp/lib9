import json
from js9 import j

from .GiteaOrgs import  GiteaOrgs
from .GiteaRepos import  GiteaRepos
from .GiteaPublicKeys import GiteaPublicKeys

JSBASE = j.application.jsbase_get_class()


class GiteaUser(JSBASE):

    def __init__(
            self,
            client,
            id=None,
            username=None,
            password=None,
            full_name=None,
            login_name=None,
            send_notify=None,
            source_id=None,
            email=None,
            active=None,
            admin=None,
            allow_git_hook=False,
            allow_import_local=False,
            location=None,
            max_repo_creation=None,
            website=None,
            avatar_url=None):

        JSBASE.__init__(self)
        self.client = client
        self.id=id
        self.username=username
        self.password = password
        self.full_name = full_name
        self.login_name = login_name
        self.send_notify = send_notify
        self.source_id = source_id
        self.email = email
        self.active = active
        self.admin = admin
        self.allow_git_hook = allow_git_hook
        self.allow_import_local = allow_import_local
        self.location = location
        self.max_repo_creation = max_repo_creation
        self.website = website
        self.avatar_url = avatar_url

    @property
    def data(self):
        """
        :return: obj as dict excluding all fields that don't have value set
        """
        d = {}

        for attr in [
            'id',
            'username',
            'password',
            'full_name',
            'login_name',
            'source_id',
            'send_notify',
            'email',
            'active',
            'admin',
            'allow_git_hook',
            'allow_import_local',
            'location',
            'max_repo_creation',
            'website',
            'avatar_url'
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

        if update:
            operation = 'update'
        elif delete:
            operation = 'delete'

        # Create or update

        if update or delete:
            if not self.username:
                is_valid = False
                errors['username'] = 'Missing'

        elif create:
            if self.id:
                errors['id'] = 'Already existing'
                is_valid = False
            else:
                if not self.password:
                    is_valid = False
                    errors['password'] = 'Missing'

                if not self.username:
                    is_valid = False
                    errors['username'] = 'Missing'

                if not self.email:
                    is_valid = False
                    errors['email'] = 'Missing'
        else:
            raise RuntimeError('You must choose operation to validate')

        if is_valid:
            return True, ''
        return False, '{0} Error '.format(operation) + json.dumps(errors)

    def save(self, update=False):
        """
        Save User
        """
        is_valid, err = self.validate(update=update)

        if not is_valid:
            raise Exception(err)

        if not update:
            resp = self.client.api.admin.adminCreateUser(data=self.data)
            user = resp.json()
            for k, v in user.items():
                setattr(self, k, v)

        elif update:
            self.client.api.admin.adminEditUser(data=self.data, username=self.username)

    def delete(self):
        is_valid, err = self.validate(create=False, delete=True)

        if not is_valid:
            raise Exception(err)

        self.client.api.admin.adminDeleteUser(username=self.username)

    @property
    def keys(self):
        return GiteaPublicKeys(self)

    @property
    def organizations(self):
        return GiteaOrgs(self)

    @property
    def repos(self):
        return GiteaRepos(self)

    __str__ = __repr__ = lambda self: json.dumps(self.data)
