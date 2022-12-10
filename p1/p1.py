calcounts = []

with open("input") as f:
    c = 0
    for l in f:
        if l.strip().isdigit():
            c += int(l.strip())
        else:
            calcounts.append(c)
            c = 0

if c != 0:
    calcounts.append(c)

calcounts.sort()

print(calcounts[-1])

print(sum(calcounts[-3:]))
