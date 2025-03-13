
import heapq
from graph_structure import Graph
import geopy.distance

def dijkstra(graph: Graph, start: str, end: str, start_time):
    pq = []
    heapq.heappush(pq, (0, -1, start, [], None)) 
    visited = {}
    curr_time = start_time
    ordering = 0
    
    while pq:
        cost, _, current, path, chosen_edge = heapq.heappop(pq)
        
        if current in visited and visited[current] <= cost:
            continue
        
        visited[current] = cost
        if chosen_edge is not None:
            path = path + [chosen_edge]
            curr_time = chosen_edge.end_t
        
        if current == end:
            return path, cost 
        
        for neighbor in graph.nodes[current].connected_nodes.keys():
            edge_cost, chosen_edge =  graph.get_time_cost(current, neighbor, curr_time) 
            neighbor_cost = cost + edge_cost
            ordering += 1
            heapq.heappush(pq, (neighbor_cost, ordering, neighbor, path, chosen_edge))
    return None, float('inf')


def astar(graph: Graph, start: str, end: str, start_time):
    end_coords = graph.get_coords(end)
    pq = []
    heapq.heappush(pq, (0, -1, start, [], None))
    visited = {}
    curr_time = start_time
    ordering = 0
    
    while pq:
        cost, _, current, path, chosen_edge = heapq.heappop(pq)
        
        if current in visited and visited[current] <= cost:
            continue
        
        visited[current] = cost
        if chosen_edge is not None:
            path = path + [chosen_edge]
            curr_time = chosen_edge.end_t
        
        if current == end:
            return path, cost 
        
        for neighbor in graph.nodes[current].connected_nodes.keys():
            edge_cost, chosen_edge =  graph.get_time_cost(current, neighbor, curr_time) 
            neighbor_coords =graph.get_coords(neighbor)
            neighbor_cost = cost + edge_cost + heuristic(neighbor_coords[0], neighbor_coords[1], end_coords[0], end_coords[1])
            ordering += 1
            heapq.heappush(pq, (neighbor_cost, ordering, neighbor, path, chosen_edge))
    return None, float('inf')


def heuristic(start_lat, start_lon, end_lat, end_lon):
    return geopy.distance.distance((start_lat, start_lon), (end_lat, end_lon)).km * 60.0 / 15.0

