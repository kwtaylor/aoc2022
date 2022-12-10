score = 0

with open("input") as f:
    for l in f:
        if l[2] == "X":
            #lose
            score += 0
        elif l[2] == "Y":
            #tie
            score += 3
        elif l[2] == "Z":
            #win
            score += 6
        else:
            print("HUH???")

        if l[2] == "X" and l[0] == "B" or \
           l[2] == "Y" and l[0] == "A" or \
           l[2] == "Z" and l[0] == "C":
            #rock
            score += 1
        elif l[2] == "X" and l[0] == "C" or \
             l[2] == "Y" and l[0] == "B" or \
             l[2] == "Z" and l[0] == "A":
            #paper
            score += 2
        else:
            #scissor
            score += 3

        #print(f"Score: {score}")

print(score)

