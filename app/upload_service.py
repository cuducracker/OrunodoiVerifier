import os
import pandas as pd
from app.logger import logger

class UploadService:

    def __init__(self):

        self.upload_folder = "uploads"

        os.makedirs(
            self.upload_folder,
            exist_ok=True
        )

    # -------------------------------------------------
    # Save Uploaded File
    # -------------------------------------------------

    def save_file(self, file):

        filename = os.path.basename(file.filename)
        logger.info(f"Uploaded File : {file.filename}")

        filepath = os.path.join(
            self.upload_folder,
            filename
        )

        file.save(filepath)

        return filepath

    # -------------------------------------------------
    # Read Excel
    # -------------------------------------------------

    def read_excel(self, filepath):

        return pd.read_excel(
            filepath,
            header=None
        )

    # -------------------------------------------------
    # Preview
    # -------------------------------------------------

    def get_preview(
        self,
        dataframe,
        rows=10
    ):

        return dataframe.head(rows).fillna("").values.tolist()

    # -------------------------------------------------
    # Total Rows
    # -------------------------------------------------

    def get_total_rows(
        self,
        dataframe
    ):

        return len(dataframe)

    # -------------------------------------------------
    # Total Columns
    # -------------------------------------------------

    def get_total_columns(
        self,
        dataframe
    ):

        return len(dataframe.columns)

    # -------------------------------------------------
    # Excel Column Letters
    # -------------------------------------------------

    def get_columns(
        self,
        dataframe
    ):

        columns = []

        total_columns = len(dataframe.columns)

        for i in range(total_columns):

            letter = ""

            n = i

            while True:

                letter = chr(65 + (n % 26)) + letter

                n = n // 26 - 1

                if n < 0:
                    break

            columns.append(letter)

        return columns

    # -------------------------------------------------
    # Detect Required Columns
    # -------------------------------------------------

    def detect_columns(
        self,
        dataframe
    ):

        detected = {

            "sl_no": None,

            "beneficiary": None,

            "rc_number": None,

            "village": None

        }

        keywords = {

            "sl_no": [

                "sl",
                "sl no",
                "sl. no",
                "serial",
                "serial no",
                "serial number"
            ],

            "beneficiary": [

                "beneficiary",
                "beneficiary name",
                "selected name",
                "selected name from rc during digitisation",
                "name"
            ],

            "rc_number": [

                "rc",
                "rc no",
                "rc number",
                "ration card",
                "ration card no",
                "ration card number"
            ],

            "village": [

                "village",
                "village name"
            ]

        }

        search_rows = min(5, len(dataframe))

        for row in range(search_rows):

            for col in range(len(dataframe.columns)):

                value = str(

                    dataframe.iat[row, col]

                ).strip().lower()

                if not value or value == "nan":

                    continue

                for key, words in keywords.items():

                    if detected[key] is not None:

                        continue

                    for word in words:

                        if word in value:

                            detected[key] = self.get_columns(dataframe)[col]

                            break

        return detected

    # -------------------------------------------------
    # Validate Upload
    # -------------------------------------------------

    def validate(
        self,
        detected
    ):

        required = [

            "beneficiary",

            "rc_number"

        ]

        missing = []

        for field in required:

            if detected[field] is None:

                missing.append(field)

        return {

            "valid": len(missing) == 0,

            "missing": missing

        }

    # -------------------------------------------------
    # Process Upload
    # -------------------------------------------------

    def process(self, file):

        filepath = self.save_file(file)

        dataframe = self.read_excel(filepath)
        logger.info(f"Excel Loaded Successfully")
        logger.info(f"Total Rows : {len(dataframe)}")
        logger.info(f"Total Columns : {len(dataframe.columns)}")

        detected = self.detect_columns(dataframe)

        validation = self.validate(detected)

        return {

            "success": True,

            "filename": os.path.basename(filepath),

            "file_path": filepath,

            "total_rows": self.get_total_rows(dataframe),

            "total_columns": self.get_total_columns(dataframe),

            "preview": self.get_preview(dataframe),

            "columns": self.get_columns(dataframe),

            "detected": detected,

            "validation": validation

        }