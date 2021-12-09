import networkx as nx
import numpy as np
import pandas as pd
from bfs import *
from dfs import *
from ucs import *
from ucsimproved import *

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
        tube_graph = nx.Graph()
        for column in data:
            Start = column[0]; Finish = column[1]; Line = column[2]; Time = column[3]; mainZone = column[4]; secZone = column[5]
            mainZone = zones_as_numbers(mainZone)
            secZone = zones_as_numbers(secZone)
            tube_graph.add_node(Start, zone = mainZone)
            tube_graph.add_node(Finish, zone = secZone)
            tube_graph.add_edge(Start, Finish, time = Time, line = Line)
        return tube_graph


def run():
    tube_data = load_tube_data('tubedata.csv')
    # Start, Finish = 'Canada Water', 'Stratford'
    # Start, Finish = 'New Cross Gate', 'Stepney Green'
    Start, Finish = 'Ealing Broadway', 'Turnham Green'
    # Start, Finish = 'Baker Street', 'Wembley Park'
    bfs_path, bfs_count = bfs(tube_data, Start, Finish)
    bfs_time = 0
    for index, node  in enumerate(bfs_path):
        if index != 0:
            edge_data = tube_data.get_edge_data(bfs_path[index-1], node)
            bfs_time += edge_data['time']
    print(f'BFS - The Path: {bfs_path}  Explored Nodes: {bfs_count}   Journey Time: {bfs_time}')
    dfs_path, dfs_count = dfs(tube_data, Start, Finish)
    dfs_time = 0
    for index, node  in enumerate(dfs_path):
        if index != 0:
            edge_data = tube_data.get_edge_data(dfs_path[index-1], node)
            dfs_time += edge_data['time']
    print(f'DFS - The Path: {dfs_path}  Explored Nodes: {dfs_count}   Journey Time: {dfs_time}')
    ucs_path, ucs_count, ucs_time = ucs(tube_data, Start, Finish)
    print(f'UCS - The Path: {ucs_path}  Explored Nodes: {ucs_count}   Journey Time:  {ucs_time}')
    ucsimproved_path, ucsimproved_count, ucsimproved_time = ucsimproved(tube_data, Start, Finish)
    print(f'UCS Improved - The Path: {ucsimproved_path}  Explored Nodes: {ucsimproved_count}   Journey Time:  {ucsimproved_time}')

if __name__ == '__main__':
    run()