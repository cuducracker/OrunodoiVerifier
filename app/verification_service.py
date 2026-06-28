import os
import time
from app.logger import logger
from app.excel import ExcelHandler
from app.verifier import Verifier
from app.report import ReportGenerator


class VerificationService:

    def __init__(self):

        self.excel = ExcelHandler()
        self.verifier = Verifier()
        self.report = ReportGenerator()

    # -------------------------------------------------
    # Verify Uploaded Excel
    # -------------------------------------------------

    def verify(

        self,

        file_path,

        beneficiary_column,

        rc_column,

        start_row,

        end_row

    ):

        if not os.path.exists(file_path):

            return {

                "success": False,

                "message": "Uploaded Excel file not found."

            }

        start_time = time.time()
        logger.info("Verification Started")

        # ---------------------------------------------
        # Load Excel
        # ---------------------------------------------

        self.excel.load_excel(file_path)

        records = self.excel.get_records(

            beneficiary_column=beneficiary_column,

            rc_column=rc_column,

            start_row=start_row,

            end_row=end_row

        )

        total_records = len(records)

        results = []

        # ---------------------------------------------
        # Start Browser
        # ---------------------------------------------

        self.verifier.start()

        try:

            for record in records:

                verified = self.verifier.verify_record(record)

                results.append(verified)

        except Exception as e:

            return {

                "success": False,

                "message": str(e)

            }

        finally:

            self.verifier.stop()

        # ---------------------------------------------
        # Generate Report
        # ---------------------------------------------

        output_file = self.report.generate(results)
        logger.success("Report Generated Successfully")

        # ---------------------------------------------
        # Statistics
        # ---------------------------------------------

        verified_count = 0
        review_count = 0
        skipped_count = 0
        not_found_count = 0

        for item in results:

            status = str(

                item.get(

                    "status",

                    ""

                )

            ).upper()

            if status == "MATCH":

                verified_count += 1

            elif status == "REVIEW":

                review_count += 1

            elif status == "SKIPPED":

                skipped_count += 1

            else:

                not_found_count += 1

        end_time = time.time()

        statistics = {

            "total_records": total_records,

            "verified": verified_count,

            "review": review_count,

            "not_found": not_found_count,

            "skipped": skipped_count,

            "time_taken": round(

                end_time - start_time,

                2

            )

        }
        logger.success("Verification Completed")
        logger.info(f"Total Records : {total_records}")
        logger.info(f"Verified : {verified_count}")
        logger.info(f"Review : {review_count}")
        logger.info(f"Not Found : {not_found_count}")
        logger.info(f"Skipped : {skipped_count}")
        logger.info(f"Time Taken : {round(end_time-start_time,2)} sec")
        return {

            "success": True,

            "message": "Verification Completed.",

            "download_url": "/download",

            "output_file": output_file,

            "statistics": statistics

        }