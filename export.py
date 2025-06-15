from openpyxl import Workbook
from db import get_all_applications

def export_to_excel():
    data = get_all_applications()
    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Имя", "Username", "Телефон", "Тип сайта", "Пакет", "Цена", "Комментарий"])
    for row in data:
        ws.append(row)
    file_path = "applications.xlsx"
    wb.save(file_path)
    return file_path
