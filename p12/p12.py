import heapq #CS201 time
import math

m = []
visited = []
eleva = []

for (r,l) in enumerate(open("input")):
    row = []
    for (c,h) in enumerate(l.strip()):
        v = False
        if h == "S":
            start = (r,c)
            h = "a"
        elif h == "E":
            end = (r,c)
            h = "z"
        if h=="a":
            eleva.append((r,c))
        row.append(ord(h))
    m.append(row)

print(start)
print(end)

height = len(m)
width = len(m[0])

#A* time
#heapq with elements:
#(estcost, steps, (r,c))
q = []
visited = []

def dist(pta, ptb):
    return math.sqrt((pta[0]-ptb[0])**2 + (pta[1]-ptb[1])**2)

def add_neighbors(pt, steps):
    (r,c) = pt
    cur_h = m[r][c]
    for n in (r-1,c),(r+1,c),(r,c-1),(r,c+1):
        (nr, nc) = n
        if nr<0 or nc<0 or nr>=height or nc>=width:
            #out of bounds
            continue
        elif visited[nr][nc]:
            #visited
            continue
        elif m[nr][nc] - m[r][c] > 1:
            #can't reach
            continue
        else:
            #add to heap!
            cost = steps + 1 + dist(n,end)
            heapq.heappush(q,(cost, steps+1, n))
            visited[nr][nc] = True

def find_short(st):
    #clear out queue
    global q, visited
    q = []
    visited = [[False]*width for _ in range(height)]
    
    #add starting point
    add_neighbors(st, 0)
    visited[st[0]][st[1]] = True

    #iterate
    while len(q) > 0:
        spot = heapq.heappop(q)
        spotstep = spot[1]
        spotpt = spot[2]
        if spot[2] == end:
            return spotstep
        else:
            add_neighbors(spotpt, spotstep)

    return None

#part 1
print(find_short(start))

trails = []

#part 2
for pt in eleva:
    cost = find_short(pt)
    #print(pt, cost)
    if cost != None:
        trails.append(cost)

print(min(trails))

