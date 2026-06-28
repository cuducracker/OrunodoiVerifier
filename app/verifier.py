from app.automation import EposAutomation
from app.matcher import NameMatcher
from app.cache import RCCache


class Verifier:

    def __init__(self):

        self.bot = EposAutomation()
        self.matcher = NameMatcher()
        self.cache = RCCache()

    # -------------------------
    # Start Browser
    # -------------------------

    def start(self):

        self.bot.start()

    # -------------------------
    # Verify One Record
    # -------------------------

    def verify_record(self, record):

        rc_number = str(record["rc_number"]).strip()

        beneficiary = record["beneficiary"]

        # ===========================
        # Check Excluded RC
        # ===========================

        if self.cache.is_excluded(rc_number):

            record["family_members"] = ""

            record["matched_name"] = ""

            record["match_score"] = 0

            record["found"] = False

            record["status"] = "SKIPPED"

            record["remarks"] = self.cache.excluded_reason(rc_number)

            return record

        # ===========================
        # Check Cache
        # ===========================

        if self.cache.has(rc_number):

            print(f"✓ Cache Used : {rc_number}")

            data = self.cache.get(rc_number)

            self.cache.increment(rc_number)

            family_members = data["family_members"]

        else:

            print(f"🌐 Website Search : {rc_number}")

            family_members = self.bot.search_rc(rc_number)

            self.cache.save(
                rc_number,
                family_members
            )

        # ===========================
        # Compare Names
        # ===========================

        result = self.matcher.compare(
            beneficiary,
            family_members
        )

        # ===========================
        # Update Record
        # ===========================

        record["family_members"] = ", ".join(family_members)

        record["matched_name"] = result["matched_name"]

        record["match_score"] = result["score"]

        record["found"] = result["found"]

        record["status"] = result["status"]

        record["remarks"] = result["remarks"]

        return record

    # -------------------------
    # Stop Browser
    # -------------------------

    def stop(self):

        self.bot.stop()