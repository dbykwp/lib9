import json
from js9 import j

JSBASE = j.application.jsbase_get_class()


class GiteaMarkdownRaw(JSBASE):
    def __init__(
            self,
            client,
            body=None):

        JSBASE.__init__(self)

        self.client = client
        self.body = body

    @property
    def data(self):
        """
        :return: obj as dict excluding all fields that don't have value set
        """
        d = {}

        for attr in [
            'body',
        ]:

            v = getattr(self, attr)
            if v:
                d[attr] = v
        return d

    def validate(self):
        """
        Validate required attributes are set before doing any operation
        """
        errors = {}
        is_valid = True

        if not self.body:
            is_valid = False
            errors['body'] = 'Missing'

        if is_valid:
            return True, ''

        return False, 'validation Error ' + json.dumps(errors)

    def render(self):
        is_valid, err = self.validate()

        if not is_valid:
            raise Exception(err)

        resp = self.client.api.markdown.renderMarkdownRaw(data=self.data)
        return resp.content

    def delete(self):
        raise NotImplementedError()

    __str__ = __repr__ = lambda self: json.dumps(self.data)
