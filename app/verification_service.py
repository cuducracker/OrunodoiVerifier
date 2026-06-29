import os
import time
from app.logger import logger
from app.excel import ExcelHandler
from app.verifier import Verifier
from app.report import ReportGenerator
from app.sqlite_cache import get_cached_beneficiary, save_beneficiary_to_cache


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
        try:
            self.excel.load_excel(file_path)
            records = self.excel.get_records(
                beneficiary_column=beneficiary_column,
                rc_column=rc_column,
                start_row=start_row,
                end_row=end_row
            )
        except Exception as e:
            logger.error(f"Failed to load Excel file: {e}")
            return {
                "success": False,
                "message": f"Excel loading error: {str(e)}"
            }

        total_records = len(records)
        results = []
        browser_started = False

        # ---------------------------------------------
        # Process Records (Row-by-Row Isolation)
        # ---------------------------------------------
        for record in records:
            # Wrap each row inside its own try-catch block so one bad row can't crash the whole run
            try:
                logger.info(f"🔎 Row Keys: {list(record.keys())} | Selected Column: {rc_column} | Value: {record.get(rc_column)}")

                # Robustly extract the RC number from the record dict
                # New Upgraded Line
                rc_no = record.get("rc_no") or record.get("rc_number") or record.get(rc_column) or record.get("rc")
                
                cached_result = None
                if rc_no:
                    rc_key = str(rc_no).strip()
                    cached_result = get_cached_beneficiary(rc_key)

                # --- 1. CACHE HIT ---
                if cached_result:
                    logger.info(f"🚀 Cache Hit! RC {rc_no} found in database. Skipping browser.")
                    results.append(cached_result)

                # --- 2. CACHE MISS ---
                else:
                    if not browser_started:
                        logger.info("🌐 Cache miss detected. Spinning up browser automation...")
                        self.verifier.start()
                        browser_started = True

                    verified = self.verifier.verify_record(record)
                    results.append(verified)

                    # Guard: Only cache if verification succeeded and isn't a temporary timeout/error
                    if rc_no and verified:
                        status = str(verified.get("status", "")).upper()
                        if status not in ["TIMEOUT", "ERROR"]:
                            rc_key = str(rc_no).strip()
                            save_beneficiary_to_cache(rc_key, verified)
                        else:
                            logger.warning(f"⚠️ Network lag detected for RC {rc_no} ({status}). Skipping cache write to allow a future retry.")

            except Exception as row_error:
                # If a row fails entirely, log it and keep moving forward
                logger.error(f"💥 Error processing row for RC {record.get(rc_column)}: {row_error}")
                fallback_result = {
                    "rc_no": record.get(rc_column),
                    "status": "REVIEW",
                    "message": f"System processing error: {str(row_error)}"
                }
                results.append(fallback_result)

        # ---------------------------------------------
        # Teardown Automation
        # ---------------------------------------------
        if browser_started:
            try:
                self.verifier.stop()
            except Exception as close_error:
                logger.warning(f"Failed to close browser session neatly: {close_error}")

        # ---------------------------------------------
        # Generate Report
        # ---------------------------------------------
        output_file = self.report.generate(results)
        logger.success("Report Generated Successfully")

        # ---------------------------------------------
        # Compile Statistics
        # ---------------------------------------------
        verified_count = 0
        review_count = 0
        skipped_count = 0
        not_found_count = 0

        for item in results:
            status = str(item.get("status", "")).upper() if isinstance(item, dict) else ""

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
            "time_taken": round(end_time - start_time, 2)
        }
        
        logger.success("Verification Completed")
        logger.info(f"Total Records : {total_records} | Verified : {verified_count} | Review : {review_count} | Not Found : {not_found_count}")
        
        return {
            "success": True,
            "message": "Verification Completed.",
            "download_url": "/download",
            "output_file": output_file,
            "statistics": statistics
        }