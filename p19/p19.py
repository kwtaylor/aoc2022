import re
from collections import deque
from multiprocessing import Pool
from functools import partial, reduce
import operator

#0 bp#,
#1 ore robot ore,
#2 clay robot ore,
#3 obsidian robot ore
#4 obsidian robot clay
#5 geode robot ore
#6 geode robot obsidian
bps = []

for l in open("input"):
    bps.append(list(map(int,re.findall("\d+",l))))

print(bps)

#bp is bp-1
#state is
#(minutes_left, ore, clay, obsidian, ore_robots, clay_robots, obsidian_robots)
#returns [(state, score_increment)]
def moves_from_state(bp, state):
    (_, o_ro, c_ro, ob_ro, ob_rc, g_ro, g_rob) = bps[bp]
    #(o_ro, c_ro, ob_ro, ob_rc, g_ro, g_rob) = (4,2,3,14,2,7)
    (time_left, o, c, ob, o_r, c_r, ob_r) = state
    #increment ores
    n_o = o+o_r
    n_c = c+c_r
    n_ob = ob+ob_r
    n_tl = time_left - 1

    if n_tl < 0:
        return []

    next_states = []
    
    #null action
    next_states.append( ((n_tl, n_o, n_c, n_ob, o_r, c_r, ob_r),0) )

    #possible factory actions
    #make robot if enough source ore, but not so many to make more ore than you can use
    max_o_cost = max(o_ro, ob_ro, g_ro)
    #ore robot
    max_o_use = max_o_cost*n_tl
    max_o_make = o+o_r*n_tl
    if o >= o_ro and o_r < max_o_cost and max_o_make < max_o_use:
        next_states.append( ((n_tl, n_o-o_ro, n_c, n_ob, o_r+1, c_r, ob_r),0) )

    #clay robot
    max_c_use = ob_rc*n_tl
    max_c_make = c+c_r*n_tl
    if o >= c_ro and c_r < ob_rc and max_c_make < max_c_use:
        next_states.append( ((n_tl, n_o-c_ro, n_c, n_ob, o_r, c_r+1, ob_r),0) )

    #obsidian robot
    max_ob_use = g_rob*n_tl
    max_ob_make = ob+ob_r*n_tl
    if o >= ob_ro and c >= ob_rc and ob_r < g_rob and max_ob_make < max_ob_use:
        next_states.append( ((n_tl, n_o-ob_ro, n_c-ob_rc, n_ob, o_r, c_r, ob_r+1),0) )

    #geode robot (tally score)
    if o >= g_ro and ob >= g_rob:
        next_states.append( ((n_tl, n_o-g_ro, n_c, n_ob-g_rob, o_r, c_r, ob_r), n_tl) )

    return next_states

#best possible score from this state heuristic
def best_possible(bp, state, score):
    #assume one of each robot built every cycle if possible with ores collected
    #for now don't deduct any ores
    (_, o_ro, c_ro, ob_ro, ob_rc, g_ro, g_rob) = bps[bp]
    (time_left, o, c, ob, o_r, c_r, ob_r) = state

    for t in range(time_left,0,-1):
        #increment ores
        n_o = o+o_r
        n_c = c+c_r
        n_ob = ob+ob_r
        
        if o >= o_ro:
            o_r+=1

        if o >= c_ro:
            c_r+=1

        if o >= ob_ro and c >= ob_rc:
            ob_r+=1

        if o >= g_ro and ob >= g_rob:
            score += t
            
        o = n_o
        c = n_c
        ob = n_ob

    return score

#bp is bp-1
def find_best_score(bp, minutes):
    best_score = 0

    #queue entries are (state, score, best possible)
    state_queue = deque()
    first_state = (minutes, 0, 0, 0, 1, 0, 0)
    state_queue.append( (first_state, 0, best_possible(bp,first_state,0)) )
    
    cur_level = minutes+1
    i = 0

    while state_queue:
        (state, score, bestpos) = state_queue.popleft()

        if state[0] < cur_level:
            #dict stores state -> best score so far
            #(only keep track of next-timestep to save memory/lookup time)
            #(search goes one timestep at a time since BFS)
            best_at_state = dict()
            cur_level = state[0]

        #check bestpos again in case best_score has gone up
        if bestpos <= best_score:
            continue
        
        if i%10000 == 0:
            print("#",bp,i,"evaluating state",state,"with score",score,"best score",best_score,"best possible heuristic",bestpos)
        i+=1

        for n_state, add_score in moves_from_state(bp, state):
            n_score = score+add_score
            best_score=max(best_score,n_score)
            best_poss = best_possible(bp,n_state,n_score)
            if best_poss > best_score:
                if n_state not in best_at_state or best_at_state[n_state] < n_score:
                    best_at_state[n_state] = n_score
                    state_queue.append((n_state,n_score,best_poss))

    return best_score

#part 1
with Pool(8) as p:
    find_24 = partial(find_best_score, minutes=24)
    scores = list(p.map(find_24,range(len(bps))))
    scores = [scores[i] * bps[i][0] for i in range(len(bps))]
    print("QSUM:",sum(scores))

#part 2
with Pool(8) as p:
    find_32 = partial(find_best_score, minutes=32)
    scores = list(p.map(find_32,range(3)))
    print("PROD:",reduce(operator.mul,scores))

