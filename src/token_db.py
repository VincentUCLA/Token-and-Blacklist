import redis
from src.RedisTimer import RedisTimer
from src.common import *

TOKEN_IDLETIME = 120
TOKEN_LIFETIME = 900
DEFAULT_ENTROPY = 256
CODING = "utf-8"
TOKEN_DB = redis.StrictRedis(host='localhost', port=6379, db=0)


class Token:
    def __init__(self):
        """
        Initialization of the class

        :return: Nothing
        """
        self.RT = RedisTimer(TOKEN_DB, "Access_tokens", TOKEN_IDLETIME, TOKEN_LIFETIME)

    def generate_access_token(self, user_id, ip_address, user_agent):
        """
        Generate an access token for certain user.
        The access token is only valid for the very short idle time limit (TOKEN_IDLETIME).
        However, we store an ABSOLUTE time limit. We do not extend the token time limit after
        the ABSOLUTE time limit (TOKEN_LIFETIME).

        Note we store the parameters as JSON format.

        :param user_id: User's ID in DB.
        :param ip_address: Requester's IP address.
        :param user_agent: Requester's user-agent in HTTP request header.
        :return: A boolean, whether a valid token was generated.
        """
        token = gen_token()
        temp_json = {
            "token": token,
            "ip_address": ip_address,
            "user-agent": user_agent
        }
        if not self.RT.dict_generate(user_id, temp_json):
            return False
        return token

    def extend_access_token(self, user_id):
        """
        Extend the token time limit of a very short idle time limit (TOKEN_IDLETIME) as each
        legal request is processed.

        We do not extend the token time limit after the ABSOLUTE time limit (TOKEN_LIFETIME).
        In this case, we invalidate the token.

        We return False as the token does not exist or is invalidated.

        :param user_id: User's ID in DB.
        :return: Return False as the token does not exist or is invalidated.
        """
        return self.RT.dict_extend(user_id)

    def validate_access_token(self, user_id, token, ip_address, user_agent):
        """
        Checks whether the requester's token is validated.

        :param user_id: User's ID in DB.
        :param token: Token.
        :param ip_address: Requester's IP address.
        :param user_agent: Requester's user-agent in HTTP request header.
        :return: A boolean, whether the requester's token is validated.
        """
        current_token = self.RT.dict_get(user_id)
        if not current_token:
            return False

        # If token, IP address, or user-agent is invalid
        if token != current_token["token"] \
                or ip_address != current_token["ip_address"] \
                or user_agent != current_token["user-agent"]:
            return False
        return True

    def invalidate_access_token(self, user_id):
        """
        Removes the access_token from the database, for certain reasons.

        :param user_id: User's ID in DB.
        :return: Nothing
        """
        self.RT.dict_remove(user_id)
