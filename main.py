import random
import time
import networkx as nx
import matplotlib.pyplot as plt

def is_independent_set(graph,subset):
    for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                # Check if there's an edge between any two nodes in the subset
                if graph.has_edge(subset[i], subset[j]):
                    return False
    return True


def find_max_independent_set(graph):
    #for recording the time
    start_time = time.time ()
    max_independent_set = []
    
    #initialize a subset list containing the empty subset
    subsets = [[]]
    
    #create a list to store vertices from the graph
    vertices = list(graph.nodes())
    
    #generate all subsets by adding each vertex to existing subsets
    for vertex in vertices:
        temp_subsets = []
        
        #add the current vertex to each existing subset to create new subsets
        for subset in subsets:
            temp_subset = subset + [vertex]
            temp_subsets.append(temp_subset)
        
        #add new subsets to the list of all subsets
        subsets.extend(temp_subsets)
    
    #iterating over each subset ot find the max
    for subset in subsets:
        #check if the subset is an independent set and the len of the subset is bigger than the max
        if is_independent_set(graph,subset) and len(subset) > len(max_independent_set):
            max_independent_set = subset

    #calculating the total time taken by the algorithm
    end_time = time.time ()
    total_time = end_time - start_time

    return max_independent_set, total_time

def generate_random_graph(num_vertices, edge_probability):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                G.add_edge(i, j)
    
    return G

def plot_graph_with_independent_set(G, independent_set, edge_probability, total_time):
    pos = nx.spring_layout(G)  
    
    filename = f" graph_{len(G.nodes())}_{len(G.edges())}_{edge_probability}_{total_time:.6f}_{len(independent_set)}.png"
    # Draw vertices with different colors for the independent set and other vertices
    vertex_colors = ['lightblue' if vertex not in independent_set else 'orange' for vertex in G.nodes]
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color=vertex_colors, node_size=500, font_size=10, font_color='black', edge_color='gray')
    
    # Highlight vertices in the independent set
    nx.draw_networkx_nodes(G, pos, nodelist=independent_set, node_color='orange')
    
    plt.title("Graph with Maximum Independent Set Highlighted")
    plt.savefig(filename)

    plt.show()

def main():
    for i in range(20):
        num_vertices = int(input(f"Enter the number of vertices for graph {i+1}: "))
        edge_probability = float(input(f"Enter the edge probability for graph {i+1} (between 0 and 1): "))
        
        G = generate_random_graph(num_vertices, edge_probability)
        print("Generated Graph Edges:", list(G.edges()))

        max_independent_set, total_time = find_max_independent_set(G)
        print("Maximum Independent Set:", max_independent_set)
        print("Size of Maximum Independent Set:", len(max_independent_set))

        plot_graph_with_independent_set(G, max_independent_set, edge_probability, total_time)

if __name__ == "__main__":
    main()