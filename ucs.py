import networkx as nx
from queue import PriorityQueue
import numpy as np

def ucs(graph, curr, final, count = 0):
    visited = {curr:0}
    paths = PriorityQueue() 
    paths.put([0, [curr]])
    while paths:
        time, path = paths.get()
        count+=1
        curr = path[-1]
        nodes_found = list(graph.neighbors(curr))

        for node in nodes_found:
            edge_data = graph.get_edge_data(curr, node)
            new_time = time + edge_data["time"]
            if node == final:
                return path + [final], count, new_time
            
            if (node not in visited) or (visited[node]>time):
                visited[node] = time
                paths.put([new_time, path + [node]])