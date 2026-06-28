from verifier import Verifier

record = {

    "beneficiary": "PAWAN KUMAR KEOT",

    "rc_number": "181003001234"

}

verify = Verifier()

verify.start()

result = verify.verify_record(record)

print(result)

input("Press ENTER...")

verify.stop()