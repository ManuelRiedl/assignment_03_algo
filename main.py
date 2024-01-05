import networkx as nx
import random
import matplotlib.pyplot as plt

class ColorNode:
    def __init__(self, id):
        self.id = id
        self.candidate_color =None
        self.selected_color= None
        self.neighbors= set()

def rmv_edges(graph):
    # Rmv random number of edges
    min_rmv = 1 / 8
    max_rmv = 5 / 8
    num = int(random.uniform(min_rmv, max_rmv) * graph.number_of_edges())
    for i in range(num):
        graph_coppy = graph.copy()
        edge_to_remove = random.choice(list(graph.edges))
        graph_coppy.remove_edge(*edge_to_remove)
        if nx.is_connected(graph_coppy):
            graph.remove_edge(*edge_to_remove)
        else:
            i-=1

def color_graph(graph,max_degree,num_nodes,draw_graph,comments):
    colored_nodes_count = 0
    print("Nodes-List:", graph.nodes)
    #remove some edges because the function  nx.random_regular_graph allways generates a graph where each node has the maximum degree
    rmv_edges(graph)
    print("Edges-List:", graph.edges)
    #Data structure for the algorithm
    colored_nodes = {node: ColorNode(node) for node in graph.nodes}
    #assign neigthbors in the data structure
    for node in graph.nodes:
        colored_nodes[node].neighbors.update(graph.neighbors(node))
    #as long as not all nodes have a color
    while colored_nodes_count < num_nodes:
        #candidate_color assignment
        for node in graph.nodes:
            #if the node has not selected a color it needs a color
            if colored_nodes[node].selected_color is None:
                color_pattern = set(range(max_degree + 1))
                #remove colors that are already choosen by its neightbors
                for neighbor in colored_nodes[node].neighbors:
                    if colored_nodes[neighbor].selected_color is not None:
                        if comments:
                            print(f"Node: {node} -- Discard color {colored_nodes[neighbor].selected_color} from color_pattern")
                        color_pattern.discard(colored_nodes[neighbor].selected_color)
                #choose a random color from the avaible colors
                colored_nodes[node].candidate_color = random.choice(list(color_pattern))
                if comments:
                    print(f"Node: {node} -- Selected color {colored_nodes[node].candidate_color} as a candidate_color")

        #selected_color assignment
        for node in graph.nodes:
            same = False
            #all nodes that do not have a selected color
            if colored_nodes[node].selected_color is None:
                #check if a neightbour has picked the same candidate_color
                for neighbor in colored_nodes[node].neighbors:
                    if colored_nodes[node].candidate_color == colored_nodes[neighbor].candidate_color:
                        if comments:
                            print(f"Node: {node} -- candidate_color {colored_nodes[node].candidate_color} is the same as choosen by neightbor {neighbor}")
                        same = True
                        break
                #if they have not picked the same color, assign the color
                if not same:
                    if comments:
                        print(f"Node: {node} -- Colored node with color {colored_nodes[node].candidate_color}")
                    colored_nodes[node].selected_color = colored_nodes[node].candidate_color
                    colored_nodes_count += 1
                else:
                    colored_nodes[node].candidate_color = None


    # Check for correctness
    for node in graph.nodes:
        for neighbor in colored_nodes[node].neighbors:
            #check if a neightbour has the same color as itself
            if colored_nodes[node].selected_color == colored_nodes[neighbor].selected_color:
                print("Error - Same color as neightbor!!")
                exit(1)
    print("\n\n\n---------------------Graph colored correctly------------------------------\n\n\n")
    if draw_graph:
        #Got the idea behind how to draw a graph with nx from stack overflow
        #https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
        node_colors = [colored_nodes[node].selected_color for node in graph.nodes]
        nx.draw(graph, with_labels=True, cmap=plt.get_cmap('jet'), node_color=node_colors)
        plt.show()




max_degree = 4
num_nodes = 30
#A regular graph is a graph where each node has the same number of neighbors
graph = nx.random_regular_graph(max_degree, num_nodes)

def main():
    print("Example 1: A small example with degree 4 and nodes 30 for easy readability in the graph\n")
    max_degree = 4
    num_nodes = 30
    draw_graph = True
    comments = True
    # A regular graph is a graph where each node has the same number of neighbors
    graph = nx.random_regular_graph(max_degree, num_nodes)
    color_graph(graph,max_degree,num_nodes,draw_graph,comments)
    print("\n\n\nExample 2: Degree 10 Nodes 100\n")
    max_degree = 10
    num_nodes = 100
    draw_graph = True
    comments = False
    # A regular graph is a graph where each node has the same number of neighbors
    graph = nx.random_regular_graph(max_degree, num_nodes)
    color_graph(graph, max_degree, num_nodes,draw_graph,comments)
    print("\n\n\nExample 3: Degree 25 Nodes 200\n")
    max_degree = 25
    num_nodes = 200
    # doenst work propeply with so many nodes
    draw_graph = False
    comments = False
    # A regular graph is a graph where each node has the same number of neighbors
    graph = nx.random_regular_graph(max_degree, num_nodes)
    color_graph(graph, max_degree, num_nodes,draw_graph,comments)
    print("\n\n\nExample 4: Degree 18 Nodes 500\n")
    max_degree = 18
    num_nodes = 500
    #doenst work propeply with so many nodes
    draw_graph = False
    comments = False
    # A regular graph is a graph where each node has the same number of neighbors
    graph = nx.random_regular_graph(max_degree, num_nodes)
    color_graph(graph, max_degree, num_nodes,draw_graph,comments)
if __name__ == "__main__":
    main()

