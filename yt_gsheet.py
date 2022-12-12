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

engine = db.create_engine("sqlite:///all_data.db", echo=True)
gc = gspread.service_account(filename="gspread.json")
sh = gc.open_by_url(
    url="https://docs.google.com/spreadsheets/d/16zBo7nKAljUkkVDkQDbmENs6WUt62Gtmw7OiWOPSxLg/"
)


df = pd.read_sql_table("youtube", engine.connect())
df = df.sort_values(by=["created_at"], ascending=[False]).reset_index(drop=True)
pld = [df.astype(str).columns.values.tolist()] + df.astype(str).values.tolist()

try:
    worksheet = sh.add_worksheet(
        title="All Videos", rows=df.shape[0], cols=len(list(df))
    )
except gspread.exceptions.APIError:
    to_del = sh.worksheet("All Videos")
    sh.del_worksheet(to_del)
    worksheet = sh.add_worksheet(
        title="All Videos", rows=df.shape[0], cols=len(list(df))
    )

worksheet.clear()
worksheet.update(pld)

dt = df["created_at"].apply(lambda x: x.floor("D"))
wk = dt.apply(lambda x: x - pd.Timedelta(days=x.weekday()))

df1 = df.copy()
df1.insert(loc=0, column="dt", value=dt)
df1.insert(loc=0, column="wk", value=wk)

_today = pd.Timestamp.utcnow().floor("D").tz_localize(None)
_this_week = _today - pd.Timedelta(days=_today.weekday())

# Totals
p1 = df1.pivot_table(
    index=["sent_by"], values=["url"], aggfunc=lambda x: len(x.unique())
).reset_index()
p1.columns = ["Sent By", "Total Posts"]

# daily
dt_unique = pd.Series(dt.unique())
dt_unique = dt_unique[dt_unique < _today].sort_values().reset_index(drop=True)
dt_denom = dt_unique.max() - dt_unique.min() + pd.Timedelta(days=1)
dt_denom = dt_denom.days
dt_avg = p1["Total Posts"].divide(dt_denom).round(2)
p2 = p1.copy()
p2.insert(loc=len(list(p2)), column="Daily Posts", value=dt_avg)

# weekly
wk_unique = pd.Series(wk.unique())
wk_unique = wk_unique[wk_unique < _this_week].sort_values().reset_index(drop=True)
wk_denom = wk_unique.max() - wk_unique.min() + pd.Timedelta(days=7)
wk_denom = int(wk_denom.days / 7)
wk_avg = p2["Total Posts"].divide(wk_denom).round(2)
p3 = p2.copy()
p3.insert(loc=len(list(p3)), column="Weekly Posts", value=wk_avg)


daily_posts_wt = p3["Daily Posts"].multiply(100)
weekly_posts_wt = p3["Weekly Posts"].multiply(8)
total_posts_wt = p3["Total Posts"].multiply(1)
wt = (
    daily_posts_wt.add(weekly_posts_wt).add(total_posts_wt).sort_values(ascending=False)
)
p3.insert(loc=0, column="Score", value=wt)
p3 = (
    p3.sort_values(by=["Score"], ascending=[False])
    .reset_index(drop=True)
    .reset_index(names="Rank")
)
p3["Rank"] = p3["Rank"].add(1)
col_order = ["Rank", "Sent By", "Score", "Daily Posts", "Weekly Posts", "Total Posts"]
p3 = p3[col_order]


p3_pld = [p3.astype(str).columns.values.tolist()] + p3.astype(str).values.tolist()

try:
    worksheet2 = sh.add_worksheet(title="Ranking", rows=p3.shape[0], cols=len(list(p3)))
except gspread.exceptions.APIError:
    to_del = sh.worksheet("Ranking")
    sh.del_worksheet(to_del)
    worksheet2 = sh.add_worksheet(title="Ranking", rows=p3.shape[0], cols=len(list(p3)))

worksheet2.clear()
worksheet2.update(p3_pld)
