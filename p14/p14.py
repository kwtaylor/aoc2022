minx=500
maxx=500
maxy=0
lines=[]

for l in open("input"):
    newline = []
    for p in l.split():
        if p[0].isdigit():
            (x,y) = map(int, p.split(","))
            newline.append((x,y))
            maxx = max(maxx,x)
            minx = min(minx,x)
            maxy = max(maxy,y)
    lines.append(newline)

print(minx,maxx,maxy)
#print(lines)
            
def makegrid():
    #rocks array is [y][x] to make printing easier
    #None = air, string=item
    global rocks
    rocks = [[None for _ in range(maxx-minx+1)] for _ in range(maxy+1)]
    for line in lines:
        lastpt = line[0]
        for pt in line[1:]:
            fillline(lastpt, pt)
            lastpt = pt

def printgrid():
    for row in rocks:
        for rock in row:
            r = rock if rock else "."
            print(r,end="")
        print()

def fillline(pt1, pt2):
    startx = pt1[0]-minx
    endx = pt2[0]-minx
    distx = endx - startx
    incx = 1 if distx==0 else distx//abs(distx)

    starty = pt1[1]
    endy = pt2[1]
    disty = endy - starty
    incy = 1 if disty==0 else disty//abs(disty)

    for x in range(startx, endx+incx, incx):
        for y in range(starty, endy+incy, incy):
            #print(x,y)
            rocks[y][x] = "*"

def sandfall(lefthi=0, lefthip1=0, righthi=0):
    #lefthi = height of imaginary sand pile off left of screen
    #lefthip1 = height of left pile if one more grain were added
    #righthi = height of right hand sand pile
    sandx = 500 - minx
    sandy = 0
    while True:
        sandy+=1
        if sandy > maxy:
            #falls into void
            return True
        elif not rocks[sandy][sandx]:
            #not blocked
            pass
        elif sandx == 0 and sandy < lefthi:
            #falls off left side
            if lefthip1 < lefthi and not rocks[lefthi][0]:
                #bounces back
                sandy = lefthi
                sandx = 0
            else:
                return -1
        elif sandx > 0 and not rocks[sandy][sandx-1]:
            #moves left
            sandx -=1
        elif sandx == maxx-minx and sandy < righthi:
            #falls off right side
            if not rocks[righthi][maxx-minx]:
                #bounces back
                sandy = righthi
                sandx = maxx-minx
            else:
                return 1
        elif sandx < maxx-minx and not rocks[sandy][sandx+1]:
            #moves right
            sandx +=1
        else:
            #settles
            rocks[sandy-1][sandx] = "o"
            return False
            

#PART 1
makegrid()
i = 0

while(not sandfall()):
    i+=1

printgrid()
print(i)

#PART2
import math
#MAAAATH
#kind of over-optimizing for area, solution is bounded anyway by triangle starting at (500,0)
#but I like the concept so I wanted to figure it out
def trihi(p):
    #how high a right triangle with num points is?
    #height ^ 2 / 2 + height/2 = num_points
    #h^2 + h - 2p = 0
    #h = (-1 + sqrt(1 + 4*2*p))/2

    h = (math.sqrt(1 + 8*p)-1)/2
    return int(h)

makegrid()
rocks.append([None for _ in range(maxx-minx+1)])
rocks.append(["*" for _ in range(maxx-minx+1)])
maxy+=2

leftc = 0
rightc = 0
tipx = 500 - minx
i = 0

while(not rocks[0][tipx]):
    s = sandfall(maxy-trihi(leftc), maxy-trihi(leftc+1), maxy-trihi(rightc))
    i+=1
    if type(s) is int:
        if s < 0:
            leftc += 1
        else:
            rightc += 1

printgrid()
print(i, leftc, rightc)

