class Vertex:
    def __init__(self, v_id: int):
        self.id = v_id
        self.adjacent_vertices = []
        self.is_visited = False

    def is_adjacent_to(self, other):
        for adj_vertex in self.adjacent_vertices:
            if adj_vertex == other:
                return True

        return False

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "№" + str(self.id)


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def __eq__(self, other):
        return (self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2) or \
               (self.vertex1 == other.vertex2 and self.vertex2 == other.vertex1)


class Graph:
    def __init__(self, adjacency_matrix: list):
        n = len(adjacency_matrix)
        self.vertices = [Vertex(i) for i in range(n)]
        self.edges = []

        for i in range(n):
            for j in range(n):
                if adjacency_matrix[i][j]:
                    self.vertices[i].adjacent_vertices.append(self.vertices[j])

                    edge = Edge(self.vertices[i], self.vertices[j])

                    if edge not in self.edges:
                        self.edges.append(edge)

    def __compose_component_from_vertex(self, start_vertex: Vertex, component_array: list, all_vertices_list: list):
        component_array.append(start_vertex)

        del_index = all_vertices_list.index(start_vertex)
        del all_vertices_list[del_index]

        for adj_vertex in start_vertex.adjacent_vertices:
            if adj_vertex not in component_array:
                self.__compose_component_from_vertex(adj_vertex, component_array, all_vertices_list)

    def __vertex_is_deadlock(self, vertex: Vertex, current_edges_array: list):
        for adj_vertex in vertex.adjacent_vertices:
            if Edge(vertex, adj_vertex) in current_edges_array:
                return False

        return True

    def __edge_is_visited(self, vertex1: Vertex, vertex2: Vertex, current_edges_array: list):
        edge = Edge(vertex1, vertex2)
        return edge not in current_edges_array

    def __all_degs_are_even(self):
        for vertex in self.vertices:
            if len(vertex.adjacent_vertices) % 2 == 1:
                return False

        return True

    def components(self):
        vertices_copy = self.vertices.copy()
        graph_components = []

        while len(vertices_copy):
            component = []

            self.__compose_component_from_vertex(vertices_copy[0], component, vertices_copy)

            graph_components.append(component)

        return graph_components

    def is_eulerian(self):
        odd_vertices_amount = 0

        for vertex in self.vertices:
            if len(vertex.adjacent_vertices) % 2 == 1:
                odd_vertices_amount += 1

        if odd_vertices_amount > 2:
            return False

        components = self.components()
        not_empty_components_amount = 0

        for component in components:
            if len(component) > 1:
                not_empty_components_amount += 1

        if not_empty_components_amount > 1:
            return False

        return True

    def eulerian_cycle(self):
        if self.is_eulerian():
            path = []
            vertices_stack = []
            all_edges = self.edges.copy()

            start_vertex_index = 0

            if not self.__all_degs_are_even():
                while not len(self.vertices[start_vertex_index].adjacent_vertices) % 2:
                    start_vertex_index += 1

            current_vertex = self.vertices[start_vertex_index]
            vertices_stack.append(current_vertex)

            while len(all_edges):
                # print(current_vertex)
                if not self.__vertex_is_deadlock(current_vertex, all_edges):
                    first_unvisited_edge = None

                    for adj_vertex in current_vertex.adjacent_vertices:
                        if not self.__edge_is_visited(current_vertex, adj_vertex, all_edges):
                            first_unvisited_edge = Edge(current_vertex, adj_vertex)
                            current_vertex = adj_vertex
                            break

                    vertices_stack.append(current_vertex)
                    del all_edges[all_edges.index(first_unvisited_edge)]
                else:
                    while self.__vertex_is_deadlock(vertices_stack[-1], all_edges):
                        last_stack_vertex = vertices_stack.pop()
                        path.append(last_stack_vertex)

                        current_vertex = vertices_stack[-1]

            path.extend(reversed(vertices_stack))

            return path

        return None

    def __form_two_parts(self, component_current_vertex: Vertex, first_part: list, second_part: list,
                         append_to_first_part: bool):
        component_current_vertex.is_visited = True

        if append_to_first_part:
            first_part.append(component_current_vertex)
        else:
            second_part.append(component_current_vertex)

        for adj_vertex in component_current_vertex.adjacent_vertices:
            if not adj_vertex.is_visited:
                self.__form_two_parts(adj_vertex, first_part, second_part, not append_to_first_part)

    def __component_is_bipartite(self, component: list):
        first_part = []
        second_part = []

        self.__form_two_parts(component[0], first_part, second_part, True)

        for vertex in component:
            vertex.is_visited = False

        for i in range(1, len(first_part)):
            current_vertex = first_part[i]

            for j in range(0, i):
                if current_vertex.is_adjacent_to(first_part[j]):
                    return False

        for i in range(1, len(second_part)):
            current_vertex = second_part[i]

            for j in range(0, i):
                if current_vertex.is_adjacent_to(second_part[j]):
                    return False

        return True

    def is_bipartite(self):
        components = self.components()

        for component in components:
            if not self.__component_is_bipartite(component):
                return False

        return True

    def get_parts(self):
        components = self.components()

        if self.is_bipartite():
            first_part = []
            second_part = []

            first_component_part = []
            second_component_part = []

            for component in components:
                self.__form_two_parts(component[0], first_component_part, second_component_part, True)

                for vertex in component:
                    vertex.is_visited = False

                first_part.extend(first_component_part)
                second_part.extend(second_component_part)

                first_component_part = []
                second_component_part = []

            return first_part, second_part

        return None

    def __str__(self):
        graph_str = ""

        for vertex in self.vertices:
            graph_str += str(vertex) + "\n"

        return graph_str
