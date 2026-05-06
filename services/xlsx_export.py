import openpyxl
import os
import zipfile

def export_attendance_to_xlsx(date, present_roll_numbers, xlsx_path):
    """
    Appends attendance for a specific date to an existing xlsx file.
    marks 'P' for present and 'A' for absent.
    """
    if not os.path.exists(xlsx_path):
        return None
    if not zipfile.is_zipfile(xlsx_path):
        return None

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    # Find the next empty column
    next_col = ws.max_column + 1
    
    # Check if the date already exists in the header (row 1)
    date_str = date.strftime('%d/%m/%Y')
    for c in range(1, ws.max_column + 1):
        if ws.cell(1, c).value == date_str:
            next_col = c
            break

    # Set date in the header
    ws.cell(1, next_col).value = date_str

    # Iterate through students (assuming roll numbers are in column 2 starting row 2)
    # Skipping the footer (row 36) as seen in user's file
    for row in range(2, 36):
        roll_no = ws.cell(row, 2).value
        if roll_no:
            ws.cell(row, next_col).value = 'P' if str(roll_no) in present_roll_numbers else 'A'

    wb.save(xlsx_path)
    return xlsx_path
