from graph import Graph
from graph_samples import adjacency_matrix_samples


print("===== components part =====")

multi_component_graph = Graph(adjacency_matrix_samples[1])
components = multi_component_graph.components()

for component in components:
    print(*component)

print("=====eulerian cycle part =====")

not_eulerian_graph = Graph(adjacency_matrix_samples[5])
print("graph 5 is eulerian:", not_eulerian_graph.is_eulerian())

eulerian_graph = Graph(adjacency_matrix_samples[2])
print("graph 2 is eulerian:", eulerian_graph.is_eulerian())

eulerian_cycle = eulerian_graph.eulerian_cycle()
print("eulerian cycle:", *eulerian_cycle)

print("=====bipartite graph part =====")

not_bipartite_graph = Graph(adjacency_matrix_samples[2])
print("graph 2 is bipartite:", not_bipartite_graph.is_bipartite())

bipartite_graph = Graph(adjacency_matrix_samples[6])
print("graph 6 is bipartite:", bipartite_graph.is_bipartite())

bipartite_graph_parts = bipartite_graph.get_parts()
print("first part:", *bipartite_graph_parts[0])
print("second part:", *bipartite_graph_parts[1])
