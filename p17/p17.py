dirs = open("input").read().strip()

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
NUM_ROCKS = 2022
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
        
rockn = 0
i = 0

while rockn < NUM_ROCKS:
    #draw_chamber()
    r = rocks[rockn % len(rocks)]
    rockx = ST_WIDTH
    rocky = len(chamber)
    
    while True:
        rockx=push_rock(r,dirs[i],rockx,rocky)
        i = (i+1) % len(dirs)
        if check_collide(r,rockx,rocky-1):
            break
        rocky-=1

    place_rock(r,rockx,rocky)
    rockn+=1
    

print(len(chamber)-3)
    
    
    
    
