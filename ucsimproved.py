import networkx as nx
from queue import PriorityQueue
import numpy as np

def ucsimproved(graph, curr, final, count = 0, station_time = 14):
    visited = {curr:0}
    paths = PriorityQueue() 
    paths.put([0, [curr], None])
    
    while paths:
        time, path, curr_line = paths.get()
        count+=1
        curr = path[-1]
        nodes_found = list(graph.neighbors(curr))
        
        for node in nodes_found:
            edge_data = graph.get_edge_data(curr, node)
            new_line = edge_data['line']
            new_time = 0
            if new_line != curr_line:
                new_time = station_time
            new_time += time + edge_data["time"]
            if node == final:
                return path + [final], count, new_time
            
            if (f'{node}{new_line}' not in visited) or (visited[f'{node}{new_line}']>time):
                visited[f'{node}{new_line}'] = time
                paths.put([new_time, path + [node], new_line])