import networkx as nx
import numpy as np
import pandas as pd
from queue import PriorityQueue
from heuristic import *

def zones_as_numbers(zone):
    if zone == 'a':
        zone = 7
    if zone == 'b':
        zone = 8
    if zone == 'c':
        zone = 9
    if zone == 'd':
        zone = 9
    return int(zone)
def load_tube_data(filename):
    with open(filename) as csvfile:
        df = pd.read_csv(csvfile, skipinitialspace = True, quotechar = '"')
        data = df.to_numpy()
        tube_graph = nx.MultiGraph()
        for column in data:
            Start = column[0]; Finish = column[1]; Line = column[2]; Time = column[3]; mainZone = column[4]; secZone = column[5]
            mainZone = zones_as_numbers(mainZone)
            secZone = zones_as_numbers(secZone)
            tube_graph.add_node(Start, zone = mainZone)
            tube_graph.add_node(Finish, zone = secZone)
            tube_graph.add_edge(Start, Finish, key = Line, time = Time, line = Line)
        return tube_graph

def tube_heuristic(graph,  next, final, time, curr_line, next_line, link_time):
    next_zone = graph.nodes[next]['zone']
    final_zone = graph.nodes[final]['zone']
    new_time = 0
    if curr_line != next_line:
        new_time = 4
    new_time += link_time + time
    h = new_time + ((final_zone - next_zone)/2) **2
    return h, new_time, next_line

def heuristic_search(graph, curr, final, count = 0):
    visited = {curr:0}
    paths = PriorityQueue() 
    paths.put([0, [curr], None, 0])
    
    while paths:
        h, path, curr_line, time = paths.get()
        count+=1
        curr = path[-1]
        nodes_found = graph[curr]

        for node in nodes_found:
            for next_line in nodes_found[node]:
                h, new_time, new_line = tube_heuristic(graph, node, final, time, curr_line, next_line, nodes_found[node][next_line]['time'])
                if node == final:
                    return path + [final], count, new_time
                
                if (f'{node}{next_line}' not in visited) or (visited[f'{node}{next_line}']>time):
                    visited[f'{node}{next_line}'] = time
                    paths.put([h, path + [node], new_line, new_time])

def run():
    tube_data = load_tube_data('tubedata.csv')
    Start, Finish = 'Canada Water', 'Stratford'
    h_path, h_count, h_time = heuristic_search(tube_data, Start, Finish)
    print(h_path, h_count, h_time)


if __name__ == '__main__':
    run()