# DO NOT EDIT THIS FILE. This file will be overwritten when re-running go-raml.

"""
Auto-generated class for Heartbeat
"""
from six import string_types

from . import client_support


class Heartbeat(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(**kwargs):
        """
        :type farmer_id: string_types
        :type node_id: string_types
        :type os_version: string_types
        :type robot_address: string_types
        :type uptime: int
        :rtype: Heartbeat
        """

        return Heartbeat(**kwargs)

    def __init__(self, json=None, **kwargs):
        if json is None and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'Heartbeat'
        data = json or kwargs

        # set attributes
        data_types = [string_types]
        self.farmer_id = client_support.set_property('farmer_id', data, data_types, False, [], False, False, class_name)
        data_types = [string_types]
        self.node_id = client_support.set_property('node_id', data, data_types, False, [], False, True, class_name)
        data_types = [string_types]
        self.os_version = client_support.set_property(
            'os_version', data, data_types, False, [], False, True, class_name)
        data_types = [string_types]
        self.robot_address = client_support.set_property(
            'robot_address', data, data_types, False, [], False, True, class_name)
        data_types = [int]
        self.uptime = client_support.set_property('uptime', data, data_types, False, [], False, False, class_name)

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)
