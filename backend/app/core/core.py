import re

from datetime import datetime
import pandas as pd


# excel_data = pd.read_excel("example.xlsx")
# dates = [date.date() for date in excel_data.columns if isinstance(date, datetime)]

# print(excel_data.head())
#
# for _, data in excel_data[1:].T.items():
#     row = data.values.tolist()
#     row_dict = {
#         "code": row[0],
#         "name": row[1],
#         "data": [
#             (
#                 dates[int((row_index - 2) / 2)],
#                 row[row_index],
#                 row[row_index + 1],
#             )
#             for row_index in range(2, len(row), 2)
#         ],
#     }
#     print(row_dict)

def covert_date(value) -> datetime.date:
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, str):
        match = re.search(r"\d{4}-\d{2}-\d{2}", value)
        if match:
            data_as_string = match.group(0)
            return datetime.strptime(data_as_string, "%Y-%m-%d").date()

    return None


class PandasDataLoader:
    def __init__(self, file):
        self._loaded_data = pd.read_excel(file)
        self._dates = self._set_dates()

    def _set_dates(self):
        dates = []
        for column in self._loaded_data.columns:
            converted_data = covert_date(column)
            if converted_data is not None:
                dates.append(converted_data)
        return dates

    @property
    def dates(self):
        return self._dates

    @property
    def codes(self):
        return self._loaded_data["Unnamed: 0"][1:].tolist()

    def get_projects_info_by_codes(self, codes: list):
        return self._loaded_data.loc[
            self._loaded_data["Unnamed: 0"].isin(codes),
            ["Unnamed: 0", "Unnamed: 1"],
        ].values

    def get_items_for_db(self):
        print(self.dates)
        for _, data in self._loaded_data[1:].T.items():
            row = data.values.tolist()
            row_dict = {
                "code": row[0],
                "name": row[1],
                "data": [
                    (
                        self._dates[int((row_index - 2) / 2)],
                        row[row_index],
                        row[row_index + 1],
                    )
                    for row_index in range(2, len(row), 2)
                ],
            }
            yield row_dict


class FileDataManager:
    def __init__(self, data_loader):
        pass
