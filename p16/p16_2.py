import re
from collections import deque

#values are [flow, [lead_to]]
valves = dict()

for l in open("example"):
    m = re.match(r"Valve (..) has flow rate=(\d+); .* valves? (.*)", l)
    v = m[1]
    r = int(m[2])
    to = re.findall(r"[A-Z]+",m[3])
    valves[v] = [r,to]

#state is (move, score, ele_score, cur_valve, ele_valve, (enabled_valves), {valve:best_score}, {ele_valve:best_score})
search_states = deque()
search_states.append((1,0,0,'AA','AA',(),{},{}))
MAX_MOVE=26
best_score=0
best_possible=0
best_valves = ()
culled=0

def best_possible_score(score,move,valve,e_valve,enabled_valves,ele=False):
    if move >= MAX_MOVE:
        return score
    valve_val=valves[valve][0]
    openable = valve_val > 0 and valve not in enabled_valves and (not ele or e_valve != valve)
    e_valve_val=valves[e_valve][0]
    e_openable = e_valve_val > 0 and e_valve not in enabled_valves and (ele or e_valve != valve)
    rates = []
    for vn,v in valves.items():
        if v[0] > 0 and vn not in enabled_valves and vn != valve and vn != e_valve:
            rates.append(v[0])
    rates.sort(reverse=True)
    m=move+1 if ele else move
    e_m=move

    #if user/elephant are in a node with a usable valve, assume they open it first
    if openable:
        score += valve_val*(MAX_MOVE-m)
        m+=2
    else:
        m+=1
    if e_openable:
        score += e_valve_val*(MAX_MOVE-e_m)
        e_m+=2
    else:
        e_m+=1
    
    for r in range(0,len(rates),2):
        #simulate 2 simultaneous valve openings
        if ele:
            score += rates[r]*(MAX_MOVE-e_m)
            if r+1<len(rates) and m<MAX_MOVE:
                score += rates[r+1]*(MAX_MOVE-m)
            e_m+=2
            m+=2
            if e_m>=MAX_MOVE:
                break
        else:
            score += rates[r]*(MAX_MOVE-m)
            if r+1<len(rates) and e_m<MAX_MOVE:
                score += rates[r+1]*(MAX_MOVE-e_m)
            e_m+=2
            m+=2
            if m>=MAX_MOVE:
                break
        
    return score

def get_moves(state,ele=False):
    global best_score
    global best_valves
    global best_possible
    global culled
    m,s,es,v,ev,e,bs,ebs=state

    #determine best possible score by imagining this node is connected
    #to all other unopened ones in a perfect sequence
    best_possible=best_possible_score(s+es,m,v,ev,e,ele)
        
    if best_possible <= best_score:
        #print("cull due to best possible score",b,"less than best score",best_score)
        culled+=1
        return []

    if ele:
        ov=v
        obs=bs
        v=ev
        bs=ebs
        os=s
        (s,es)=(es,s)

    if v not in bs:
        bs=dict(bs)
        bs[v]=s
        
    new_states=[]
    valve_val=valves[v][0]
    openable = valve_val > 0 and v not in e
    
    if openable:
        #enable valve (only if non-zero), update best score
        open_score=valve_val*(MAX_MOVE-m)
        new_valves=e+(v,)
        ns=s+open_score
        if es+ns >= best_score:
            best_score = es+ns
            best_valves = new_valves
        nbs=dict(bs)
        nbs[v]=ns
        if ele:
            new_states.append((m+1,os,ns,ov,v,new_valves,obs,nbs))
        else:
            new_states.append((m,ns,es,v,ev,new_valves,nbs,ebs))

    #actions during mintue 30 don't affect score, so cull here
    if m==MAX_MOVE-1:
        return []
    
    for n in valves[v][1]:
        #move to valve (only if score has improved since last visit)
        if n in bs and s<=bs[n]:
            culled+=1
        else:
            if ele:
                new_states.append((m+1,os,s,ov,n,e,obs,bs))
            else:
                new_states.append((m,s,es,n,ev,e,bs,ebs))
    
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
    
    
