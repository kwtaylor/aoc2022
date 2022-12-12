import re

DEBUG = False

#DO_REDUCE = False
#ROUNDS = 20
#worrychange = lambda w: w.div_by(3)
DO_REDUCE = True
ROUNDS = 10000
worrychange = lambda w: w

def printd(s):
    if DEBUG:
        print(s)

#this seems like more work than it should be
#here's a class that stores various mod N versions of a number and lets you manipulate it
class MultiMod:
    def __init__(self, val, do_reduce=True):
        self.initval = val
        self.modified = False
        self.moddict = {}
        self.do_reduce = do_reduce

    def __str__(self):
        return str(self.moddict)

    def __repr__(self):
        return repr(self.moddict)

    def addmod(self, mod):
        if self.modified:
            raise RuntimeError("Cannot add mod factor after value has been modified!")
        self.moddict[mod] = self.initval

    def getmodval(self, mod):
        return self.moddict[mod]
        
    def reduce(self, m):
        if self.do_reduce and self.moddict[m] >= m:
            redval = self.moddict[m] % m
            printd(f"    *item val {self.moddict[m]} reduced mod {m} to {redval}")
            self.moddict[m] = redval

    def add_to(self, val):
        self.modified = True
        for m in self.moddict:
            self.moddict[m] += val
            self.reduce(m)
    
    def mul_by(self, val):
        self.modified = True
        for m in self.moddict:
            self.moddict[m] *= val
            self.reduce(m)

    def div_by(self, val):
        self.modified = True
        for m in self.moddict:
            self.moddict[m] //= val
            self.reduce(m)

    def square(self):
        self.modified = True
        for m in self.moddict:
            self.moddict[m] *= self.moddict[m]
            self.reduce(m)


#fine i'll do OOP
class Monkey:
    def __init__(self):
        self.items = []
        self.op = None
        self.throw_t = 0
        self.throw_n = 0
        self.divby = 1

    def __str__(self):
        return " ".join(map(str, [self.items, self.throw_t, self.throw_n, self.divby, self.op]))

    #operand is either a number or "old"
    #returns integer or "None" if "old"
    #raises ValueError otherwise
    @staticmethod
    def parse_operand(token):
        if token.isdigit():
            return int(token)
        elif token == "old":
            return None
        else:
            raise ValueError(f"invalid operand: {token}")

    #opstring must be "operand operator operand" separated by whitespace
    #operand is a number or "old"
    #operator is + or *
    #sets self.op to the lambda(old) of the operation
    def set_op(self, op_string):
        tokens = op_string.split()
        if len(tokens) != 3:
            raise ValueError(f"Invalid op syntax: incorrect number of tokens in {op_string}")
        
        if tokens[0] != "old":
            raise ValueError(f"Left operand must be 'old', not {tokens[0]}")
        op_right = self.parse_operand(tokens[2])

        if tokens[1] == "+":
            self.op = lambda old, r=op_right: old.add_to(r)
        elif tokens[1] == "*":
            if op_right:
                self.op = lambda old, r=op_right: old.mul_by(r)
            else:
                self.op = lambda old: old.square()
        else:
            raise ValueError(f"Invalid operator: {tokens[1]}")


    #removes first item, applies op, then applies worrychange
    #tests value based on test and throws to either throw_t or throw_n
    #returns (monkey_num, item_worry)
    def inspect_and_throw(self, worrychange):
        item_worry = self.items.pop(0)
        printd(f"  Monkey inspects an item with a worry level of {item_worry.getmodval(self.divby)}")
        printd(item_worry)
        self.op(item_worry)
        printd(f"    Worry level increases to {item_worry.getmodval(self.divby)}")
        worrychange(item_worry)
        printd(f"    Monkey gets bored with item. Worry level is now {item_worry.getmodval(self.divby)}")
        printd(item_worry)

        if item_worry.getmodval(self.divby) % self.divby == 0:
            printd(f"    Current worry level is divisible by {self.divby}.")
            t = self.throw_t
        else:
            printd(f"    Current worry level is not divisible by {self.divby}.")
            t = self.throw_f

        printd(f"    Item with worry level {item_worry.getmodval(self.divby)} is thrown to monkey {t}")
        return (t, item_worry)

monkeys = []
mods = []

with open("input") as f:
    for l in f:
        #really dumb parser time. whitespace is required
        tokens = l.split()
        if len(tokens) < 1:
            continue
        if tokens[0] == "Monkey":
            m = Monkey()
            monkeys.append(m)
        elif tokens[0] == "Starting":
            for t in tokens[2:]:
                item = int(re.search(r"\d+", t).group())
                monkeys[-1].items.append(MultiMod(item, DO_REDUCE))
        elif tokens[0] == "Operation:":
            monkeys[-1].set_op(" ".join(tokens[3:]))
        elif tokens[0] == "Test:":
            if tokens[1] != "divisible":
                raise ValueError(f"unknown test {tokens[1]}")
            divby = int(tokens[3])
            mods.append(divby)
            print(divby)
            monkeys[-1].divby = divby
        elif tokens[0] == "If":
            if tokens[1] == "true:":
                monkeys[-1].throw_t = int(tokens[5])
            elif tokens[1] == "false:":
                monkeys[-1].throw_f = int(tokens[5])
            else:
                raise ValueError(f"unknown test result {tokens[1]}")

for m in monkeys:
    for i in m.items:
        for d in mods:
            i.addmod(d)
    print(m)

inspect = [0 for m in monkeys]

for r in range(ROUNDS):
    printd(f"ROUND {r}")
    for m in monkeys:
        printd(m.items)
    for (n,m) in enumerate(monkeys):
        printd(f"Monkey {n}:")
        while len(m.items) > 0:
            inspect[n] += 1
            (t,w) = m.inspect_and_throw(worrychange)
            monkeys[t].items.append(w)

print()

for m in monkeys:
    print(m.items)

print()
print(inspect)
inspect.sort()

mbusiness = inspect[-1]*inspect[-2]
print(mbusiness)
