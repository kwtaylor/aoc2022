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

#state is (move, score, cur_valve, (enabled_valves), {valve:best_score})
search_states = deque()
search_states.append((1,0,'AA',(),{}))
MAX_MOVE=30
best_score=0
best_possible=0
best_valves = ()

def best_possible_score(score,move,enabled_valves):
    rates = []
    for vn,v in valves.items():
        if v[0] > 0 and vn not in enabled_valves:
            rates.append(v[0])
    rates.sort(reverse=True)
    m=move
    for r in rates:
        score += v[0]*(MAX_MOVE-m)
        m+=2
        if m>=MAX_MOVE:
            break
    return score

def get_moves(state):
    global best_score
    global best_valves
    global best_possible
    m,s,v,e,bs=state

    best_possible=best_possible_score(s,m,e)
    if best_possible <= best_score:
        #print("cull due to best possible score",b,"less than best score",best_score)
        return []
    
    if v not in bs:
        bs=dict(bs)
        bs[v]=s
    new_states=[]
    
    if valves[v][0] > 0 and v not in e:
        #enable valve (only if non-zero), update best score
        ns=s+valves[v][0]*(MAX_MOVE-m)
        best_score = max(best_score,ns)
        best_valves = e+(v,)
        nbs=dict(bs)
        nbs[v]=ns
        new_states.append((m+1,ns,v,best_valves,nbs))

    #actions during mintue 30 don't affect score, so cull here
    if m==MAX_MOVE-1:
        return []
    
    for n in valves[v][1]:
        #move to valve (only if rate has improved since last visit)
        if n not in bs or s>bs[n]:
            new_states.append((m+1,s,n,e,bs))
    
    return new_states

turn = 0
v_open = 0
b_score = 0
while search_states:
    cs = search_states.popleft()
    for m in get_moves(cs):
        search_states.append(m)
    if best_score > b_score:
        b_score = best_score
        print("Best Score:",b_score,"Best Possible:",best_possible,"Turn",cs[0],"Valves:",best_valves)
    
    
