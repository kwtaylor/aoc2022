sumpri = 0

def getpri(item):
    if item.islower():
        pri = 1 + ord(item) - ord("a")
    else:
        pri = 27 + ord(item) - ord("A")
    return pri

with open("input") as f:
    for l in f:
        l = l.strip()
        size = len(l)
        c1 = set(l[:size//2])
        c2 = set(l[size//2:])
        item = c1.intersection(c2).pop()
        sumpri += getpri(item)


print(sumpri)

sumpri = 0

with open("input") as f:
    for l in f:
        c0 = set(l.strip())
        c1 = set(f.readline().strip())
        c2 = set(f.readline().strip())

        item = c0.intersection(c1).intersection(c2).pop()
        sumpri += getpri(item)

print(sumpri)

        
