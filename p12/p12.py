import heapq #CS201 time

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
#visited holds None if not visited
#(steps, previous) if visited
visited = []

def dist(pta, ptb):
    return abs(pta[0]-ptb[0]) + abs(pta[1]-ptb[1])

def add_neighbors(pt, steps):
    (r,c) = pt
    cur_h = m[r][c]
    newstep = steps+1
    for n in (r-1,c),(r+1,c),(r,c-1),(r,c+1):
        (nr, nc) = n
        if nr<0 or nc<0 or nr>=height or nc>=width:
            #out of bounds
            continue
        vis = visited[nr][nc]
        if vis and vis[0] <= newstep:
            #visited path is shorter
            continue
        elif m[nr][nc] - m[r][c] > 1:
            #can't reach
            continue
        else:
            #add to heap!
            cost = newstep + dist(n,end)
            heapq.heappush(q,(cost, newstep, n))
            visited[nr][nc] = (newstep, pt)

def find_short(sts):
    #clear out queue
    global q, visited
    q = []
    visited = [[None]*width for _ in range(height)]
    
    #add starting point(s)
    for st in sts:
        heapq.heappush(q,(dist(st,end), 0, st))
        visited[st[0]][st[1]] = (0, st)

    #iterate
    while len(q) > 0:
        spot = heapq.heappop(q)
        #print(spot)
        spotstep = spot[1]
        spotpt = spot[2]
        if spot[2] == end:
            return spotstep
        else:
            add_neighbors(spotpt, spotstep)

    return None

def print_path(endpt):
    pmap = []
    for row in m:
        prow = list(map(chr, row))
        pmap.append(prow)

    pt = endpt
    while True:
        pmap[pt[0]][pt[1]] = "*"
        prev = visited[pt[0]][pt[1]][1]
        if prev==None or prev==pt:
            break
        else:
            pt = prev
    for row in pmap:
        print("".join(row))

#part 1
print(find_short([start]))
print_path(end)

#part 2
print(find_short(eleva))
print_path(end)

