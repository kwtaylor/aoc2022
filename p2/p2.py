score = 0

with open("input") as f:
    for l in f:
        if l[2] == "X":
            #we play rock
            #print("Rock ", end="")
            score += 1
        elif l[2] == "Y":
            #we play paper
            #print("Paper ", end="")
            score += 2
        elif l[2] == "Z":
            #print("Scissors ", end="")
            #we play scissors
            score += 3
        else:
            print("HUH???")

        if l[2] == "X" and l[0] == "A" or \
           l[2] == "Y" and l[0] == "B" or \
           l[2] == "Z" and l[0] == "C":
            #tie
            #print("Ties! ", end="")
            score += 3
        elif l[2] == "X" and l[0] == "C" or \
             l[2] == "Y" and l[0] == "A" or \
             l[2] == "Z" and l[0] == "B":
            #win
            #print("Wins! ", end="")
            score += 6
        else:
            #lose
            #print("Loses! ", end="")
            score += 0

        #print(f"Score: {score}")

print(score)

