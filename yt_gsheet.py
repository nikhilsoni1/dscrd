import gspread
import sqlalchemy as db
import pandas as pd
import os
import shutil

source = "yt_info"
table_changed_record = os.path.join(source, "table_change.txt")

records = 0
if os.path.exists(table_changed_record):
    with open(table_changed_record, "r") as fp:
        records = fp.read()

if int(records) > 0:
    os.remove(table_changed_record)
else:
    exit()

engine = db.create_engine('sqlite:///all_data.db', echo=True)
gc = gspread.service_account(filename="gspread.json")
sh = gc.open_by_url(url="https://docs.google.com/spreadsheets/d/16zBo7nKAljUkkVDkQDbmENs6WUt62Gtmw7OiWOPSxLg/")
worksheet = sh.worksheet("All Videos")

df = pd.read_sql_table("youtube", engine.connect())
df = df.sort_values(by=["created_at"], ascending=[False])
pld = [df.astype(str).columns.values.tolist()] + df.astype(str).values.tolist()
worksheet.clear()
worksheet.update(pld)