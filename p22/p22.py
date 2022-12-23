import re

m = []
width = 0

for l in open("input"):
    #store sequence in last map position because why not
    m.append(l)
    width = max(width,len(l))
    
seq = m.pop(-1).strip()
height=len(m)

def move(dr,dc):
    global row,col
    tr=(row+dr)%height
    tc=(col+dc)%width

    while tc>=len(m[tr]) or m[tr][tc].isspace():
        tr=(tr+dr)%height
        tc=(tc+dc)%width

    if m[tr][tc] == ".":
        row,col = tr,tc

def rot(d):
    global d_r,d_c
    if d=="R":
        d_r,d_c=d_c,-d_r
    else:
        d_r,d_c=-d_c,d_r

row = 0
col = width-1
d_r =0
d_c =1
move(d_r,d_c) #get to first leftmost space

i=0
while i<len(seq):
    d=seq[i]
    if d.isdigit():
        sn=re.match(r"\d+",seq[i:]).group()
        i+=len(sn)
        for _ in range(int(sn)):
            move(d_r,d_c)
    else:
        rot(d)
        i+=1

print(row,col,d_r,d_c)

f=0
if d_r==1:
    f=1
elif d_c==-1:
    f=2
elif d_r==-1:
    f=3

print(1000*(row+1)+4*(col+1)+f)
