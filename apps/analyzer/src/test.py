# PY001
 a = [1, 3, 4, 5]

# PY002
mots = ["Python", "est", "génial"]
phrase = ""
for mot in mots:
    phrase += mot + " "
print(phrase)

# PY003
count = 0

def inc():
    global count
    count += 1
    return count

# PY006
big_list = list(range(1000))
sub = big_list[100:200]
step = big_list[::10]

# PY007
d = {"a": 1, "b": 2}
for k in d:
    v = d[k]
    print(k, v)
for k, v in d.items():
    print(k, v)

# PY008
d2 = {}
key = "x"
if key in d2:
    val = d2[key]
else:
    val = 0

val = d2.get(key, 0)
val2 = d2.setdefault(key, 0)

# PY009
from collections import defaultdict

dd = defaultdict(int)
for x in ["a", "b", "a"]:
    dd[x] += 1

dd2 = defaultdict(list)
dd2["key"].append("value")

# PY010 - mutable default argument example (should trigger diagnostic)
def add_item(x, items=[]):
    items.append(x)
    return items

# correct version

def add_item_safe(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items

