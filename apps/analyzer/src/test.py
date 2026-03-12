<<<<<<< HEAD
a = [1,3,4,5]
=======
# PY001
a = [1, 3, 4, 5]

# PY002
>>>>>>> a826a1d6920b733e30ac77fbc3d5769787816f41
mots = ["Python", "est", "génial"]
phrase = ""
for mot in mots:
    phrase += mot + " "
print(phrase)

<<<<<<< HEAD
=======
# PY003
>>>>>>> a826a1d6920b733e30ac77fbc3d5769787816f41
count = 0
def inc():
    global count
    count += 1
    return count

<<<<<<< HEAD

=======
# PY006
>>>>>>> a826a1d6920b733e30ac77fbc3d5769787816f41
big_list = list(range(1000))
sub = big_list[100:200]
step = big_list[::10]

<<<<<<< HEAD
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
=======
a = ["Alice", "Bob"]
b = [20, 25]
for i in range(len(a)):
    print(a[i], b[i])

# PY011
def find_user(users, name):
    for u in users:
        if u == name:
            return u
    return None

# PY012
def stats(nums):
    return (min(nums), max(nums), sum(nums) / len(nums))

# PY013
s1 = "bonjour"
if s1 is "bonjour":
    print("Equal")

lst = [1, 2]
if lst is [1, 2]:
    print("same")

# PY014
my_list = [1, 2, 3, 4, 5]
if 3 in my_list:
    print("Found")

# PY015
words = ["Le", "Python", "est", "rapide"]
sentence = ""
for w in words:
    sentence += w + " "
print(sentence)

# PY016
list = [1, 2, 3]
str = "bonjour"
print(sum(list))

# PY017
numbers = [1, 3, 5, 8]
found = False
for x in numbers:
    if x % 2 == 0:
        found = True
        break

if found:
    print("There is an even number")

positives = [1, 2, -1]
all_positive = True
for x in positives:
    if x <= 0:
        all_positive = False
        break

if all_positive:
    print("All numbers are positive")
>>>>>>> a826a1d6920b733e30ac77fbc3d5769787816f41
