
import heapq
from graph_structure import Graph
import geopy.distance

def dijkstra(graph: Graph, start: str, end: str, start_time, const_func):
    pq = []
    heapq.heappush(pq, (0, -1, start, [], None)) 
    visited = {}
    curr_time = start_time
    ordering = 0
    last_line = ""
    used_lines = 0
    
    while pq:
        cost, _, current, path, chosen_edge = heapq.heappop(pq)
        
        if current in visited and visited[current] <= cost:
            continue
        
        visited[current] = cost
        if chosen_edge is not None:
            path = path + [chosen_edge]
            curr_time = chosen_edge.end_t
            if last_line != chosen_edge.line:
                # print(type(last_line))
                last_line = chosen_edge.line
                used_lines += 1
        
        if current == end:
            return path, cost 
        
        for neighbor in graph.nodes[current].connected_nodes.keys():
            edge_cost, chosen_edge =  const_func(current, neighbor, curr_time, last_line, used_lines) 
            neighbor_cost = cost + edge_cost
            ordering += 1
            heapq.heappush(pq, (neighbor_cost, ordering, neighbor, path, chosen_edge))
    return None, float('inf')


def astar(graph: Graph, start: str, end: str, start_time, cost_func):
    end_coords = graph.get_coords(end)
    pq = []
    heapq.heappush(pq, (0, -1, start, [], None))
    visited = {}
    curr_time = start_time
    ordering = 0
    last_line = ""
    used_lines = 0
    
    while pq:
        cost, _, current, path, chosen_edge = heapq.heappop(pq)
        
        if current in visited and visited[current] <= cost:
            continue
        
        visited[current] = cost
        if chosen_edge is not None:
            path = path + [chosen_edge]
            curr_time = chosen_edge.end_t
            if last_line != chosen_edge.line:
                last_line = chosen_edge.line
                used_lines += 1
        
        if current == end:
            return path, cost 
        
        for neighbor in graph.nodes[current].connected_nodes.keys():
            edge_cost, chosen_edge =  cost_func(current, neighbor, curr_time, last_line, used_lines) 
            neighbor_coords =graph.get_coords(neighbor)
            neighbor_cost = cost + edge_cost + heuristic(neighbor_coords[0], neighbor_coords[1], end_coords[0], end_coords[1])
            ordering += 1
            heapq.heappush(pq, (neighbor_cost, ordering, neighbor, path, chosen_edge))
    return None, float('inf')


def heuristic(start_lat, start_lon, end_lat, end_lon):
    return geopy.distance.distance((start_lat, start_lon), (end_lat, end_lon)).km * 60.0 / 15.0

