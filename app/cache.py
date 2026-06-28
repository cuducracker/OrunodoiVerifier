from datetime import datetime

# Status Constants
STATUS_SUCCESS = "FOUND"
STATUS_RC_NOT_FOUND = "RC_NOT_FOUND"
STATUS_WEBSITE_ERROR = "WEBSITE_ERROR"
STATUS_TIMEOUT = "TIMEOUT"
STATUS_UNIVERSAL_RC = "UNIVERSAL_RC"
STATUS_NO_RATION = "NO_RATION"
STATUS_INVALID_RC = "INVALID_RC"
STATUS_BLANK_RC = "BLANK_RC"


class RCCache:

    def __init__(self):

        # RC Number -> Cached Information
        self.cache = {}

        # RCs that should never be searched
        self.excluded_rc = {

            "999999999999": "Universal RC",

            "000000000000": "Invalid RC",

            "": "Blank RC",

            "NO RATION": "No Ration Card",

            "NAN": "Blank RC from Excel"
        }

    # -------------------------
    # Normalize RC Number
    # -------------------------

    def normalize(self, rc_number):

        if rc_number is None:
            return ""

        return str(rc_number).strip().upper()

    # -------------------------
    # Is Excluded? © 2026 Ankur Dowarah. All Rights Reserved.
    # -------------------------

    def is_excluded(self, rc_number):

        rc_number = self.normalize(rc_number)

        return rc_number in self.excluded_rc

    # -------------------------
    # Get Excluded Reason
    # -------------------------

    def excluded_reason(self, rc_number):

        rc_number = self.normalize(rc_number)

        return self.excluded_rc.get(rc_number)

    # -------------------------
    # Has Cache?
    # -------------------------

    def has(self, rc_number):

        rc_number = self.normalize(rc_number)

        return rc_number in self.cache

    # -------------------------
    # Get Cache
    # -------------------------

    def get(self, rc_number):

        rc_number = self.normalize(rc_number)

        return self.cache.get(rc_number)

    # -------------------------
    # Save Cache
    # -------------------------

    def save(self, rc_number, family_members):

        rc_number = self.normalize(rc_number)

        if self.is_excluded(rc_number):
            return
# RC Number -> Cached Information
        self.cache[rc_number] = {

            "family_members": family_members,

            "status": STATUS_SUCCESS,

            "cached_at": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

            "search_count": 1
        }

    # -------------------------
    # Increase Search Count
    # -------------------------

    def increment(self, rc_number):

        rc_number = self.normalize(rc_number)

        if self.has(rc_number):

            self.cache[rc_number]["search_count"] += 1

    # -------------------------
    # Size
    # -------------------------

    def size(self):

        return len(self.cache)

    # -------------------------
    # Clear
    # -------------------------

    def clear(self):

        self.cache.clear()
# © 2026 Ankur Dowarah. All Rights Reserved.