
def visible(g, s, maxr, maxc):
    (r,c) = s
    height = g[r][c]

    visl = visr = visu = visd = True

    #visible to left
    for i in range(c):
        if g[r][i] >= height:
            visl= False
            break
    #visible up
    for i in range(r):
        if g[i][c] >= height:
            visu= False
            break
    #visible right
    for i in range(c+1, maxc):
        if g[r][i] >= height:
            visr = False
            break
    #visible down
    for i in range(r+1, maxr):
        if g[i][c] >= height:
            visd= False
            break
        
    return visl or visr or visu or visd

def scenic(g, s, maxr, maxc):
    (r,c) = s
    height = g[r][c]

    visl = visr = visu = visd = 0

    #visible to left
    for (s,i) in enumerate(reversed(range(c))):
        visl= s+1
        if g[r][i] >= height:
            break
    #visible up
    for (s,i) in enumerate(reversed(range(r))):
        visu= s+1
        if g[i][c] >= height:
            break
    #visible right
    for (s,i) in enumerate(range(c+1, maxc)):
        visr = s+1
        if g[r][i] >= height:
            break
    #visible down
    for (s,i) in enumerate(range(r+1, maxr)):
        visd= s+1
        if g[i][c] >= height:
            break
        
    return visl * visr * visu * visd

grid= []

with open("input") as f:
    for l in f:
        row = [int(c) for c in l.strip()]
        grid.append(row)

viscount = 0
maxscenic = 0
maxr = len(grid)
maxc = len(grid[0])


for r in range(maxr):
    for c in range(maxc):
        if visible(grid, (r,c), maxr, maxc):
            viscount += 1
        score = scenic(grid, (r,c), maxr, maxc)
        if score > maxscenic:
            maxscenic = score
        #print (r,c,score)

print(viscount)
print(maxscenic)
