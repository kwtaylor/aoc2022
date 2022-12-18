import re
from collections import deque

#values are [flow, [lead_to]]
valves = dict()

for l in open("input"):
    m = re.match(r"Valve (..) has flow rate=(\d+); .* valves? (.*)", l)
    v = m[1]
    r = int(m[2])
    to = re.findall(r"[A-Z]+",m[3])
    valves[v] = [r,to]

print(valves)

def get_cost(start_valve):
    cost_to = dict()
    queue = deque()
    queue.append(start_valve)
    cost_to[start_valve] = 0
    while queue:
        v = queue.popleft()
        c=cost_to[v]
        for nv in valves[v][1]:
            if nv not in cost_to:
                cost_to[nv] = c+1
                queue.append(nv)
    return cost_to

#calculate cost to nodes, only for "good valves" and start point, to create a smaller network
#values are {lead_to:cost}
good_valves = dict()
START_VALVE = 'AA'

for vn,v in valves.items():
    if v[0] > 0 or vn==START_VALVE:
        good_valves[vn] = dict()
        costs = get_cost(vn)
        for cn,c in costs.items():
            if valves[cn][0] > 0:
                good_valves[vn][cn]=c

print(good_valves)

#state is (move, score, cur_valve, dist, ele_valve, ele_dist, (enabled_valves))
search_states = deque()
if valves[START_VALVE][0] == 0:
    #if broken valve at start, mark as enabled to simplify serach
    e = (START_VALVE,)
else:
    e = tuple()
search_states.append((1,0,START_VALVE,0,START_VALVE,0,e))
MAX_MOVE=26
best_score=0
best_possible=0
best_valves = ()
culled=0

def best_possible_score(score,move,enabled_valves):
    rates = []
    for vn,v in valves.items():
        if v[0] > 0 and vn not in enabled_valves:
            rates.append(v[0])
    rates.sort(reverse=True)
    m=move
    if m>=MAX_MOVE:
        return score
    for r in range(0,len(rates),2):
        #simulate 2 simultaneous valve openings
        score += rates[r]*(MAX_MOVE-m)
        if r+1<len(rates):
            score += rates[r+1]*(MAX_MOVE-m)
        m+=2
        if m>=MAX_MOVE:
            break
    return score

def get_moves(state,ele=False):
    global best_score
    global best_valves
    global best_possible
    global culled
    m,s,v,d,ev,ed,e=state

    #determine best possible score by imagining this node is connected
    #to all other unopened ones in a perfect sequence
    best_possible=best_possible_score(s,m,e)

    if best_possible <= best_score:
        #print("cull due to best possible score",b,"less than best score",best_score)
        culled+=1
        return []

    if ele:
        ev,v=v,ev
        ed,d=d,ed

    #move forward toward destination nodes
    if d>0:
        if d>ed:
            #other side reaches destination first
            d-=ed+1
            m+=ed
            if ele:
                if m+1 >= MAX_MOVE-1:
                    return []
                else:
                    return [(m+1,s,ev,0,v,d,e)]
            else:
                if m >= MAX_MOVE-1:
                    return []
                else:
                    return [(m,s,v,d,ev,0,e)]
        else:
            #we reach destination, continue below
            ed-=d
            m+=d

    #actions during last minute don't affect score, so cull here
    if m>=MAX_MOVE-1:
        return []
    
    valve_val=valves[v][0]
    openable = valve_val > 0 and v not in e

    #if openable, always open
    if openable:
        #enable valve (only if non-zero), update best score
        open_score=valve_val*(MAX_MOVE-m)
        new_valves=e+(v,)
        ns=s+open_score
        if ns >= best_score:
            best_score = ns
            best_valves = new_valves
        if ele:
            return [(m+1,ns,ev,ed,v,0,new_valves)]
        else:
            return [(m,ns,v,0,ev,ed,new_valves)]

    #else move to another openable valve
    new_states=[]
        
    for n,c in good_valves[v].items():
        #move to next openable valve
        if n in e:
            culled+=1
        else:
            if ele:
                new_states.append((m+1,s,ev,ed,n,c-1,e))
            else:
                new_states.append((m,s,n,c-1,ev,ed,e))
    
    return new_states

turn = 0
v_open = 0
b_score = 0
i=0
while search_states:
    cs = search_states.popleft()
    for m in get_moves(cs,False):
        for e in get_moves(m,True):
            search_states.append(e)
    if best_score > b_score or i%100000==0:
        b_score = best_score
        print("Best Score:",b_score,"Best Possible:",best_possible,"Turn:",cs[0],"Valves:",best_valves,"Culled:",culled,"Queue:",len(search_states),"Iter:",i)
    i+=1
    
    
