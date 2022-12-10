
# tree structure
# [ None, size, { dir:[ parent, size, {} ]
#                 dir:[ parent, size, {} ],
#                 etc
#               }
# ]

root = [None, 0, {}]
curdir = root
alldirs = []

def add_dir(parent, name):
    newdir = [parent, 0, {}]
    parent[2].update({name:newdir})
    return newdir

def add_file(parent, size):
    parent[1] += size
    if parent[0]:
        add_file(parent[0], size)

#only works because puzzle input steps logically through directories,
#hitting each once, so took some shortcuts
with open("input") as f:
    for line in f:
        tokens = line.split()
        if len(tokens) == 0:
            continue
        if tokens[0] == "$":
            # command line
            if tokens[1] == "cd" and tokens[2] == "..":
                curdir = curdir[0]
            elif tokens[1] == "cd" and tokens[2] != "/":
                curdir = add_dir(curdir, tokens[2])
                alldirs.append(curdir)
        elif tokens[0].isdigit():
            # file listing
            add_file(curdir, int(tokens[0]))

print(root[1], root[2].keys())

dsum = 0
dsizes = []

TARGET = 30000000 - (70000000 - root[1])

for d in alldirs:
    dsize = d[1]
    if dsize >= TARGET:
        dsizes.append(dsize)
    if dsize <= 100000:
        dsum += dsize

print(dsum)

print(TARGET, min(dsizes))


