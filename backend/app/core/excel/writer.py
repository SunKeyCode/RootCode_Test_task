import math
import os
from datetime import datetime

import xlsxwriter

from configs.app_config import FILES_DIR


def ignore_nan(worksheet, row, col, number, format=None):
    if math.isnan(number):
        return worksheet.write_blank(row, col, None, format)
    else:
        return None


def write_excel(data_to_write: dict):
    unload_path = FILES_DIR / "downloaded"
    if not os.path.exists(unload_path):
        os.makedirs(unload_path)

    workbook = xlsxwriter.Workbook(unload_path / "temp.xlsx")
    worksheet = workbook.add_worksheet("data")
    worksheet.add_write_handler(float, ignore_nan)

    date_format = workbook.add_format(
        {
            "num_format": "dd/mm/yy",
            "align": "center",
            "border": 1,
            "bg_color": "#E5E8E8",
        }
    )
    header_format = workbook.add_format(
        {
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "bg_color": "#E5E8E8",
            "text_wrap": True,
        }
    )
    values_format = workbook.add_format(
        {
            "border": 1,
        }
    )
    worksheet.set_row(1, 28, header_format)
    worksheet.set_column(1, 1, 15)

    first_value = list(data_to_write.values())[0]
    dates = first_value["data"].keys()

    col = 2
    for date in dates:
        worksheet.merge_range(
            0, col, 0, col + 1, datetime.strptime(date, "%Y-%m-%d"), date_format
        )
        worksheet.write_string(1, col, "план", header_format)
        worksheet.write_string(1, col + 1, "факт", header_format)
        col += 2

    worksheet.write_blank(0, 0, None, header_format)
    worksheet.write_blank(0, 1, None, header_format)
    worksheet.write_string(1, 0, "Код", header_format)
    worksheet.write_string(1, 1, "Наименование проекта", header_format)

    row = 2
    for key, project_data in data_to_write.items():
        col = 0
        worksheet.write(row, col, key, values_format)
        worksheet.write_string(row, col + 1, project_data["name"], values_format)
        for data_key, data_value in project_data["data"].items():
            col += 2
            worksheet.write(row, col, data_value["planed"], values_format)
            worksheet.write(row, col + 1, data_value["in_fact"], values_format)

        row += 1

    workbook.close()

    return unload_path / "temp.xlsx"
