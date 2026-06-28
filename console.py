import os
import time

from app.excel import ExcelHandler
from app.verifier import Verifier
from app.report import ReportGenerator


def main():

    print("=" * 60)
    print("ORUNODOI SMART VERIFIER")
    print("Designed & Developed by Ankur Dowarah")
    print("=" * 60)

    file_path = input(
        "\nEnter Excel File Path : "
    ).strip()

    if not os.path.exists(file_path):

        print("\nExcel file not found.")

        return

    beneficiary_column = input(
        "Beneficiary Column (Example B): "
    ).upper()

    rc_column = input(
        "RC Number Column (Example C): "
    ).upper()

    rows = input(
        "Rows (Example 3-2000): "
    )

    start_row, end_row = map(
        int,
        rows.split("-")
    )

    excel = ExcelHandler()

    excel.load_excel(file_path)

    records = excel.get_records(

        beneficiary_column=beneficiary_column,

        rc_column=rc_column,

        start_row=start_row,

        end_row=end_row

    )

    print(f"\nRecords Loaded : {len(records)}")

    verifier = Verifier()

    verifier.start()

    results = []

    start_time = time.time()

    for index, record in enumerate(records, start=1):

        print()

        print("-" * 50)

        print(

            f"{index}/{len(records)}",

            record["beneficiary"]

        )

        verified = verifier.verify_record(record)

        results.append(verified)

    verifier.stop()

    report = ReportGenerator()

    report.generate(results)

    end_time = time.time()

    print()

    print("=" * 60)

    print("Verification Completed")

    print(f"Total Records : {len(results)}")

    print(

        f"Time Taken : "

        f"{round(end_time-start_time,2)} sec"

    )

    print("Output Saved in output/Output.xlsx")

    print("=" * 60)


if __name__ == "__main__":

    main()