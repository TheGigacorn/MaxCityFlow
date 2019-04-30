import decimal
import math
import time

def max_flow(C, s, t):
    ## implemented precondition
    assert(len(C) > 1)
    for i in range(len(C)):
        for n in range(len(C)):
            assert(C[i][n] >= 0)
            assert(isinstance(C[i][n], !str))

    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in range(n)] # flow matrix
    path = bfs(C, F, s, t) # path equal to shortest availible path found by bfs
    #  print path
    while path != None: #while there is still an availible path
        flow = min(C[u][v] - F[u][v] for u,v in path)
        for u,v in path:
            F[u][v] += flow
            F[v][u] -= flow
        path = bfs(C, F, s, t)
        print('{}'.format(path))
    return sum(F[s][i] for i in range(n))

#find path by using BFS
def bfs(C, F, s, t):
    queue = [s]
    paths = {s:[]}
    if s == t:
        return paths[s]
    while queue: 
        u = queue.pop(0)
        for v in range(len(C)):
                if(C[u][v]-F[u][v]>0) and v not in paths:
                    paths[v] = paths[u]+[(u,v)]
                    #print(paths)
                    if v == t:
                        return paths[v]
                    queue.append(v)
    return None



filearray = [] # array to hold 
cityname = []
population = []
latitude = [] #latitude and longitude are decimal degree form
longitude = []
distance = [] #distance is calculated in miles
R = 3961
with open("mocities.dat","r") as data: #opens .dat file for file reading
    for x in data:
        filearray.append(x) # appends each line into an array for easier splitting
    for y in filearray:
        if y.find(',') != -1: #if row with names
            cityname.append(y[:y.find(',')])
        if y.find('+') != -1: #if row with population, latitude, longitude
            population.append(y[:y.find('+')-1])
            latitude.append(y[y.find('+')+1:y.find('+')+3] + '.' + y[y.find('+')+3:y.find('-')-1])
            longitude.append(y[y.find('-'):y.find('-')+4] + '.' + y[y.find('-')+4:y.find('\n')])
data.close()


#       Equation that converts lat-long to distance in miles        #
adjacencyMat = [[0 for i in range(len(latitude))] for j in range(len(longitude))] # creates an adjacency matrix

#adjacencyMatOut = [[0 for i in range(len(latitude))] for j in range(len(longitude))] # creates an adjacency matrix

for i in range(0, len(latitude)):
    for j in range(0, len(longitude)):
        p = 0.017453292519943295     #Pi/180
        a = 0.5 - math.cos((float(latitude[j]) - float(latitude[i])) * p)/2 + math.cos(float(latitude[i]) * p) * math.cos(float(latitude[j])* p) * (1 - math.cos((float(longitude[j]) - float(longitude[i])) * p)) / 2
        d= 7922 * math.asin(math.sqrt(a))
        if d <= 15: #if distance is less than 30 miles it has a direct connection
            adjacencyMat[i][j] = d #matrix inputing

adjacencyMatFlow = [[0 for i in range(len(latitude))] for j in range(len(longitude))]

data = open('adjacencyMat.txt', "w")
for i in range(len(cityname)):
    data.write('{}\n'.format(adjacencyMat[i]))
data.close()

## driver Code  ##
for i in range(len(cityname)):
    for n in range(len(cityname)):
        if adjacencyMat[i][n] != 0:
            adjacencyMatFlow[i][n] = 1

totaltime = 0
source = 448
sink = 781
timestart = time.time()
max_flow = max_flow(adjacencyMatFlow, source, sink)
totaltime = totaltime + (time.time() - timestart)
print(max_flow)
print('time in seconds: {}'.format(totaltime))

