import os
import time

from app.excel import ExcelHandler
from app.verifier import Verifier
from app.report import ReportGenerator


def main():

    print("=" * 60)
    print("ORUNODOI SMART VERIFIER")
    print("Version : 1.0")
    print("Designed & Developed by Ankur Dowarah")
    print("=" * 60)

    file_path = input("\nEnter Excel File Path : ").strip()

    if not os.path.exists(file_path):

        print("\n❌ Excel file not found.")
        return

    beneficiary_column = input(
        "Beneficiary Column (Example B): "
    ).strip().upper()

    rc_column = input(
        "RC Number Column (Example C): "
    ).strip().upper()

    rows = input(
        "Rows (Example 3-2000): "
    ).strip()

    start_row, end_row = map(int, rows.split("-"))

    excel = ExcelHandler()

    excel.load_excel(file_path)

    records = excel.get_records(
        beneficiary_column=beneficiary_column,
        rc_column=rc_column,
        start_row=start_row,
        end_row=end_row
    )

    print(f"\n✓ Records Loaded : {len(records)}")

    verifier = Verifier()

    verifier.start()

    results = []

    start_time = time.time()

    try:

        for index, record in enumerate(records, start=1):

            print("\n" + "-" * 60)

            print(
                f"[{index}/{len(records)}] "
                f"{record['beneficiary']} "
                f"({record['rc_number']})"
            )

            verified = verifier.verify_record(record)

            results.append(verified)

    finally:

        verifier.stop()

    report = ReportGenerator()

    output_file = report.generate(results)

    end_time = time.time()

    print("\n" + "=" * 60)

    print("✓ Verification Completed")

    print("=" * 60)

    print(f"Total Records   : {len(results)}")

    print(
        f"Time Taken      : "
        f"{round(end_time-start_time,2)} seconds"
    )

    print(f"Report Saved    : {output_file}")

    print("=" * 60)


if __name__ == "__main__":

    main()