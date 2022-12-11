import gspread
import sqlalchemy as db
import pandas as pd


engine = db.create_engine('sqlite:///all_data.db', echo=True)
gc = gspread.service_account(filename="gspread.json")
sh = gc.open_by_url(url="https://docs.google.com/spreadsheets/d/16zBo7nKAljUkkVDkQDbmENs6WUt62Gtmw7OiWOPSxLg/")
worksheet = sh.worksheet("All Videos")

df = pd.read_sql_table("youtube", engine.connect())
df = df.sort_values(by=["created_at"], ascending=[False])
pld = [df.astype(str).columns.values.tolist()] + df.astype(str).values.tolist()
worksheet.clear()
worksheet.update(pld)