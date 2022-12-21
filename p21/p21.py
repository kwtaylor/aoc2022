#name -> [number, [mokneya, operand, monkeyb]]
monkeys = {}
#name -> [list of monkeys that depend on]
depends = {}

import re
from collections import deque

#monkeys that are leaf nodes (have available number)
leafs = deque()

for l in open("input"):
    name,expr = re.split(": ", l.strip())
    
    if expr[0].isdigit():
        monkeys[name]=[int(expr),None]
        leafs.append(name)
    else:
        a,op,b=re.split("\s+",expr)
        monkeys[name]=[None,[a,op,b]]
        for d in a,b:
            if d not in depends:
                depends[d]=[name]
            else:
                depends[d].append(name)

#bottoms up!
while leafs:
    l = leafs.popleft()
    if l=="root":
        break;
    n = monkeys[l][0]
    for d in depends[l]:
        m = monkeys[d]
        ready = True
        for i in (0,2):
            if m[1][i] == l:
                m[1][i] = n
            elif not type(m[1][i]) is int:
                ready = False
        if ready:
            a,op,b = m[1]
            if op == "+":
                m[0] = a+b
            elif op == "*":
                m[0] = a*b
            elif op == "-":
                m[0] = a-b
            elif op == "/":
                m[0] = a//b
            else:
                print("Unknown operator",op,"in monkey",d)
            leafs.append(d)

print(monkeys["root"])
