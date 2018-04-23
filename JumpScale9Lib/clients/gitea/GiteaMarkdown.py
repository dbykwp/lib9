import json
from js9 import j

JSBASE = j.application.jsbase_get_class()


class GiteaMarkdown(JSBASE):
    def __init__(
            self,
            client,
            context=None,
            mode = None,
            text = None,
            wiki = True,):

        JSBASE.__init__(self)

        self.client = client
        self.context = context
        self.mode = mode
        self.text = text
        self.wiki = wiki

    @property
    def data(self):
        """
        :return: obj as dict excluding all fields that don't have value set
        """
        d = {}

        for attr in [
            'context',
            'mode',
            'text',
            'wiki',
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

        if not self.text:
            is_valid = False
            errors['text'] = 'Missing'

        if is_valid:
            return True, ''

        return False, 'validation Error ' + json.dumps(errors)

    def render(self):
        is_valid, err = self.validate()

        if not is_valid:
            raise Exception(err)

        resp = self.client.api.markdown.renderMarkdown(data=self.data)
        return resp.content


    def delete(self):
        raise NotImplementedError()

    __str__ = __repr__ = lambda self: json.dumps(self.data)
