from collections import deque
import math

moving_left = []
moving_right = []
moving_up = []
moving_down = []

with open("input") as f:
    w = len(f.readline().strip())-2
    h=0
    for l in f:
        ml,mr,mu,md = [],[],[],[]
        l=l.strip()
        if l[1]=='#':
            continue
        for x in l[1:-1]:
            ml.append(True) if x == '<' else ml.append(False)
            mr.append(True) if x == '>' else mr.append(False)
            mu.append(True) if x == '^' else mu.append(False)
            md.append(True) if x == 'v' else md.append(False)
        h+=1
        moving_left.append(ml)
        moving_right.append(mr)
        moving_up.append(mu)
        moving_down.append(md)

phase_max = math.lcm(w,h)
print(w,h,phase_max)

def occupied(phase,r,c):
    return moving_left[r][(c+phase)%w] or \
           moving_right[r][(c-phase)%w] or \
           moving_up[(r+phase)%h][c] or \
           moving_down[(r-phase)%h][c]

def print_board(phase,row=None,col=None):
    for r in range(h):
        for c in range(w):
            if r!=None and r==row and c==col:
                print("E",end='')
            else:
                count = 0
                p = '.'
                if moving_left[r][(c+phase)%w]:
                    count+=1
                    p = '<'
                if moving_right[r][(c-phase)%w]:
                    count+=1
                    p = '>'
                if moving_up[(r+phase)%h][c]:
                    count+=1
                    p = '^'
                if moving_down[(r-phase)%h][c]:
                    count+=1
                    p = 'v'
                if count > 1:
                    print(count,end='')
                else:
                    print(p,end='')
        print()

def do_search(start_step,start_phase,startr,startc,goalr,goalc):
    #state is (phase, row, column) -> step
    seen_state = {}

    #search state has (phase, row, column, step)
    #r,c of None,None is starting point
    search_state = deque()
    search_state.append( (start_phase,None,None,start_step) )
    i=0
    while search_state:
        phase,row,column,step = search_state.popleft()
        #print("-------Step",step,"--------")
        #print_board(phase,row,column)
        if i%10000==0:
            print(i,phase,row,column,step)
        i+=1
        if row==goalr and column==goalc:
            print(i,phase,"GOAL!!")
            break
        elif row==None:
            #waiting at entrance
            #print(i,"WAIT",phase,row,column,step)
            if step < phase_max:
                search_state.append( ((phase+1)%phase_max,None,None,step+1) )
                if not occupied(phase+1,startr,startc):
                    search_state.append( (phase+1,startr,startc,step+1) )
        elif (phase,row,column) not in seen_state or \
           seen_state[(phase,row,column)] > step:
            #print(i,"ADD",phase,row,column,step)
            seen_state[(phase,row,column)] = step
            step+=1
            phase = (phase+1)%phase_max
            for r,c in (row,column),(row,column+1),(row,column-1),(row+1,column),(row-1,column):
                if r>=0 and r<h and c>=0 and c<w:
                    if not occupied(phase,r,c):
                        search_state.append((phase,r,c,step))
        #else:
        #    print(i,"CULL",phase,row,column,step,seen_state[(phase,row,column)])
    return (step+1,(phase+1)%phase_max)

next_step,next_phase = do_search(0,0,0,0,h-1,w-1)
print(next_step)
next_step,next_phase = do_search(next_step,next_phase,h-1,w-1,0,0)
next_step,next_phase = do_search(next_step,next_phase,0,0,h-1,w-1)
print(next_step)
