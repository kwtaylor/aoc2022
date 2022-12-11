
def catchup(head, tail):
    distr = tail[0] - head[0]
    distc = tail[1] - head[1]
    #print(distr,distc)

    if distr == 0:
        #same row
        if distc < -1:
            tail[1] += 1
        elif distc > 1:
            tail[1] -= 1
    elif distc == 0:
        #same column
        if distr < -1:
            tail[0] += 1
        elif distr > 1:
            tail[0] -= 1
    elif distr > 1:
        #diag catchup up
        tail[0] -= 1
        if distc < 0:
            tail[1] += 1
        elif distc > 0:
            tail[1] -= 1
    elif distr < -1:
        #diag catchup down
        tail[0] += 1
        if distc < 0:
            tail[1] += 1
        elif distc > 0:
            tail[1] -= 1
    elif distc > 1:
        #diag catchup left
        if distr < 0:
            tail[0] += 1
        elif distr > 0:
            tail[0] -= 1
        tail[1] -= 1
    elif distc < -1:
        #diag catchup right
        if distr < 0:
            tail[0] += 1
        elif distr > 0:
            tail[0] -= 1
        tail[1] += 1

def move(head, d):
    if d == "U":
        head[0] -= 1
    elif d == "D":
        head[0] += 1
    elif d == "L":
        head[1] -= 1
    elif d == "R":
        head[1] += 1

ropes = [[0,0] for i in range(10)]
spots = set()

with open("input") as f:
    for l in f:
        (d, n) = l.split()
        for i in range(int(n)):
            move(ropes[0],d)
            for j in range(1,10):
                catchup(ropes[j-1],ropes[j])
            spots.add(tuple(ropes[9]))
        
print(len(spots))
        
