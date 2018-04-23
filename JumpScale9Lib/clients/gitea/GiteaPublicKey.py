import json
from js9 import j

JSBASE = j.application.jsbase_get_class()


class GiteaPublicKey(JSBASE):

    def __init__(
            self,
            user,
            id=None,
            key=None,
            title=None,
            created_at=None,
            fingerprint=None,
            url=None
    ):
        JSBASE.__init__(self)
        self.user = user
        self.id = id
        self.key = key
        self.title = title
        self.created_at = created_at
        self.fingerprint=fingerprint
        self.url = url

    @property
    def data(self):
        d = {}
        for attr in [
            'id',
            'key',
            'title',
            'created_at',
            'fingerprint',
            'url'
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
            raise NotImplementedError()

        elif create:
            if self.id:
                is_valid = False
                errors['id'] = 'Already existing'
            else:
                if not self.user.username:
                    is_valid = False
                    errors['user'] = {'username': 'Missing'}

                if not self.key:
                    is_valid = False
                    errors['key'] = 'Missing'

                if not self.title:
                    is_valid = False
                    errors['title'] = 'Missing'

        elif delete:
            if not self.id:
                is_valid = False
                errors['id'] = 'Missing'
        else:
            raise RuntimeError('You must choose operation to validate')

        if is_valid:
            return True, ''

        return False, '{0} Error '.format(operation) + json.dumps(errors)

    def save(self, update=False):
        """
        Create public key for user
        """
        is_valid, err = self.validate(update=update, create=not update)

        if not is_valid:
            raise Exception(err)

        if not update:
            resp = self.user.client.api.admin.adminCreatePublicKey(self.data, self.user.username)
            pubkey = resp.json()
            for k, v in pubkey.items():
                setattr(self, k, v)
        else:
            raise NotImplementedError()

    def delete(self):
        is_valid, err = self.validate(delete=True)

        if not is_valid:
            raise Exception(err)

        self.client.user.client.api.admin.adminDeleteUserPublicKey(username=self.username, id=self.id)

    __str__ = __repr__ = lambda self: json.dumps(self.data)
