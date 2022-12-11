import sqlalchemy as db
import re
import os
import json
import datetime
import shutil

# Defining the Engine
engine = db.create_engine('sqlite:///all_data.db', echo=True)
  
# Create the Metadata Object
metadata_obj = db.MetaData()
  
# Define the profile table
  
# database name
youtube = db.Table(
    'youtube',                                        
    metadata_obj,                                    
    db.Column('created_at', db.TIMESTAMP, primary_key=True),  
    db.Column('in_channel', db.String, primary_key=True),                    
    db.Column('sent_by', db.String, primary_key=True),
    db.Column('title', db.String, primary_key=True),
    db.Column('url', db.String, primary_key=True)                
)
  
 

# Create the profile table
metadata_obj.create_all(engine)
source = "yt_info"
backup = os.path.join(source, "backup")
source_exists = os.path.exists(source)
os.makedirs(backup, exist_ok=True)

if source_exists:
    pass
else:
    print(f"source {source} doesn't exist!")
    exit()

pattern = re.compile(r"yt-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d{6}\.json")
file_names = os.listdir(source)
file_names1 = list(filter(lambda x: re.match(pattern, x), file_names))

if len(file_names1) > 0:
    pass
else:
    print("Nothing to process!")
    exit()

file_paths = list(map(lambda x: os.path.join(source, x), file_names1))
json_store = list()
for file in file_paths:
    with open(file, "r") as fp:
        j = json.load(fp)
        json_store += j.copy()

insert = db.insert(youtube).prefix_with("OR IGNORE")
records = 0
for j in json_store:
    created_at = j["created_at"]
    j["created_at"] = datetime.datetime.fromisoformat(created_at)
    with engine.connect() as conn:
        result = conn.execute(insert, j)
        records += 1

for file in file_names1:
    _from = os.path.join(source, file)
    _to = os.path.join(backup, file)
    shutil.move(_from, _to)
    
table_changed_record = os.path.join(source, "table_change.txt")
with open(table_changed_record, "w") as fp:
    fp.write(str(records))
