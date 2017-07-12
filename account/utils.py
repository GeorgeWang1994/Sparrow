from django.conf import settings
from django.utils.encoding import smart_bytes
from django.utils.functional import allow_lazy
from django.utils.six import text_type

from Sparrow import settings as sparrow_settings

from hashlib import sha1
import random


def get_protocol():
    """
    Returns a string with the current protocol.

    This can be either 'http' or 'https' depending on ``USERENA_USE_HTTPS``
    setting.

    """
    protocol = 'http'
    if getattr(settings, 'USERENA_USE_HTTPS', sparrow_settings.DEFAULT_USERENA_USE_HTTPS):
        protocol = 'https'
    return protocol


def generate_sha1(string, salt=None):
    """
    Generates a sha1 hash for supplied string. Doesn't need to be very secure
    because it's not used for password checking. We got Django for that.

    :param string:
        The string that needs to be encrypted.

    :param salt:
        Optionally define your own salt. If none is supplied, will use a random
        string of 5 characters.

    :return: Tuple containing the salt and hash.

    """
    if not isinstance(string, (str, text_type)):
        string = str(string)

    if not salt:
        salt = sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]

    salted_bytes = (smart_bytes(salt) + smart_bytes(string))
    hash_ = sha1(salted_bytes).hexdigest()

    return salt, hash_