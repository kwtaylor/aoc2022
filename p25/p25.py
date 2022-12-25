def snafu_to_dec(snafu):
    tot = 0
    mul = 1
    for c in reversed(snafu):
        if c=='=':
            d=-2
        elif c=='-':
            d=-1
        else:
            d=int(c)
        tot+=d*mul
        mul*=5
    return tot

def dec_to_snafu(num):
    s=""
    while num>0:
        r=num%5
        if r==4:
            num=num+1
            c='-'
        elif r==3:
            num=num+2
            c='='
        else:
            num=num-r
            c=str(r)
        s = c+s
        num//=5
    return s

tot=0
for l in open("input"):
    tot += snafu_to_dec(l.strip())

print(dec_to_snafu(tot))
