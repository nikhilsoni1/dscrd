import pandas as pd
import json

with open("videos.json", "r") as fp:
    videos = json.load(fp)
df = pd.DataFrame(videos)
created_at = pd.to_datetime(df["created_at"]).copy()
pst = created_at.dt.tz_convert("US/Pacific").dt.tz_localize(None)
est = created_at.dt.tz_convert("US/Eastern").dt.tz_localize(None)
ist = created_at.dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
# df = df.drop(columns=["created_at"])
df.insert(loc=0, column="created_at_ist", value=ist)
df.insert(loc=0, column="created_at_est", value=est)
df.insert(loc=0, column="created_at_pst", value=pst)
df.to_csv("videos.csv", index=False)