import datetime
import os
import pickle
import pandas as pd
from collections import defaultdict, namedtuple

use_cols = ["line", "departure_time", "arrival_time", 
                "start_stop", "end_stop", "start_stop_lat", "start_stop_lon", 
                "end_stop_lat", "end_stop_lon"]
Rowtuple = namedtuple("Rowtuple", use_cols)

class Edge:
    def __init__(self, data: namedtuple):
        self.line: str = data.line
        dep_time = str(int(data.departure_time[:2]) % 24) + data.departure_time[2:]
        arr_time = str(int(data.arrival_time[:2]) % 24) + data.arrival_time[2:]
        
        self.start_t: datetime.time = datetime.datetime.strptime(dep_time, '%H:%M:%S').time()
        self.end_t: datetime.time = datetime.datetime.strptime(arr_time, '%H:%M:%S').time()
        self.start_s: str = data.start_stop
        self.end_s: str = data.end_stop
        self.start_lat: float = data.start_stop_lat
        self.start_lon: float = data.start_stop_lon
        self.end_lat: float = data.end_stop_lat
        self.end_lon: float = data.end_stop_lon

class NodeB:
    def __init__(self):
        self.connecting_edges: list[Edge] = []

    def update(self, entry: namedtuple):
        self.connecting_edges.append(Edge(entry))

class NodeA:
    def __init__(self):
        self.connected_nodes: dict[NodeB] = defaultdict(NodeB)

    def update(self, entry: namedtuple):
        if entry.end_stop not in self.connected_nodes:
            self.connected_nodes[entry.end_stop] = NodeB()
        self.connected_nodes[entry.end_stop].update(entry)

class Graph:
    def __init__(self):
        self.nodes: dict[NodeA] = defaultdict(NodeA)

def get_raw_data_from_csv() -> set:
    csv_file = "data/raw.csv"
    
    
    df = pd.read_csv(csv_file, usecols=use_cols)
    no_dupls =  set(df.itertuples(index=False, name="Rowtuple"))
    stop_coords = defaultdict(set)

    for row in no_dupls:
        stop_coords[row.start_stop].add((row.start_stop_lat, row.start_stop_lon))
        stop_coords[row.end_stop].add((row.end_stop_lat, row.end_stop_lon))

    average_coords = {
        stop: (sum(lat for lat, _ in coords) / len(coords), 
            sum(lon for _, lon in coords) / len(coords))
        for stop, coords in stop_coords.items()
    }

    updated_rows = set()

    for row in no_dupls:
        (line, dep_time, arr_time, start_stop, end_stop, 
        _, _, _, _) = row
        
        new_row = Rowtuple(
            line, dep_time, arr_time, start_stop, end_stop, 
            average_coords[start_stop][0], average_coords[start_stop][1], 
            average_coords[end_stop][0], average_coords[end_stop][1]
        )
        
        updated_rows.add(new_row)
    return updated_rows

def get_structure_from_set(source_set: set) -> Graph:
    graph = Graph()
    for entry in source_set:
        if entry.start_stop not in graph.nodes:
            graph.nodes[entry.start_stop] = NodeA()
        graph.nodes[entry.start_stop].update(entry)
    return graph



# Filepath for the pickle file
pickle_file = "data/.cached.pkl"

# Check if the pickle file exists
if os.path.exists(pickle_file):
    print("Pickle file exists. Loading data...")
    with open(pickle_file, "rb") as f:
        graph = pickle.load(f)
else:
    print("Pickle file does not exist. Creating new pickle file...")
    # Create an instance of the class
    
    rows = get_raw_data_from_csv()
    graph = get_structure_from_set(rows)
    # Save it to a pickle file
    with open(pickle_file, "wb") as f:
        pickle.dump(graph, f)

print(len(graph.nodes))
print(len(graph.nodes["Paprotna"].connected_nodes["Obornicka (Wołowska)"].connecting_edges))

# print(list(rows)[:10], sep="\n")
# print(len(rows))
