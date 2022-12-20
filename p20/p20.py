#index into mixed array from original file order
index = []
#mixed array is of pairs (num, original index)
mixed = []

i=0
for l in open("input"):
    n = int(l.strip())
    if n==0:
        izero=i
    index.append(i)
    mixed.append((n,i))
    i+=1

num = len(index)
print(num)
print(mixed)

#part 1
for i in range(0,num):
    pop_i = index[i]
    n,orig_i = mixed.pop(pop_i)
    push_i = pop_i + n
    #fixup wrap-around
    push_i += push_i//num
    push_i %= num
    mixed.insert(push_i,(n,orig_i))
    for fixup_i in range(0,num):
        #could technically optimize
        _,orig_i = mixed[fixup_i]
        index[orig_i] = fixup_i
    #print(mixed)

pzero = index[izero]
print(pzero,mixed[pzero])
n1000 = mixed[(pzero+1000) % num][0]
n2000 = mixed[(pzero+2000) % num][0]
n3000 = mixed[(pzero+3000) % num][0]

print(n1000,"+",n2000,"+",n3000,"=",n1000+n2000+n3000)
