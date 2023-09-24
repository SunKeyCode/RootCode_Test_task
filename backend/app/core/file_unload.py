import math
import os
from collections import OrderedDict
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
import xlsxwriter

from models.models import ProjectData
from configs.app_config import FILES_DIR


async def select_file_data(session: AsyncSession, version: int):
    data = await session.scalars(
        select(ProjectData)
        .where(ProjectData.file_version_id == version)
        .options(joinedload(ProjectData.project))
        .order_by(ProjectData.date)
    )

    return data.all()


def create_file_from_data(data: list[ProjectData]):
    result_dict = {}
    for item in data:
        project = result_dict.setdefault(item.project_id, {})
        project["name"] = item.project.name
        proj_data = project.setdefault("data", OrderedDict())
        project_data_as_string = str(item.date.date())
        date = proj_data.setdefault(project_data_as_string, {})
        date["in_fact"] = item.in_fact
        date["planed"] = item.planed

    return result_dict


def ignore_nan(worksheet, row, col, number, format=None):
    if math.isnan(number):
        return worksheet.write_blank(row, col, None, format)
    else:
        # Return control to the calling write() method for any other number.
        return None


def write_exel(data_to_write: dict):
    unload_path = FILES_DIR / "unloaded"
    if not os.path.exists(unload_path):
        os.makedirs(unload_path)

    workbook = xlsxwriter.Workbook(unload_path / "test.xlsx")
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
            "text_wrap": True
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

    return unload_path / "test.xlsx"
