import json
import uuid
import random


_FLAG = False
mem_src = "dscrd-lab-members.json"
mem_dest = "dscrd-lab-nyeb-ord.json"
if _FLAG:
    mem_src = "nayagan-members.json"
    mem_dest = "nayagan-nyeb-ord.json"
else:
    print("DEV MODE")

with open(mem_src, "r") as fp:
    mem = json.load(fp)

for m in mem:
    m.setdefault("member_nyeb", False)
    m.setdefault("member_foo", f"{uuid.uuid4()}")
    m.setdefault("member_nyeb_order", 0)


if mem_dest == "nayagan-nyeb-ord.json":
    with open(mem_dest, "w") as fp:
        json.dump(mem, fp, indent=4, sort_keys=True)
else:
    for idx, i in enumerate(range(3)):
        pld = random.choice(mem).copy()
        pld["member_nyeb_order"] = idx + 1
        mem.append(pld.copy())
    with open(mem_dest, "w") as fp:
        json.dump(mem, fp, indent=4, sort_keys=True)
