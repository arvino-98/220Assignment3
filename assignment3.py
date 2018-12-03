'''
Arvin Aya-ay
Programming Assignment 3
'''

import networkx as nx
inputFile = 'sample_in.txt'

rawInputArray = []
with open(inputFile) as f:
    for line in f:
        rawInputArray.append(line.split())

'''
Print Utilities
////////////////////////////////////////////////////////
'''
'''
printMultilineAdjList()
Prints adjacency list line-by-line
'''
def printMultilineAdjList(G):
    for line in nx.generate_multiline_adjlist(G):
        print(line)

'''
printTestGraphArr()
Prints a given array of graphs
'''
def printTestGraphArr(testCaseGraphs):
    testCaseNumber = 1
    for i in testCaseGraphs:
        print("Test Case " + str(testCaseNumber))
        printMultilineAdjList(i)
        testCaseNumber += 1
'''
End print utilities
////////////////////////////////////////////////////////
'''

'''
validRoute()
Returns whether a route is valid.
That is, its departure is not earlier than 18:00
and its arrival is no later than 6:00
'''
def validRoute(departureTime, travelTime):
    arrivalTime = departureTime + travelTime
    if (departureTime <= 6):
        return arrivalTime <= 6
    elif (departureTime >= 18 and departureTime <= 24):
        return arrivalTime <= 30
    else:
        return False

'''
normalizedArrivalTime()
Return arrival time according to departure and travel times
'''
def normalizedArrivalTime(time):
    if time == 24:
        return time
    else:
        return time % 24

'''
addNodesAndEdge()
Adds an edge and its corresponding nodes and info to a graph G
Weight is initialized to -1
'''
def addNodesAndEdge(G, source, destination, departureTime, travelTime):
    # check if valid route first
    if validRoute(departureTime, travelTime):
        # if destination in graph
        if destination in G:
            # check if its coming from a new source
            if source not in G.nodes:
                G.add_node(source, earliestArrivalTime = departureTime)
            # if the new arrival time is < than the old one, overwrite it
            if (normalizedArrivalTime(departureTime+travelTime) < normalizedArrivalTime(G.nodes[destination]['earliestArrivalTime'])):
                #print("overwrite")

                G.add_edge(source, destination, departureTime=departureTime, travelTime = travelTime, weight=-1)
                G.nodes[destination]['earliestArrivalTime'] = (departureTime+travelTime)

            #print("destination in G, possible overwrite [" + source + " " + destination + "]" + "[" + str(G.nodes[source]['earliestArrivalTime']) + " " + str(G.nodes[destination]['earliestArrivalTime']) + "]")
        # if source in graph (and destination isn't)
        elif source in G:
            G.add_node(destination, earliestArrivalTime = (departureTime+travelTime))
            G.add_edge(source, destination, departureTime=departureTime, travelTime = travelTime, weight=-1)

            #print("source in G, new destination  [" + source + " " + destination + "]" + "[" + str(G.nodes[source]['earliestArrivalTime']) + " " + str(G.nodes[destination]['earliestArrivalTime']) + "]")
        # else both source and destination not in graph
        elif (source, destination) not in G.edges:
            G.add_node(source, earliestArrivalTime = departureTime)
            G.add_node(destination, earliestArrivalTime = (departureTime+travelTime))
            G.add_edge(source, destination, departureTime=departureTime, travelTime = travelTime, weight=-1)

            #print("source nor destination in G  [" + source + " " + destination + "]" + "[" + str(G.nodes[source]['earliestArrivalTime']) + " " + str(G.nodes[destination]['earliestArrivalTime']) + "]")

    #else:
        #print("Not a valid route")

'''
weightGraph()
Adjusts each edge of the graph to proper weight
'''
def weightGraph(G):
    for (u, v) in G.edges:
        edgeDeparture = (G.edges[u,v]['departureTime'])
        earliestArrivalTime = G.nodes[u]['earliestArrivalTime']

        # special case if arrival ran over into next day
        # and departure is early
        if earliestArrivalTime >= 24 and edgeDeparture <= 6:
            earliestArrivalTime = earliestArrivalTime % 24

        if edgeDeparture < earliestArrivalTime:
            G.edges[u, v]['weight'] = 1
        else:
            G.edges[u, v]['weight'] = 0

        #print(G.edges[u, v])

'''
litersConsumed()
Return string specifying number of liters required
'''
def litersConsumed(G, source, target):
    if target not in G:
        return "There is no route Vladimir can take."

    else:
        shortestPath = nx.shortest_path(G, source=source, target=target, weight='weight')
        #print(shortestPath)

        total = 0
        for i in range(len(shortestPath) - 1):
            edgeWeight = G.edges[shortestPath[i],shortestPath[i + 1]]["weight"]
            total += edgeWeight

        return "Vladimir needs " + str(total) + " litre(s) of blood."

'''
Parsing input into graphs
////////////////////////////////////////////////////////
'''
# testCaseGraphs will hold each graph created by each test case from input file.
# testCaseGraphsSourceAndTarget maps 1 to 1 with testCaseGraphs, specifying the
# source and target for each test case.
testCaseGraphs = []
testCaseGraphsSourceAndTarget = []

# number of test cases is always first line of input
numOfTestCases = int(rawInputArray[0][0])

# we will iterate in such a way that the value of lineNum always
# represents a line number that gives the number of route specifications.
# we init is as 1 to start from the second line (since the first line specifies # of test cases)
lineNum = 1
for i in range(numOfTestCases):
    #print("test case " + str(i + 1))
    G = nx.DiGraph()
    # get int value from the line
    valueAtLineNum = int(rawInputArray[lineNum][0])
    # slice array from first route specification to source and target specification
    testCaseSlice = rawInputArray[lineNum + 1:(lineNum + valueAtLineNum + 2)]
    sliceLength = len(testCaseSlice)
    # last line of slice contains the source and target
    SourceAndTarget = testCaseSlice[sliceLength - 1]
    testCaseGraphsSourceAndTarget.append(SourceAndTarget)

    # for each row of input in a slice
    for j in range(sliceLength - 1):
        source = testCaseSlice[j][0]
        destination = testCaseSlice[j][1]
        departureTime = int(testCaseSlice[j][2])
        travelTime = int(testCaseSlice[j][3])

        addNodesAndEdge(G, source, destination, departureTime, travelTime)

    weightGraph(G)

    testCaseGraphs.append(G)
    #print("End test case\n")

    # iterate to next line that contains a number of route specification
    lineNum += (valueAtLineNum + 2)
'''
End parsing
////////////////////////////////////////////////////////
'''

'''
Writing to output file
////////////////////////////////////////////////////////
'''
output = open("output.txt", "w")
for i, graph in enumerate(testCaseGraphs):
    source = testCaseGraphsSourceAndTarget[i][0]
    target = testCaseGraphsSourceAndTarget[i][1]
    tc = "Test case " + str(i + 1) + "."
    lc = litersConsumed(graph, source, target)
    #print(tc)
    #print(lc)
    output.write(tc + '\n')
    output.write(lc + '\n')
'''
End writing
////////////////////////////////////////////////////////
'''
