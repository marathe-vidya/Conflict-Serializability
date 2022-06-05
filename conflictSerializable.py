"""
If a non-serial schedule is conflict equivalent to any serial schedule, then it is said to be conflict serializable.
Precedence graph should not contain any cycle, if it is acyclic then schedule is conflict serializable.
"""
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class ConflictSerializable:
    def __init__(self):
        self.G = nx.DiGraph()   # Directed Graph
        self.accessDict = {}    # Dictionary will store edges that are connected.
        self.nodes = []

    def checkConflictSerializability(self, inputFile, outputGraph):
        print("Parse the input file to obtain transactions of the schedule.")
        self.parseInput(inputFile=inputFile)
        print("Checking for conflict serializability")
        self.output(outputGraph=outputGraph)

    def addNodeToGraph(self, node):
        self.G.add_node(node)

    def addEdgeToGraph(self, fromNode, toNode):
        self.G.add_edge(u_of_edge=fromNode, v_of_edge=toNode)

    def parseInput(self, inputFile):
        # Read schedule from ods file
        data = pd.read_excel(inputFile) # reads data as dataframe
        print("Schedule is : ")
        print(data.fillna(""))   # Prettyprint the schedule, prints space instead of NaN

        # Initialise access dictionary with processes
        self.nodes = data.columns.values.tolist()    # Gives name of all the nodes, ie name and no. of transactions
        for proc in self.nodes:
            self.addNodeToGraph(node=proc)
            self.accessDict[proc] = []    # Initially all nodes have 0 edges.

        # Parse the data and read access values of all processes in the schedule and check for conflict.
        data = data.fillna(0)
        listedVal = data.values.tolist()
        for item in listedVal:
            for value in item:
                if value:
                    self.checkConflict(process=self.nodes[item.index(value)], access=value)

    def checkConflict(self, process, access):
        for node in self.accessDict:
            if process != node:
                # Check for R-W conflicts
                if access[0] == 'R' and 'W'+access[1:] in self.accessDict[node]:
                    self.addEdgeToGraph(fromNode=node, toNode=process)

                # Check for W-R and W-W conflicts
                elif access[0] == 'W':
                    if 'W' + access[1:] in self.accessDict[node] or 'R' + access[1:] in self.accessDict[node]:
                        self.addEdgeToGraph(fromNode=node, toNode=process)

        # Append current access into mapping
        self.accessDict[process].append(access)

    def output(self, outputGraph):
        # Print Precedence Graph.
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)
        nx.draw_networkx_edges(self.G, pos, arrows=True, connectionstyle='arc3,rad=0.2')
        plt.savefig(outputGraph)

        # Print Output to console.
        if len(list(nx.simple_cycles(self.G))):
            print("Precedence Graph is Cyclic, Schedule is NOT Conflict Serializable")
        else:
            print("Schedule is Conflict Serializable")

# ---------------------------------------------------------------------------------------------------
GRAPH_IMG = "precedenceGraph.png"
if __name__ == "__main__":
    inputFile = input("Enter Input filename : ")
    confSerial = ConflictSerializable()
    confSerial.checkConflictSerializability(inputFile=inputFile, outputGraph=GRAPH_IMG)
