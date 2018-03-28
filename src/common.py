import json
import datetime
import os
import base64
DEFAULT_ENTROPY = 256

CODING = "utf-8"


def get_timestamp():
    """
    Gets the current UNIX timestamp

    :return: Current UNIX timestamp.
    """
    return datetime.datetime.now().timestamp()


def byte2json(byte):
    """
    Convert a byte string

    :param byte: A string of bytes.
    :return: A JSON dict.
    """
    return json.loads(byte.decode(CODING).replace("\'", "\""))


def gen_token(entropy=DEFAULT_ENTROPY):
    """
    Generates a URL-save token with 256-bit entropy.

    :return: A URL-save token.
    """
    return base64.urlsafe_b64encode(os.urandom(entropy)).rstrip(b'=').decode('ascii')
