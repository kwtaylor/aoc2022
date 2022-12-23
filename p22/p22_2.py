import re
import math
import operator
from collections import deque

m = []
width = 0

for l in open("input"):
    #store sequence in last map position because why not
    if len(l.strip())>0:
        m.append(ls := l.rstrip())
    lwidth=width
    width = max(width,len(ls))
    
seq = m.pop(-1).strip()
height=len(m)
width=lwidth
edge=math.gcd(width,height)
if edge==height or edge==width:
    #cover 2x6 case (all others are 3x4)
    edge=edge//2

print(width,height,edge)

#translate flat map into face connectivity map
#face map is Rx[Cx[]]
#Each face map entry is [R,D,L,U]
#Each RDLU is is (R,C) to connecting face
DIRS = ( (0,1), #right
         (1,0), #down
         (0,-1), #left
         (-1,0)) #up
face_map = []
start_face_C = width//edge
for r in range(0,height,edge):
    face_row = []
    for c in range(0,width,edge):
        print(f"test {r} {c}")
        if c>=len(m[r]):
            face_row.append(None)
        elif m[r][c].isspace():
            face_row.append(None)
        else:
            print("face!")
            if r==0:
                start_face_C=min(start_face_C,c//edge)
            face = []
            for nr,nc in ( (r+DR*edge, c+DC*edge) for DR,DC in DIRS ):
                print(f"   test {nr} {nc}")
                if nr<0 or nr >= height:
                    face.append(None)
                elif nc<0 or nc >= len(m[nr]):
                    face.append(None)
                elif m[nr][nc].isspace():
                    face.append(None)
                else:
                    print("   Neighbor!")
                    R=nr//edge
                    C=nc//edge
                    face.append((R,C))
            face_row.append(face)
    face_map.append(face_row)

print(start_face_C)
                    
#Now fold up into faces:
#Right-hand coordinate system is row (+down), column (+right), depth (+front)
#faces are labeled by axis direction they face (r,c,d) so front is (0,0,1) top is (-1,0,0) etc
# each face entry is (r,c,d)->(face map (R,C), local r direction (r,c,d), local c direction (r,c,d))
faces = {}
cur_face = (0,0,1)
#queue of faces to search, item is (face (r,c,d), face entry () )
#"starting" face is front with local r,c aligned with global r,c
fqueue = deque()
fqueue.append(( cur_face, ((0,start_face_C),(1,0,0),(0,1,0)) ))

#get new face coordinates when folding over edge
#move is local (r,c) signed direction
#returns ((face),(r_map),(c_map))
def fold_over(move, face, r_map, c_map):
    mr,mc=move
    #new face points in global direction of move on initial face
    new_face = tuple(gr*mr+gc*mc for gr,gc in zip(r_map,c_map))
    new_r_map = r_map
    new_c_map = c_map
    if mr!=0:
        #over top/bottom edge, r coordinate shifts to negative face direction
        new_r_map = tuple(-mr*fr for fr in face)
    elif mc!=0:
        #over left/right edge, c coordinate shifts to negative face direction
        new_c_map = tuple(-mc*fc for fc in face)

    return (new_face,new_r_map,new_c_map)

while fqueue:
    face,((R,C),r_map,c_map) = fqueue.popleft()

    if face in faces:
        continue
    faces[face] = ((R,C),r_map,c_map)

    print(R,C, face, face_map[R][C], r_map, c_map)

    for move, neigh in zip(DIRS, face_map[R][C]):
        if neigh:
            new_face,new_r_map,new_c_map = fold_over(move, face, r_map, c_map)
            print ("   neighbor",move,new_face,neigh)
            fqueue.append( (new_face, (neigh, new_r_map, new_c_map)) )
            
print(faces)

def dot(vec1, vec2):
    return sum(map(operator.mul, vec1, vec2))

# find coord position in new_map from old_map
def xform(coord, old_rmap, old_cmap, new_rmap, new_cmap):
    r_glob = tuple(r*coord[0] for r in old_rmap)
    c_glob = tuple(c*coord[1] for c in old_cmap)

    new_r = dot(new_rmap,r_glob)+dot(new_rmap,c_glob)
    new_c = dot(new_cmap,r_glob)+dot(new_cmap,c_glob)

    return (new_r,new_c)

#given current face, current local r,c, and local movement direction,
#return (new_face, new local (r,c), new local movement direction)
def move_over(face, old_pos, move):
    global edge
    _,r_map,c_map = faces[face]
    mr,mc = move

    #new face points in global direction of move on initial face
    new_face = tuple(gr*mr+gc*mc for gr,gc in zip(r_map,c_map))
    _,new_r_map,new_c_map = faces[new_face]

    if mr!=0:
        #over top/bottom edge, r coordinate shifts to negative face direction
        r_map = tuple(-mr*fr for fr in face)
    elif mc!=0:
        #over left/right edge, c coordinate shifts to negative face direction
        c_map = tuple(-mc*fc for fc in face)

    #transform coordinates & move from old map to new map
    new_r,new_c = xform(old_pos, r_map, c_map, new_r_map, new_c_map)
    new_move = xform(move, r_map, c_map, new_r_map, new_c_map)
    new_r+=new_move[0]
    new_c+=new_move[1]

    #wrapping to non-inverted coordinates is just mod:
    # 49+1=50 ->0  = 50%50
    #  0-1=-1 ->49 = -1%50
    #but to inverted, need to flip and adjust by 1 first:
    # 49+1=50 ->49 = (-50-1)%50
    #  0-1=-1 ->0  = ( +1-1)%50
    #
    # original map ->
    #(1,0,0),(0,1,0) ->flip right side
    #(1,0,0),(0,0,-1) ->old map R is R, C is -D
    #(0,0,-1),(-1,0,0) ->new map R is -D, C is -R
    r_sense = dot(new_r_map, r_map) + dot(new_r_map, c_map)
    c_sense = dot(new_c_map, r_map) + dot(new_c_map, c_map)

    if r_sense<0:
        new_r=new_r-1
    if c_sense<0:
        new_c=new_c-1

    new_pos = tuple(c%edge for c in (new_r,new_c))

    return (new_face, new_pos, new_move)

local_pos = (0,0)
d_r =0
d_c =1

def move():
    global local_pos,cur_face,d_r,d_c
    (tr,tc) = local_pos
    test_face = cur_face
    tdr,tdc = d_r,d_c

    ttr=tr+tdr
    ttc=tc+tdc
    
    if ttr<0 or ttr>=edge or ttc<0 or ttc>=edge:
        test_face, (tr,tc), (tdr,tdc) = move_over(cur_face,(tr,tc),(tdr,tdc))
    else:
        tr,tc=ttr,ttc

    (R,C) = faces[test_face][0]
    nr = tr+R*edge
    nc = tc+C*edge

    if m[nr][nc] != "#":
        m[nr] = m[nr][0:nc] + "x" + m[nr][nc+1:]
        local_pos = (tr,tc)
        cur_face = test_face
        d_r,d_c=tdr,tdc
        

def rot(d):
    global d_r,d_c
    if d=="R":
        d_r,d_c=d_c,-d_r
    else:
        d_r,d_c=-d_c,d_r

i=0
while i<len(seq):
    d=seq[i]
    if d.isdigit():
        sn=re.match(r"\d+",seq[i:]).group()
        i+=len(sn)
        for _ in range(int(sn)):
            move()
    else:
        rot(d)
        i+=1

for l in m:
    print(l)

R,C=faces[cur_face][0]
row = local_pos[0] + R*edge
col = local_pos[1] + C*edge

print(row,col,d_r,d_c)

f=0
if d_r==1:
    f=1
elif d_c==-1:
    f=2
elif d_r==-1:
    f=3

print(1000*(row+1)+4*(col+1)+f)
