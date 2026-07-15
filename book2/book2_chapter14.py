import openpyxl
import openpyxl.utils
wb = openpyxl.load_workbook("book2/chapter14_testdata.xlsx")
sheet1 = wb.active
row = sheet1["C"]
print(row)
