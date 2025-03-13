
import pandas as pd
from collections import defaultdict
from graph_structure import Graph, NodeA
from constants import *


def get_raw_data_from_csv() -> set:    
    df = pd.read_csv(data_file, usecols=use_cols)
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
