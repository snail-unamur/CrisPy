# pyquit-disable avoid-shadowing-builtin-names
# pyquit-disable reduce-python-object-cost
# pyquit-disable use-collections-defaultdict
# pyquit-disable use-explicit-typing

# PY001
# pyquit-disable-next-line reduce-python-object-cost
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
    # pyquit-disable-next-line prefer-namedtuple-dataclass
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

# PY023
from math import *

value = ceil(2.7)
print(value)

# PY024
f = open("demo.txt", "r")
content = f.read()
print(content)
f.close()

# PY025
class Animal:
    pass

class Dog(Animal):
    pass

obj = Dog()
if type(obj) is Animal:
    print("Animal")

# PY026
numbers = [1, 2, 3, 4]
double_map = dict([(n, n * 2) for n in numbers])
print(double_map)

# PY027
def gcd(a, b):
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a

print(gcd(12, 8))

# PY028
name_str = "Alice"
count_int = 5
items_list = [1, 2, 3]
config_dict = {"mode": "dev"}

# PY029
try:
    x = 10 / 0
except Exception:
    print("Generic exception")
except ZeroDivisionError:
    print("Division by zero")

# PY030
def append_item(item, items=[]):
    items.append(item)
    return items

print(append_item(1))
print(append_item(2))

# PY031
import os

if os.path.exists("temp.txt"):
    os.remove("temp.txt")

# PY032
values = [1, 2, 3, 4]
doubles = map(lambda x: x * 2, values)
evens = filter(lambda x: x % 2 == 0, values)

print(list(doubles))
print(list(evens))


# PY018
my_list = [1, 2, 3, 4, 5]
if 3 in my_list:  # Cette ligne déclenche PY018
    print("Trouvé!")

# PY019

for i in range(10):
    for j in range(10):  # Cette ligne déclenche PY019
        print(i, j)

# PY020
total = sum([x * 2 for x in range(1000)])  # Déclenche PY020

# PY021
result = []
for i in range(100):
    result = result + [i]  # Cette ligne déclenche PY021

# PY022
i = 0
while i < 10:  # Cette boucle déclenche PY022
    print(i)
    i += 1

# PY034
matrix = [[i + j for j in range(100)] for i in range(100)]

for j in range(100):
    for i in range(100):
        x = matrix[i][j]

# PY035
numbers = [1, 2, 3, 4, 5]

# PY036
cache = []

for i in range(1000000):
    cache.append(i)

# PY037
data = []

for i in range(100000):
    data.append([i])

# PY007
d = {"a": 1, "b": 2, "c": 3}
for k in d:
    print(f"{k}: {d[k]}")  # Accès redondant

# PY008
player_scores = {"alice": 10, "bob": 5}
if "charlie" in player_scores:
    score = player_scores["charlie"]
else:
    score = 0
print(f"Score de Charlie: {score}")

# PY009
text = "le chat le chien le oiseau"
word_count = {}
for word in text.split():
# pyquit-disable-next-line use-dict-get-or-setdefault
    if word not in word_count:
        word_count[word] = 0
    word_count[word] += 1
print(word_count)  # {'le': 3, 'chat': 1, 'chien': 1, 'oiseau': 1}