import networkx as nx
from collections import deque
import numpy as np
def bfs(graph, curr, final, count = 0):
    visited = [curr]
    paths = deque([[curr]]) 
    while paths:
        path = paths.popleft()
        curr = path[-1]
        nodes_found = list(graph.neighbors(curr))
        if final in nodes_found:
            return path + [final], count+1

        for node in nodes_found:
            if node not in visited:
                count += 1
                visited.append(node)
                paths.append(path + [node])