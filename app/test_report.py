from report import ReportGenerator

records = [

    {

        "sl_no": 1,

        "beneficiary": "PAWAN KEOT",

        "rc_number": "181003001234",

        "family_members": "PAWAN, NIHA, SABITRI",

        "best_match": "PAWAN KEOT",

        "match_score": 100,

        "status": "Exact Match",

        "remarks": "Matched Successfully"

    },

    {

        "sl_no": 2,

        "beneficiary": "ROKINI",

        "rc_number": "181003004321",

        "family_members": "ROHINI, MINU",

        "best_match": "ROHINI",

        "match_score": 94,

        "status": "Review Required",

        "remarks": "Possible spelling difference"

    }

]

report = ReportGenerator()

report.generate(records)