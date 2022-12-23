import sys

DIRS = ((-1,0), #N
        (1,0),  #S
        (0,-1), #E
        (0,1))  #W

m = []
#elf list, [(row, col), next_move]
elves = []
r=0
r_min=999
r_max=0
c_min=999
c_max=0

if len(sys.argv)>1:
    f = sys.argv[1]
else:
    f = "input"

for l in open(f):
    l=l.strip()
    w=len(l)
    row = ['.']*w
    c=w
    for i in l:
        row.append(i)
        if i=='#':
            elves.append([(r+w,c),None])
            r_min=min(r_min,r+w)
            r_max=max(r_max,r+w)
            c_min=min(c_min,c)
            c_max=max(c_max,c)
        c+=1
    row += ['.']*w
    m.append(row)
    r+=1

m = [['.']*w*3 for _ in range(w)] + m + [['.']*w*3 for _ in range(w)]
w*=3

dir_phase = 0

print(r_min,r_max,c_min,c_max)

def print_and_count():
    count=0
    for r in range(r_min,r_max+1):
        print(f"{r:3}", end='')
        for c in range(c_min,c_max+1):
            c=m[r][c]
            print(c,end='')
            if c==".":
                count+=1
        print()
        
    print(count)

print_and_count()

#map markers
# .=space
# #=elf
# +=potential elf move
# *=elf conflict

i=0
elf_moved=True
while elf_moved:
    if i%10 == 0:
        print(i)
    #first half, decide on moves
    for e in elves:
        er, ec = e[0]
        e[1] = None
        plan = None
        neigh = False
        for d in range(dir_phase,dir_phase+4):
            dr,dc = DIRS[d %4]
            tr=er+dr
            tc=ec+dc
            if dr==0:
                tm=tuple(m[tr+o][tc]=="#" for o in (-1,0,1))
            else:
                tm=tuple(m[tr][tc+o]=="#" for o in (-1,0,1))
            if tm == (False, False, False):
                if not plan:
                    #plan move
                    plan=(tr,tc)
            else:
                neigh=True

        if neigh and plan:
            tr,tc=plan
            if m[tr][tc] == '.':
                e[1]=plan
                m[tr][tc]="+"
            else:
                #elf conflict
                m[tr][tc] = "*"
    r_min=w
    r_max=0
    c_min=w
    c_max=0

    #2nd half, do move:
    elf_moved=False
    for e in elves:
        if e[1]:
            er,ec = e[0]
            mr,mc = e[1]
            if m[mr][mc] == "*":
                #elf conflict, back off
                m[mr][mc] = "."
            else:
                #do move
                m[er][ec] = "."
                m[mr][mc] = "#"
                e[0] = (mr,mc)
                elf_moved=True
        r_min=min(r_min,e[0][0])
        r_max=max(r_max,e[0][0])
        c_min=min(c_min,e[0][1])
        c_max=max(c_max,e[0][1])
    #print(i,dir_phase,r_min,r_max,c_min,c_max)
    #print_and_count()
    dir_phase = (dir_phase+1)%4
    i+=1

print(i)

