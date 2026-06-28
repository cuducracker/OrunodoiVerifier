import os

import pandas as pd

from flask import request, jsonify


UPLOAD_FOLDER = "uploads"


def register_routes(app):

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

        os.makedirs(

            UPLOAD_FOLDER,

            exist_ok=True

        )

        filepath = os.path.join(

            UPLOAD_FOLDER,

            file.filename

        )

        file.save(filepath)

        df = pd.read_excel(

            filepath,

            header=None

        )

        preview = df.head(10).fillna("").values.tolist()

        headers = []

        total_columns = len(df.columns)

        for i in range(total_columns):

            headers.append(

                chr(65 + i)

            )

        return jsonify({

            "success": True,

            "preview": preview,

            "columns": headers,

            "rows": len(df)

        })