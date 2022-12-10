import re

def contains(a, b):
    if a[0] <= b[0] and a[1] >= b[1] or \
       a[0] >= b[0] and a[1] <= b[1]:
        return True
    else:
        return False

def ovlp(a, b):
    if a[0] < b[0] and a[1] < b[0] or \
       a[0] > b[1] and a[1] > b[1]:
        return False
    else:
        return True

count_cont = 0

with open("input") as f:
    for l in f:
        (a, b, c, d) = map(int, re.split("[,-]", l.strip()))
        if contains((a,b),(c,d)):
            count_cont += 1

print(count_cont)

count_ovlp = 0

with open("input") as f:
    for l in f:
        (a, b, c, d) = map(int, re.split("[,-]", l.strip()))
        #print(a,b,c,d)
        if ovlp((a,b),(c,d)):
            #print("OVLP")
            count_ovlp += 1

print(count_ovlp)
