import json
import uuid
import random
import sys

_FLAG = False
try:
    _FLAG = bool(sys.argv[1])
except IndexError:
    pass
mem_src = "dscrd-lab-members.json"
mem_dest = "dscrd-lab-nyeb-ord.json"
if _FLAG:
    mem_src = "nayagan-members.json"
    mem_dest = "nayagan-nyeb-ord.json"
else:
    print("DEV MODE")

with open(mem_src, "r") as fp:
    mem = json.load(fp)

for idx, m in enumerate(mem):
    m.setdefault("member_nyeb", False)
    m.setdefault("member_foo", f"{uuid.uuid4()}")
    m.setdefault("member_nyeb_order", idx)


if mem_dest == "nayagan-nyeb-ord.json":
    with open(mem_dest, "w") as fp:
        json.dump(mem, fp, indent=4, sort_keys=True)
else:
    _order = list(range(3))
    random.shuffle(_order)
    pld = mem[0].copy()
    for i in _order:
        pld["member_nyeb_order"] = i + 1
        pld["member_foo"] = f"{uuid.uuid4()}"
        mem.append(pld.copy())
    with open(mem_dest, "w") as fp:
        json.dump(mem, fp, indent=4, sort_keys=True)
