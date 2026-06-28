from flask import request, jsonify, send_file
import os

from loguru import logger

from app.upload_service import UploadService
from app.verification_service import VerificationService


upload_service = UploadService()
verification_service = VerificationService()

latest_report = None


def register_routes(app):

    # -----------------------------------------
    # Upload Excel
    # -----------------------------------------

    @app.route("/upload", methods=["POST"])
    def upload_excel():

        if "file" not in request.files:
            return jsonify({
                "success": False,
                "message": "No file selected."
            })

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "success": False,
                "message": "Please choose an Excel file."
            })

        return jsonify(upload_service.process(file))

    # -----------------------------------------
    # Verify Excel
    # -----------------------------------------

    @app.route("/verify", methods=["POST"])
    def verify():

        global latest_report

        data = request.get_json()

        result = verification_service.verify(

            file_path=data["file_path"],

            beneficiary_column=data["beneficiary_column"],

            rc_column=data["rc_column"],

            start_row=int(data["start_row"]),

            end_row=int(data["end_row"])

        )

        if result.get("success"):
            latest_report = result.get("output_file")

        return jsonify(result)

    # -----------------------------------------
    # Download Report
    # -----------------------------------------

   # -----------------------------------------
    # Download Report
    # -----------------------------------------

    @app.route("/download", methods=["GET"])
    def download():

        global latest_report

        if latest_report is None:
            return jsonify({
                "success": False,
                "message": "No report generated yet."
            }), 404

        # --- THESE LINES ARE NOW PROPERLY INDENTED INSIDE THE FUNCTION ---
        print("=" * 60)
        print("LATEST REPORT :", latest_report)

        absolute_path = os.path.abspath(latest_report)

        print("ABSOLUTE PATH :", absolute_path)
        print("FILE EXISTS   :", os.path.exists(absolute_path))
        print("=" * 60)

        if not os.path.exists(absolute_path):
            return jsonify({
                "success": False,
                "message": f"Report not found : {absolute_path}"
            }), 404
        logger.info(f"Downloading Report : {absolute_path}")
        return send_file(
            absolute_path,
            as_attachment=True,
            download_name=os.path.basename(absolute_path)
        )