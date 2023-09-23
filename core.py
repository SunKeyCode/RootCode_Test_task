from datetime import datetime
import pandas as pd

excel_data = pd.read_excel("example.xlsx")
dates = [date.date() for date in excel_data.columns if isinstance(date, datetime)]

for _, data in excel_data[1:].T.items():
    row = data.values.tolist()
    row_dict = {
        "id": row[0],
        "name": row[1],
        "data": [
            (
                dates[int((row_index - 2) / 2)],
                row[row_index],
                row[row_index + 1],
            )
            for row_index in range(2, len(row), 2)
        ],
    }
    print(row_dict)
