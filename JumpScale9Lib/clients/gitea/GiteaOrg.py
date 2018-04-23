import json
from js9 import j

JSBASE = j.application.jsbase_get_class()


class GiteaOrg(JSBASE):

    def __init__(
            self,
            user,
            avatar_url=None,
            description=None,
            full_name=None,
            id=None,
            location=None,
            username=None,
            website=None
    ):
        JSBASE.__init__(self)
        self.user = user
        self.avatar_url = avatar_url
        self.description = description
        self.full_name = full_name
        self.id = id
        self.location = location
        self.username = username
        self.website = website

    @property
    def data(self):
        d = {}

        for attr in [
            'id',
            'avatar_url',
            'description',
            'full_name',
            'location',
            'username',
            'website',
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

                if not self.full_name:
                    is_valid = False
                    errors['full_name'] = 'Missing'

                if not self.username:
                    is_valid = False
                    errors['username'] = 'Missing'
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
            resp = self.user.client.api.admin.adminCreateOrg(data=self.data, username=self.user.username)
            user = resp.json()
            for k, v in user.items():
                setattr(self, k, v)

        elif update:
                raise NotImplementedError()

    __str__ = __repr__ = lambda self: json.dumps(self.data)
