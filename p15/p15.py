import re

#sensor list is x,y,beaconx,beacony,distance,num
sensors = []

def man_dist(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

n=0
for l in open("input"):
    line = re.split(r"[^-0-9]+",l.strip())
    (sx,sy,bx,by) = map(int, line[1:5])
    sensors.append((sx,sy,bx,by,man_dist(sx,sy,bx,by),n))
    n+=1

print(sensors)

covered = dict()
row = 2000000

for (sx,sy,bx,by,sd,_) in sensors:
    dist_to_row = abs(sy-row)
    if dist_to_row <= sd:
        xoffs = sd - dist_to_row
        xstart = sx - xoffs
        xend = sx + xoffs
        for x in range(xstart, xend+1):
            if (x,row) != (bx,by):
                covered[(x,row)] = True

print(len(covered))
        
#PART 2: 
size = 4000000
#sort sensors by y coordinate to speed things up
sensors.sort(key=lambda s: s[1])
print(sensors)

for x in range(0,size+1):
    if x%10000==0:
        print(x)
    y = 0
    found=False
    while(y <= size and not found):
        for (sx,sy,_,_,sd,n) in sensors:
            if man_dist(x,y,sx,sy) <= sd:
                #yold=y
                y = sy + sd -abs(x-sx) + 1
                #print("skip",n,yold,y)
                #would need to break here and recheck all sensors
                #if not sorted by y
                if y > size:
                    break
        else:
            found=True
        
    if found:
        print(x,y)
        print(x*size+y)
        break


