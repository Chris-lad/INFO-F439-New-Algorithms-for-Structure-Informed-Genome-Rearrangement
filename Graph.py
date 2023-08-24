import math
import itertools

class Graph:
    def __init__(self):
        self.graph = {}
        self.weight = {}

    def add_node(self, node):
        self.graph[node] = []
        self.weight[node] = node.get_weight()

    def add_edge(self, start, end):
        if start in self.graph:
            self.graph[start].append(end)
        else:
            self.graph[start] = [end]
            self.weight[start] = start.get_weight()
        
        if end in self.graph:
            self.graph[end].append(start)
        else:
            self.graph[end] = [start]
            self.weight[end] = end.get_weight()
    
    def get_all_subsets_vertices(self):
        subsets = []
        for i in range(len(self.graph)+1):
            subsets.extend(itertools.combinations(self.graph.keys(), i))
        return subsets
    
    def is_vertex_cover(self, subset):
        for start in self.graph:
            for end in self.graph[start]:
                if start not in subset and end not in subset:
                    return False
        return True

    def get_weight_subset(self, subset):
        weight = 0
        for node in subset:
            weight += self.weight[node]
        return weight
        
    def get_minimum_vertex_cover_weight(self):
        min_value = math.inf
        vertex_cover = None
        subsets = self.get_all_subsets_vertices()
        for subset in subsets:
            if self.is_vertex_cover(subset):
                if self.get_weight_subset(subset) < min_value:
                    min_value = self.get_weight_subset(subset)
                    vertex_cover = subset
        return min_value, vertex_cover