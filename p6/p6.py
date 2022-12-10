
def is_marker(s):
    return len(set(s)) == len(s)


with open("input") as f:
    signal = f.readline()

signal = signal.strip()

TEST_LEN=14

for i in range(len(signal)):
    test_mkr = signal[i:i+TEST_LEN]
    #print(i,test_mkr)
    if is_marker(test_mkr):
        break

print(i+TEST_LEN)
