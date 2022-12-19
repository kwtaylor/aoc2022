dirs = open("input").read().strip()
print(len(dirs))

rocks = (
    ((1,1,1,1),),
    ((0,1,0),
     (1,1,1),
     (0,1,0)),
    ((0,0,1),
     (0,0,1),
     (1,1,1)),
    ((1,),
     (1,),
     (1,),
     (1,)),
    ((1,1),
     (1,1))
    )

CH_WIDTH = 7
ST_HEIGHT = 3
ST_WIDTH = 2
NUM_ROCKS = 1000000000000 #2022
chamber = [[0] * CH_WIDTH for _ in range(ST_HEIGHT)]

def check_collide(rock,x,y):
    if x < 0:
        return True
    if x > CH_WIDTH - len(rock[0]):
        return True
    if y < 0:
        return True

    for row in reversed(r):
        if y >= len(chamber):
            return False
        c = x
        for col in row:
            if col and chamber[y][c]:
                return True
            c+=1
        y+=1

def push_rock(rock,d,x,y):
    if d == '<':
        if check_collide(rock,x-1,y):
            return x
        else:
            return x-1
    elif d == '>':
        if check_collide(rock,x+1,y):
            return x
        else:
            return x+1

def place_rock(rock,x,y):
    new_height = y+len(rock)+ST_HEIGHT
    for _ in range(len(chamber),new_height):
        chamber.append([0] * CH_WIDTH)
    for row in reversed(r):
        c = x
        for col in row:
            if col:
                chamber[y][c]=col
            c+=1
        y+=1

def draw_chamber():
    for row in reversed(chamber):
        for col in row:
            if col:
                print("#",end='')
            else:
                print(".",end='')
        print()
    print('-'*CH_WIDTH)

flat_rockn = 0
flat_ipat = 0
flat_offs = 0
flat_hi= 0
ff_height = 0

rockn = 0
i = 0

while rockn < NUM_ROCKS:
    r = rocks[rockn % len(rocks)]
    rockx = ST_WIDTH
    rocky = len(chamber)

    if rockn%10000 == 0:
        print(rockn)
    
    while True:
        rockx=push_rock(r,dirs[i],rockx,rocky)
        i = (i+1) % len(dirs)
        if check_collide(r,rockx,rocky-1):
            break
        rocky-=1

    place_rock(r,rockx,rocky)

    #columns 0-6 filled is as good as flat, since vertical line rock can't be blown to rightmost column
    ch_height = len(chamber)-ST_HEIGHT 
    if chamber[ch_height-1] == [1,1,1,1,1,1,0]:
        ipat = len(dirs)-1 if i==0 else i-1
        f_rock = rockn%len(rocks)
        offs = rockn-flat_rockn
        hoffs = ch_height-flat_hi
        
        print("flat surface found after",rockn,"wind pattern",ipat,"rock",f_rock,"offset",offs,"height",ch_height,"hoffs",hoffs)
        if ipat == flat_ipat and f_rock == flat_rockn%len(rocks) and flat_offs==offs:
            print("Pattern found! fast-forwarding")
            ff_rounds = (NUM_ROCKS-rockn-1)//flat_offs
            rockn += ff_rounds*flat_offs
            ff_height = ff_rounds*hoffs
            print("Resume at rock #",rockn,"height",ff_height)
            
        flat_rockn=rockn
        flat_ipat=ipat
        flat_offs=offs
        flat_hi=ch_height
        
    rockn+=1
    

print(len(chamber)-ST_HEIGHT+ff_height)
    
