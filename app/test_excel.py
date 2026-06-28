from excel import ExcelHandler

excel = ExcelHandler()

excel.load_excel("beneficiaries.xlsx")

print(excel.preview())

records = excel.get_records(

    beneficiary_column="B",

    rc_column="C",

    start_row=3,

    end_row=10

)

for record in records:

    print(record)