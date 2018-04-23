from js9 import j

from .GiteaUsers import GiteaUsers

JSBASE = j.application.jsbase_get_class()


class GiteaAdmin(JSBASE):
    """
    cl = j.clients.gitea
    admin = cl.admin
    new_user = admin.users.new()

    """
    def __init__(self, client):
        JSBASE.__init__(self)
        self.client = client

    @property
    def users(self):
        return GiteaUsers(self.client)

    def test(self):
        user = self.users.new()
        user.update(username='demo4', email='demo4@demo.com', password='123456')
        user.save()  # add
        j.logger.logger.info('successfully added user ' + str(user))

        # organizations
        user.organizations.test()
        user.repos.test()

        # keys
        key = user.keys.new()
        key.update(title='new_key',
                   key='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfurByig08O9oOKjWdx+B8RuQYJBE6UIjB26V/HQYxB/uGGMQxpFYCjEE51Cac7kHyBCqt+FHrqouL0buJEuvcVD8RGnPpyYO0jIf/T/sEevWOq2WshsshjOOkWHdPS1z5vfsgLhLTljAmvLAhPf2bBqJX1NRW5YFwcv9QgAihozlAeIFg8hnxsWf/tS5tggx9Y9eX9+20IBkUSftZQ6lRI6HXpzp2v4sHrMHYShCKEoFBL40Icy3KB/ZQfzoeXS3qvY5KRYWQDtkyaxN8fS4CkndQx07279Q7PXX6II2+OsgGgdoHz8NKb+0Wi4aG8/gOtzJHVuVt6PTk2B37+78r hamdy@hamdy')
        key.save()  # add
        j.logger.logger.info('successfully added key ' + str(key))
        key.delete()
        j.logger.logger.info('successfully deleted key ' + str(key))

        user.update(email='demo5@demo.com', username='demo4')
        user.save(update=True)  # edit
        j.logger.logger.info('successfully update user ' + str(user))
        user.delete()
        j.logger.logger.info('successfully deleted user ' + str(user))

    __repr__ = __str__ = lambda self: "Gitea Admin"

