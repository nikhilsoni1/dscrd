import gspread
import sqlalchemy as db
import pandas as pd
import os
import shutil
import numpy as np
import random
from collections import OrderedDict

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

# Initiating connection with DB
engine = db.create_engine("sqlite:///all_data.db", echo=True)
# Initiating connection with DB

# Google Sheets - Initiating connection
gc = gspread.service_account(filename="gspread.json")
sh = gc.open_by_url(
    url="https://docs.google.com/spreadsheets/d/16zBo7nKAljUkkVDkQDbmENs6WUt62Gtmw7OiWOPSxLg/"
)
# Google Sheets - Initiating connection

# Reading and writing all videos from DB -------------
df = pd.read_sql_table("youtube", engine.connect())
df = df.sort_values(by=["created_at"], ascending=[False]).reset_index(drop=True)

# Column name renaming and ordering
df_col_names = OrderedDict()
df_col_names.setdefault("created_at", "Timestamp (UTC)")
df_col_names.setdefault("in_channel", "Channel/Thread")
df_col_names.setdefault("sent_by", "User")
df_col_names.setdefault("title", "Title")
df_col_names.setdefault("url", "URL")
df = df[df_col_names.keys()]
df = df.rename(columns=df_col_names)

pld = [df.astype(str).columns.values.tolist()] + df.astype(str).values.tolist()
worksheet = sh.worksheet(title="All Videos")
worksheet.clear()
worksheet.update(pld)
# Reading and writing all videos from DB -------------

# Summary Stats -------------
# Number of days/weeks calc. for denom
_today = pd.Timestamp.utcnow().floor("D").tz_localize(None)
dt = df["created_at"].apply(lambda x: x.floor("D"))
dt_unique = pd.Series(dt.unique())
dt_unique = dt_unique[dt_unique < _today].sort_values().reset_index(drop=True)
dt_denom = dt_unique.max() - dt_unique.min() + pd.Timedelta(days=1)
denom_dt = dt_denom.days
denom_wk = denom_dt/7
# Number of days/weeks calc. for denom

# Initial pivot table
func_len_unique = lambda x: len(x.unique())
piv = df.pivot_table(index=["sent_by"], values=["url"], aggfunc=func_len_unique)
piv = piv.reset_index()
# Initial pivot table

# Calc. averages
total = piv["url"]
avg_daily = total.divide(denom_dt).round().astype(int)
avg_weekly = total.divide(denom_wk).round().astype(int)
# Calc. averages

# Scoring
wt_daily = 100
wt_weekly = 8
wt_total = 1

wtd_avg_daily = avg_daily.multiply(wt_daily)
wtd_avg_weekly = avg_weekly.multiply(wt_weekly)
wtd_total = total.multiply(wt_total)
score = wtd_avg_daily.add(wtd_avg_weekly).add(wtd_total)
# Scoring

# Inserting averages + score to piv
piv.insert(loc=0, column="avg_daily", value=avg_daily)
piv.insert(loc=0, column="avg_weekly", value=avg_weekly)
piv.insert(loc=0, column="score", value=score)
# Inserting averages to piv

# Grand total - This break the flow
piv_sum = pd.DataFrame(piv.sum()).T
piv_sum.loc[:, "sent_by"] = "Grand Total"
piv_sum.loc[:, "score"] = -1
# Grand total - Flow continues from here...

# Sorting and numbers correction
piv = piv.sort_values(by=["score"], ascending=[False])
piv = pd.concat([piv, piv_sum], ignore_index=True)
piv = piv.reset_index(drop=True)
piv = piv.reset_index(names="rank")
piv.loc[:, "rank"] = piv["rank"].add(1)
piv.loc[piv["sent_by"]=="Grand Total", "rank"] = -1
# Sorting and numbers correction

# Column name renaming and ordering
col_names_order = OrderedDict()
col_names_order.setdefault("rank", "Rank")
col_names_order.setdefault("sent_by", "User")
col_names_order.setdefault("avg_daily", "Daily Posts")
col_names_order.setdefault("avg_weekly", "Weekly Posts")
col_names_order.setdefault("url", "All-time Posts")
col_names_order.setdefault("score", "Score")
piv = piv[col_names_order.keys()]
piv = piv.rename(columns=col_names_order)
# Column name renaming and ordering

# Writing to gsheet
piv_pld = [piv.astype(str).columns.values.tolist()] + piv.astype(str).values.tolist()
worksheet2 = sh.worksheet(title="Ranking")
worksheet2.clear()
worksheet2.update(piv_pld)
# Writing to gsheet
# Summary Stats -------------
