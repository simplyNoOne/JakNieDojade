
from collections import defaultdict, namedtuple
import datetime
from constants import *
from bisect import bisect

class Edge:
    def __init__(self, data: namedtuple):
        self.line: str = data.line
        if type(self.line) == int:
            self.line = str(self.line)
        dep_time = str(int(data.departure_time[:2]) % 24) + data.departure_time[2:]
        arr_time = str(int(data.arrival_time[:2]) % 24) + data.arrival_time[2:]
        self.start_t: datetime.datetime = datetime.datetime.strptime(dep_time, '%H:%M:%S')
        self.end_t: datetime.datetime = datetime.datetime.strptime(arr_time, '%H:%M:%S')
        self.start_s: str = data.start_stop.lower()
        self.end_s: str = data.end_stop.lower()
        self.start_lat: float = data.start_stop_lat
        self.start_lon: float = data.start_stop_lon
        self.end_lat: float = data.end_stop_lat
        self.end_lon: float = data.end_stop_lon
    
    def get_travel_time(self) -> float:
        diff = self.end_t - self.start_t
        return diff.seconds / 60.0

class NodeB:
    def __init__(self):
        self.connecting_edges: list[Edge] = []
        self.was_sorted = False

    def update(self, entry: namedtuple):
        self.connecting_edges.append(Edge(entry))

    def get_sorted_edges(self):
        if not self.was_sorted:
            self.connecting_edges = sorted(self.connecting_edges, key=lambda path: path.start_t)
            self.was_sorted = True
        return self.connecting_edges


class NodeA:
    def __init__(self):
        self.connected_nodes: dict[NodeB] = defaultdict(NodeB)
        self.lat = 0.0
        self.lon = 0.0

    def update(self, entry: namedtuple):
        formated_name = entry.end_stop
        if formated_name not in self.connected_nodes:
            self.connected_nodes[formated_name] = NodeB()
        self.connected_nodes[formated_name].update(entry)
        if self.lat == 0.0:
            self.lat = entry.start_stop_lat
            self.lon = entry.start_stop_lon

    def get_coords(self):
        return (self.lat, self.lon)

class Graph:
    def __init__(self):
        self.nodes: dict[NodeA] = defaultdict(NodeA)

    def get_first_for(self, a: str, b: str):
        connections = self.nodes[a].connected_nodes[b].connecting_edges
        if len(connections) > 0:
            return connections[0]
        return None
    
    def get_time_cost(self, start: str, end: str, time: datetime.datetime, last_line: str, used_lines: int) -> tuple[int, Edge]:
        possible_paths : list[Edge] = self.nodes[start].connected_nodes[end].get_sorted_edges()
        soonest = self.find_first_after(possible_paths, time)
        if soonest is None:
            soonest = possible_paths[0]
        time_cost = soonest.get_travel_time() + abs((soonest.start_t - time).seconds / 60.0)
        if soonest.line != last_line:
            time_cost += 15
        return time_cost, soonest
    
    def get_switch_cost(self, start: str, end: str, time: datetime.datetime, last_line: str, used_lines: int):
        possible_paths : list[Edge] = self.nodes[start].connected_nodes[end].get_sorted_edges()
        soonest = self.find_first_after(possible_paths, time)
        if soonest is None:
            soonest = possible_paths[0]
        time_cost = (soonest.get_travel_time() + abs((soonest.start_t - time).seconds / 60.0))
        if soonest.line != last_line:
            time_cost += 100 * used_lines
        return time_cost, soonest

    def find_first_after(self, paths: list[Edge], time: datetime.datetime):
        path_i = bisect(paths, time, key = lambda path: path.start_t)
        if paths[path_i - 1].start_t == time:
            return paths[path_i - 1]
        if path_i != len(paths):
            return paths[path_i]
        return None
    
    def get_coords(self, stop: str):
        return self.nodes[stop].get_coords()

