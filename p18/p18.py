from ast import literal_eval
from collections import deque

coords = []
maxx = 0
maxy = 0
maxz = 0

for l in open("input"):
    coord = literal_eval(l)
    maxx = max(maxx,coord[0])
    maxy = max(maxy,coord[1])
    maxz = max(maxz,coord[2])
    coords.append(coord)

grid = [[[0] * (maxz+3) for _ in range(maxy+3)] for _ in range(maxx+3)]

num_edges = 0
adjacents = ((1,0,0),
             (-1,0,0),
             (0,1,0),
             (0,-1,0),
             (0,0,1),
             (0,0,-1))

def count_edges(x,y,z):
    edges = 0
    for xo,yo,zo in adjacents:
        edges+=grid[x+xo][y+yo][z+zo]
    return edges

for c in coords:
    x,y,z=c
    #offset cube to make sure empty space is around all sides
    x+=1
    y+=1
    z+=1
    grid[x][y][z]=1
    num_edges += 6 - count_edges(x,y,z)*2
 
print(num_edges)

#part 2 BFS time
search = deque()
seen = [[[0] * (maxz+3) for _ in range(maxy+3)] for _ in range(maxx+3)]

num_edges = 0
search.append((0,0,0))
seen[0][0][0]=1

while search:
    c = search.popleft()
    x,y,z=c
    for xo,yo,zo in adjacents:
        xn,yn,zn = x+xo,y+yo,z+zo
        if 0<=xn<=maxx+2 and \
           0<=yn<=maxy+2 and \
           0<=zn<=maxz+2:
            if grid[xn][yn][zn]:
                num_edges+=1
            elif not seen[xn][yn][zn]:
                seen[xn][yn][zn]=1
                search.append((xn,yn,zn))
            
print(num_edges)
    
