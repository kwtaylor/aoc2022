def compare(a, b):
    #print(a,b)
    a_int = type(a) is int
    b_int = type(b) is int
    if a_int and b_int:
        return b-a
    elif a_int:
        return compare([a],b)
    elif b_int:
        return compare(a,[b])
    elif len(a) == 0:
        return len(b)
    else:
        for (n, i) in enumerate(a):
            if n < len(b):
                c = compare(i, b[n])
                if c != 0:
                    return c
            else:
                return -1
        return 0

right_order_sum = 0
pair = 1
                
with open("input") as f:
    for l in f:
        a=eval(l.strip())
        b=eval(f.readline().strip())
        c = compare(a,b)
        print(c)
        if c >= 0:
            right_order_sum += pair
        f.readline()
        pair += 1

print()
print(right_order_sum)


#part 2
import functools

all_packets = [[[2]],[[6]]]

for l in open("input"):
    l = l.strip()
    if len(l)>0:
        all_packets.append(eval(l))

all_packets.sort(reverse=True, key=functools.cmp_to_key(compare))
print("\n".join(map(str,enumerate(all_packets))))

all_packets = list(map(str, all_packets))
k1 = all_packets.index("[[2]]")+1
k2 = all_packets.index("[[6]]")+1

print(k1, k2, k1*k2)

