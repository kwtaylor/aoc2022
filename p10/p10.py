signal = [1]

with open("input") as f:
    for l in f:
        tokens = l.split()
        x = signal[-1]
        if tokens[0] == "noop":
            signal.append(x)
        elif len(tokens) >1:
            v = int(tokens[1])
            signal.append(x)
            signal.append(x+v)

print(signal)

total = 0

for c in (20,60,100,140,180,220):
    total += c*signal[c-1]

print(total)

cyc = 0

while cyc < len(signal)-40:
    for p in range(40):
        if p >= signal[cyc]-1 and p <= signal[cyc]+1:
            print("#", end="")
        else:
            print(".", end="")
        cyc += 1

    print("")
