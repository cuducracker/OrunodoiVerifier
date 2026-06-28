import pandas as pd


class ExcelHandler:

    def __init__(self):

        self.df = None

    # -------------------------------
    # Load Excel File
    # -------------------------------

    def load_excel(self, file_path):

        self.df = pd.read_excel(file_path, header=None)

        return self.df

    # -------------------------------
    # Preview First Rows
    # -------------------------------

    def preview(self, rows=10):

        return self.df.head(rows)

    # -------------------------------
    # Convert Excel Column Letter
    # Example:
    # A -> 0
    # B -> 1
    # C -> 2
    # AA -> 26
    # -------------------------------

    def column_to_index(self, column):

        column = column.upper()

        index = 0

        for char in column:

            index = index * 26 + (ord(char) - ord("A") + 1)

        return index - 1

    # -------------------------------
    # Read Data
    # -------------------------------

    def get_records(

            self,

            beneficiary_column,

            rc_column,

            start_row,

            end_row

    ):

        beneficiary_index = self.column_to_index(
            beneficiary_column
        )

        rc_index = self.column_to_index(
            rc_column
        )

        records = []

        for row in range(start_row - 1, end_row):

            beneficiary = str(
                self.df.iat[row, beneficiary_index]
            ).strip()

            rc = str(
                self.df.iat[row, rc_index]
            ).strip()

            records.append({

                "beneficiary": beneficiary,

                "rc_number": rc,

                "excel_row": row + 1

            })

        return records