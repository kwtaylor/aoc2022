import re

DEBUG = False

def printd(s):
    if DEBUG:
        print(s)

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
        
        op_left = self.parse_operand(tokens[0])
        op_right = self.parse_operand(tokens[2])

        if tokens[1] == "+":
            theop = lambda a,b: a+b
        elif tokens[1] == "*":
            theop = lambda a,b: a*b
        else:
            raise ValueError(f"Invalid operator: {tokens[1]}")

        if op_left and op_right:
            #constant function... weird
            self.op = lambda old, l=op_left, r=op_right: theop(l, r)
        elif op_left:
            self.op = lambda old, l=op_left: theop(l, old)
        elif op_right:
            self.op = lambda old, r=op_right: theop(old, r)
        else:
            self.op = lambda old: theop(old,old)

    #removes first item, applies op, then applies worrychange
    #tests value based on test and throws to either throw_t or throw_n
    #returns (monkey_num, item_worry)
    def inspect_and_throw(self, worrychange):
        item_worry = self.items.pop(0)
        printd(f"  Monkey inspects an item with a worry level of {item_worry}")
        item_worry = self.op(item_worry)
        printd(f"    Worry level increases to {item_worry}")
        item_worry = worrychange(item_worry)
        printd(f"    Monkey gets bored with item. Worry level is now {item_worry}")

        if item_worry % self.divby == 0:
            printd(f"    Current worry level is divisible by {self.divby}.")
            t = self.throw_t
        else:
            printd(f"    Current worry level is not divisible by {self.divby}.")
            t = self.throw_f

        printd(f"    Item with worry level {item_worry} is thrown to monkey {t}")
        return (t, item_worry)

monkeys = []
#I had thought of doing LCM but it was buggy and gave me the wrong answer. So I abandoned.
#I should have had confidence in myself!
LCM = 1

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
                monkeys[-1].items.append(item)
        elif tokens[0] == "Operation:":
            monkeys[-1].set_op(" ".join(tokens[3:]))
        elif tokens[0] == "Test:":
            if tokens[1] != "divisible":
                raise ValueError(f"unknown test {tokens[1]}")
            divby = int(tokens[3])
            if LCM % divby != 0:
                LCM *= divby
            print(divby, LCM)
            monkeys[-1].divby = divby
        elif tokens[0] == "If":
            if tokens[1] == "true:":
                monkeys[-1].throw_t = int(tokens[5])
            elif tokens[1] == "false:":
                monkeys[-1].throw_f = int(tokens[5])
            else:
                raise ValueError(f"unknown test result {tokens[1]}")

for m in monkeys:
    print(m)

inspect = [0 for m in monkeys]

ROUNDS = 10000
worrychange = lambda w: w % LCM

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
