import re

gotcrates = False
stacks = [[] for j in range(9)]

with open("input") as f:
    for l in f:
        if not gotcrates:
            for j,i in enumerate(range(1, len(l), 4)):
                val = l[i]
                #print(j, i, val)
                if val.isdigit():
                    gotcrates = True
                elif val.isalpha():
                    stacks[j].append(val)
                #print(stacks)
        else:
            cmd = re.split(r"\D+",l.strip())
            if len(cmd) == 4:
                (mv, fr, to) = map(int, cmd[1:])
                for i in reversed(range(mv)):
                    #CrateMover9000
                    #stacks[to-1].insert(0, stacks[fr-1].pop(0))
                    #CreateMover9001
                    stacks[to-1].insert(0, stacks[fr-1].pop(i))
        #print(stacks)
        

for s in stacks:
    item = " "
    if s:
        item = s[0]

    print(item, end="")

print("")
