from src.common import *

CODING = "utf-8"


class IP_blacklist:
    def __init__(self, token_db, violation_limit, violation_period, block_time):
        """
        Set all initial parameters

        :param token_db: The DB to be used
        :param violation_limit: Max violations in the period
        :param violation_period: the length of "period"
        :param block_time: After exceed violation, we block the violator for a period
        """
        self.token_db = token_db
        self.violation_limit = violation_limit
        self.violation_lifetime = violation_period
        self.block_time = block_time

    def violate(self, ip_address):
        """
        Each time an IP address violates some certain security policy, we record the violator's
        IP address for this incident, both in the Redis DB and in the logging DB.

        After certain times of violation, the violator's IP address would be temporarily blocked.

        :param ip_address: The violator's IP address to be recorded.
        :return: if it was already blocked, return False, o.w. True.
        """
        if not self.check_ip_validity(ip_address):
            return False
        current_violations = self.token_db.hget("Access_violations", ip_address)
        #print(current_violations)
        if not current_violations:
            temp_json = {"violation_attempts": [get_timestamp()]}
            self.token_db.hset("Access_violations", ip_address, temp_json)
            return True
        now = get_timestamp()
        temp_json = byte2json(current_violations)

        # Add the current violation timestamp
        temp_json["violation_attempts"].append(now)

        # Pop out all expired violations
        while temp_json["violation_attempts"] \
                and now - temp_json["violation_attempts"][0] > self.violation_lifetime:
            del temp_json["violation_attempts"][0]

        # Store the modified violation list
        self.token_db.hset("Access_violations", ip_address, temp_json)

        # If the violation exceeds limit, block the IP
        if len(temp_json["violation_attempts"]) >= self.violation_limit:
            self.token_db.hset("Blocked_violators", ip_address, now)
        return True

    def check_ip_validity(self, ip_address):
        """
        Each time we process a request, we check whether the requester's IP address was already blocked.

        :param ip_address: Requester's IP address.
        :return: A boolean, return False if IP address is blocked.
        """
        current_result = self.token_db.hget("Blocked_violators", ip_address)
        if not current_result:
            return True
        if get_timestamp() - float(current_result) > self.block_time:
            self.token_db.hdel("Blocked_violators", ip_address)
            return True    # It was released
        return False