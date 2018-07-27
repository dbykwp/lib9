"""
Modules for common utilites
"""
import re
import string
import requests
from random import choice
from pyblake2 import blake2b

from JumpScale9 import j
from JumpScale9Lib.clients.blockchain.rivine import secrets
from JumpScale9Lib.clients.blockchain.rivine.const import HASH_SIZE
from JumpScale9Lib.clients.blockchain.rivine.encoding import binary
from JumpScale9Lib.clients.blockchain.rivine.errors import RESTAPIError


DURATION_REGX_PATTERN = '^(?P<hours>\d*)h(?P<minutes>\d*)m(?P<seconds>\d*)s$'
DURATION_TEMPLATE = 'XXhXXmXXs'

logger = j.logger.get(__name__)

def hash(data, encoding_type=None):
    """
    Hashes the input binary data using the blake2b algorithm

    @param data: Input data to be hashed
    @param encoding_type: Type of the data to guide the binary encoding before hashing
    @returns: Hashed value of the input data
    """
    binary_data = binary.encode(data, type_=encoding_type)
    return blake2b(binary_data, digest_size=HASH_SIZE).digest()



def locktime_from_duration(duration):
    """
    Parses a duration string and return a locktime timestamp

    @param duration: A string represent a duration if the format of XXhXXmXXs and return a timestamp
    @returns: number of seconds represented by the duration string
    """
    if not duration:
        raise ValueError("Duration needs to be in the format {}".format(DURATION_TEMPLATE))
    match = re.search(DURATION_REGX_PATTERN, duration)
    if not match:
        raise ValueError("Duration needs to be in the format {}".format(DURATION_TEMPLATE))
    values = match.groupdict()
    result = 0
    if values['hours']:
        result += int(values['hours']) * 60 * 60
    if values['minutes']:
        result += int(values['minutes']) * 60
    if values['seconds']:
        result += int(values['seconds'])

    return int(result)


def get_secret(size):
    """
    Generate a random secert token

    @param size: The size of the secret token
    """
    # alphapet = string.ascii_letters + string.digits
    # result = []
    # for _ in range(size):
    #     result.append(choice(alphapet))
    # return ''.join(result)
    return secrets.token_bytes(nbytes=size)


def get_current_chain_height(rivine_explorer_address):
    """
    Retrieves the current chain height
    """
    result = None
    url = '{}/explorer'.format(rivine_explorer_address.strip('/'))
    headers = {'user-agent': 'Rivine-Agent'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        msg = 'Failed to get current chain height. {}'.format(response.text)
        logger.error(msg)
        raise RESTAPIError(msg)
    else:
        result = response.json().get('height', None)
        if result is not None:
            result = int(result)
    return result


def check_address(rivine_explorer_address, address, log_errors=True):
    """
    Check if an address is valid and return its details

    @param address: Address to check
    @param log_errors: If False, no logging will be executed

    @raises: @RESTAPIError if failed to check address
    """
    result = None
    url = '{}/explorer/hashes/{}'.format(rivine_explorer_address, address)
    headers = {'user-agent': 'Rivine-Agent'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        msg = "Failed to retrieve address information. {}".format(response.text.strip('\n'))
        if log_errors:
            logger.error(msg)
        raise RESTAPIError(msg)
    else:
        result = response.json()
    return result
