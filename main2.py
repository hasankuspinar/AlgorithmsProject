import networkx as nx
import random
import matplotlib.pyplot as plt
import time

def find_max_independent_set(graph):
    best_independent_set = set()  #stores the largest independent set found
    vertices = list(graph.nodes())  #list of vertices in the graph
    #for recording the time
    start_time = time.time ()

    for initial_vertex in vertices:
        independent_set = set()  #independent set for the current iteration
        independent_set.add(initial_vertex)

        #add neighbors of the initial vertex to the independent set if feasible
        neighbors = list(graph.neighbors(initial_vertex))
        for neighbor in neighbors:
            if all(not graph.has_edge(neighbor, node) for node in independent_set):
                independent_set.add(neighbor)

        #update adjacency matrix by removing edges adjacent to nodes in the independent set and their neighbors
        temp_graph = graph.copy()
        nodes_to_remove = set(independent_set)
        for node in independent_set:
            if node in temp_graph:  
                nodes_to_remove.update(temp_graph.neighbors(node))
        temp_graph.remove_nodes_from(nodes_to_remove)

        #repeat the improvement process
        while temp_graph.number_of_edges() > 0:
            #find the vertex with the maximum degree
            max_degree_vertex = max(temp_graph.degree, key=lambda x: x[1])[0]

            #add neighbors of the maximum degree vertex if feasible
            neighbors = list(temp_graph.neighbors(max_degree_vertex))
            for neighbor in neighbors:
                if all(not graph.has_edge(neighbor, node) for node in independent_set):
                    independent_set.add(neighbor)

            #update the adjacency matrix
            nodes_to_remove = set(independent_set)
            for node in independent_set:
                if node in temp_graph:  
                    nodes_to_remove.update(temp_graph.neighbors(node))
            temp_graph.remove_nodes_from(nodes_to_remove)

        #try to add remaining vertices to the independent set
        for vertex in graph.nodes():
            if vertex not in independent_set and all(
                neighbor not in independent_set for neighbor in graph.neighbors(vertex)
            ):
                independent_set.add(vertex)

        #try shifting vertices to create feasible additions
        for vertex in vertices:
            if vertex not in independent_set:
                neighbors = list(graph.neighbors(vertex))
                for neighbor in neighbors:
                    if neighbor in independent_set and len(neighbors) == 1:
                        independent_set.remove(neighbor)
                        independent_set.add(vertex)
                        break

        #update the best independent set if the current one is larger
        if len(independent_set) > len(best_independent_set):
            best_independent_set = independent_set

    #calculating the total time taken by the algorithm
    end_time = time.time ()
    total_time = end_time - start_time

    return best_independent_set,total_time

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
    
    filename = f" heuristic_graph_{len(G.nodes())}_{len(G.edges())}_{edge_probability}_{total_time:.10f}_{len(independent_set)}.png"
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