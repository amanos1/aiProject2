#reads all 100 files in the ground_truth folder
import math

class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

    def get_state(self):
        return self.state

    def is_blocked(self):
        return self.state == BLOCKED

    def get_local(self):
        return self.x, self.y

graph = []
heatmap = []
locs = []
plocs = []
cloc = []
for x in range(100):
    cloc.append(0)
dirs = []
obs = []
error = []
for x in range(100):
    error.append(0)
start = (0,0)
rows = 50
columns = 100
NORMAL = 'N'
HIGHWAY = 'H'
HARD_TO_TRAVERSE = 'T'
BLOCKED = 'B'
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

def printmap():
    g = graph
    for x in g:
        print(x.get_state(),end="")
        if x.x==columns-1:
            print()
def printheat():
    g = heatmap
    t = max(g)
    if g == heatmap:
        for x in range(len(g)):
            if g[x]==t:
                print('\033[1m'+'[{:.5f}%]'.format(g[x] * 100)+'\033[0m', end=" ")
                #print("{:.3f}%".format(g[x] * 100), end=" ")
            else:
                print("{:.6f}%".format(g[x]*100),end=" ")
            if graph[x].x==columns-1:
                print()
def readmap(filename):
    f = open(filename, "r")
    str = f.read()
    for x in range(len(str)):
        if str[x] == NORMAL or str[x] == HIGHWAY or str[x] == HARD_TO_TRAVERSE or str[x] == BLOCKED:
            graph.append(Cell(int(x/2) % columns, int(int(x/2) / columns), str[x]))
    f.close()
    for x in range(len(graph)):
        graph[x].x = x%columns
        graph[x].y = int(x/columns)
def readgtruth(filename):
    f = open(filename, "r")
    temp = f.readline().split()
    start = (int(temp[0]),int(temp[1]))
    #get locations
    for i in range(100):
        str = f.readline().split()
        locs.append((int(str[0]),int(str[1])))
    #get directions
    for i in range(100):
        str = f.readline()
        dirs.append(str[0])
    #get observations
    for i in range(100):
        str = f.readline()
        obs.append(str[0])
    f.close()
def initheatmap():
    count = 0
    for x in graph:
        if x.state==BLOCKED:
            count+=1
    chance = 1/(rows*columns-count)
    for x in graph:
        if x.state!=BLOCKED:
            heatmap.append(chance)
        else:
            heatmap.append(0.0)
def predict(a,s):
    tempheatmap = heatmap.copy()
    if a==RIGHT:
        for x in range(len(heatmap)):
            if graph[x].state!=BLOCKED:
                if graph[x].x==columns-1:
                    heatmap[x] = tempheatmap[x-1]*.9 + tempheatmap[x]
                elif graph[x].x==0:
                    if graph[x+1].state==BLOCKED:
                        heatmap[x]=tempheatmap[x]*1
                    else:
                        heatmap[x]=tempheatmap[x]*0.1
                else:
                    if graph[x+1].state!=BLOCKED:
                        heatmap[x]=tempheatmap[x]*.1+tempheatmap[x-1]*.9
                    else:
                        heatmap[x] = tempheatmap[x]+tempheatmap[x-1]*.9
    elif a==LEFT:
        for x in range(len(heatmap)):
            if graph[x].state != BLOCKED:
                if graph[x].x==columns-1:
                    if graph[x-1].state==BLOCKED:
                        heatmap[x]= tempheatmap[x]*1
                    else:
                        heatmap[x]= tempheatmap[x]*.1
                elif graph[x].x==0:
                    heatmap[x] = tempheatmap[x+1]*.9 + tempheatmap[x]
                else:
                    if graph[x-1].state!=BLOCKED:
                        heatmap[x] = tempheatmap[x]*.1 + tempheatmap[x+1] * .9
                    else:
                        heatmap[x] = tempheatmap[x]+tempheatmap[x+1]*.9
    elif a==UP:
        for x in range(len(heatmap)):
            if graph[x].state != BLOCKED:
                if graph[x].y==0:
                    heatmap[x]=tempheatmap[x]*1 + tempheatmap[x+columns]*.9
                elif graph[x].y==rows-1:
                    if graph[x-columns].state==BLOCKED:
                        heatmap[x]=tempheatmap[x]*1
                    else:
                        heatmap[x]=tempheatmap[x]*.1
                else:
                    if graph[x-columns].state!=BLOCKED:
                        heatmap[x] =tempheatmap[x]*.1+ tempheatmap[x+columns] * .9
                    else:
                        heatmap[x] = tempheatmap[x]+tempheatmap[x+columns]*.9
    elif a==DOWN:
        for x in range(len(heatmap)):
            if graph[x].state != BLOCKED:
                if graph[x].y==rows-1:
                    heatmap[x] = tempheatmap[x-columns]*.9 + tempheatmap[x]
                elif graph[x].y==0:
                    if graph[x+columns].state==BLOCKED:
                        heatmap[x]=tempheatmap[x]*1
                    else:
                        heatmap[x]=tempheatmap[x]*.1
                else:
                    if graph[x+columns].state!=BLOCKED:
                        heatmap[x] = tempheatmap[x]*.1+ tempheatmap[x-columns] * .9
                    else:
                        heatmap[x] = tempheatmap[x]+tempheatmap[x-columns]*.9
    for x in range(len(heatmap)):
        if graph[x].state==s:
            heatmap[x]*=0.9
        else:
            heatmap[x]*=0.05
    normalize()
def normalize():
    sum = 0.0
    for x in heatmap:
        sum+=x
    for x in range(len(heatmap)):
        heatmap[x] = heatmap[x]/sum
def findmax():
    m = max(heatmap)
    p = 0
    for x in range(len(heatmap)):
        if heatmap[x]==m:
            p = x
            break
    return(p%100,int(p/100))
def pcycle():
    for x in range(len(obs)):
        predict(dirs[x],obs[x])
        #if x==9:
            #printheat()
        plocs.append(findmax())
        if plocs[x]==locs[x]:
            cloc[x]+=1
        if x>4:
            error[x] += math.dist(locs[x],plocs[x])
        else:
            error[x] = 0
def finderror():
    for i in range(len(error)):
        error[i]  = error[i]/len(error)
        cloc[i] = cloc[i]/len(cloc)
def clearall():#clears all but graph
    heatmap.clear()
    locs.clear()
    plocs.clear()
    dirs.clear()
    obs.clear()
    start = (0, 0)
def readall():
    for i in range(10):
        readmap(f"ground_truth/map{i}.txt")
        for j in range(10):
            readgtruth(f"ground_truth/map{i}test{j}.txt")
            initheatmap()
            pcycle()
            clearall()
        graph.clear()
def printEandC():
    for x in range(len(error)):
        print(x + 1, end=" ")
        print(error[x],end=" ")
    print()
    for x in range(len(cloc)):
        print(x + 1, end=" ")
        print(cloc[x],end=" ")
if __name__ == '__main__':
    readall()
    finderror()
    #printEandC()
    #readmap("ground_truth/map0.txt")
    #readgtruth("ground_truth/map0test0.txt")
    #initheatmap()
    #pcycle()

    if False:
        graph.append(Cell(0,0,HIGHWAY))
        graph.append(Cell(1, 0, HIGHWAY))
        graph.append(Cell(2, 0, HARD_TO_TRAVERSE))

        graph.append(Cell(0, 1, NORMAL))
        graph.append(Cell(1, 1, NORMAL))
        graph.append(Cell(2, 1, NORMAL))

        graph.append(Cell(0, 2, NORMAL))
        graph.append(Cell(1, 2, BLOCKED))
        graph.append(Cell(2, 2, HIGHWAY))
        dirs.append(RIGHT)
        dirs.append(RIGHT)
        dirs.append(DOWN)
        dirs.append(DOWN)
        obs.append(NORMAL)
        obs.append(NORMAL)
        obs.append(HIGHWAY)
        obs.append(HIGHWAY)
