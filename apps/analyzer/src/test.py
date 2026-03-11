a = [1,3,4,5]
mots = ["Python", "est", "génial"]
phrase = ""
for mot in mots:
    phrase += mot + " "
print(phrase)

count = 0
def inc():
    global count
    count += 1
    return count


big_list = list(range(1000))
sub = big_list[100:200]
step = big_list[::10]

# exemples d'itération de dictionnaire 
d = {"a": 1, "b": 2}
for k in d:
    v = d[k]
    print(k, v)

# bon pattern, ne déclenche rien
for k, v in d.items():
    print(k, v)

# exemples d'utilisation de get/setdefault 
d2 = {}
key = "x"
if key in d2:
    val = d2[key]
else:
    val = 0

# bonnes variantes
val = d2.get(key, 0)
val2 = d2.setdefault(key, 0)
