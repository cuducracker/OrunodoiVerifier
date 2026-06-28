from rapidfuzz import fuzz


class NameMatcher:

    def __init__(self):

        self.exact_match = 95

        self.review_match = 80

    # ----------------------------------

    # Compare Beneficiary Name

    # ----------------------------------

    def compare(self, beneficiary_name, family_members):

        beneficiary = beneficiary_name.upper().strip()

        best_name = ""

        best_score = 0

        for member in family_members:

            score = fuzz.token_set_ratio(

                beneficiary,

                member.upper().strip()

            )

            if score > best_score:

                best_score = score

                best_name = member

        # -----------------------------

        # Decide Status

        # -----------------------------

        if best_score >= self.exact_match:

            status = "EXACT MATCH"

            remarks = "Matched Successfully"

            found = True

        elif best_score >= self.review_match:

            status = "REVIEW REQUIRED"

            remarks = "Possible spelling difference"

            found = True

        else:

            status = "NOT FOUND"

            remarks = "Manual Verification Required"

            found = False

        return {

            "matched_name": best_name,

            "score": round(best_score, 2),

            "status": status,

            "remarks": remarks,

            "found": found

        }