import sys

def countText(path):
    with open(path, 'r') as file:
        text = file.read()
        words = text.split()
        used = {}
        for word in words:
            if word in used:
                used[word] += 1
            else:
                used[word] = 1
        return used
def printNcount(count,path):
    data = sorted(countText(path).items(), key=lambda x: x[1], reverse=True)
    for i in range(count):
        print(data[i][0])

path = 'alice.txt'
num = 0
try:
    num = int(sys.argv[1])
except:
    print("did not provide the number")
printNcount(num,path)