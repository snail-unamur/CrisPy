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