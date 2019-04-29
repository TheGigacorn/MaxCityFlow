import decimal
import math

def max_flow(C, s, t):
    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in range(n)]
    path = bfs(C, F, s, t)
    #  print path
    while path != None:
        flow = min(C[u][v] - F[u][v] for u,v in path)
        for u,v in path:
            F[u][v] += flow
            F[v][u] -= flow
        path = bfs(C, F, s, t)
        print('\n\n{}'.format(path))
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



class Graph_Matrix():
    def __init__(self, verticies): #creates a graph with verticies being set to the number passed to it and graph is initialized to be all 0 in a 2D matrix
        self.V = verticies
        self.graph = [[0 for x in range(verticies)] for y in range(verticies)]

    def printMST(self, parent):
        #print(self.graph)
        print("Edge \tWeight")
        for i in range (1,self.V):
                #print(cityname[parent[i]],"-",cityname[i],"\t",self.graph[i][parent[i]])
                adjacencyMatOut[parent[i]][i] = self.graph[i][parent[i]]

    def minKey(self, key, mstSet):
        minimum = float("inf")
        for v in range(self.V):
            if key[v] < minimum and mstSet[v] == False:
                minimum = key[v]
                min_index = v

        return min_index

    def primMST(self):
        key = [float("inf")] * self.V
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V
        parent[0] = -1
        for cout in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u
        self.printMST(parent)



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

adjacencyMatOut = [[0 for i in range(len(latitude))] for j in range(len(longitude))] # creates an adjacency matrix

for i in range(0, len(latitude)):
    for j in range(0, len(longitude)):
        p = 0.017453292519943295     #Pi/180
        a = 0.5 - math.cos((float(latitude[j]) - float(latitude[i])) * p)/2 + math.cos(float(latitude[i]) * p) * math.cos(float(latitude[j])* p) * (1 - math.cos((float(longitude[j]) - float(longitude[i])) * p)) / 2
        d= 7922 * math.asin(math.sqrt(a))
        if d <= 30: #if distance is less than 30 miles it has a direct connection
            adjacencyMat[i][j] = d #matrix inputing

adjacencyMatFlow = [[0 for i in range(len(latitude))] for j in range(len(longitude))]

#for i in range(len(cityname)):
    #print('{}\n'.format(adjacencyMat[i]))

g = Graph_Matrix(len(cityname))
g.graph = adjacencyMat
g.primMST()

## driver Code  ##
for i in range(len(cityname)):
    if cityname[i] == "Joplin city":
        print(i)
    if cityname[i] == "St. Louis city":
        print(i)
    for n in range(len(cityname)):
        if adjacencyMat[i][n] != 0:
            adjacencyMatFlow[i][n] = 1

source = 448
sink = 781

max_flow = max_flow(adjacencyMatFlow, source, sink)
print(max_flow)

