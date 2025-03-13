
import pandas as pd
from collections import defaultdict
from graph_structure import Graph, NodeA
from constants import *
import csv

def format_csv() -> None:
    with open(data_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = [[cell.lower() for cell in row] for row in reader]
    
    with open(formated_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


def get_data_from_csv() -> set:
    df = pd.read_csv(formated_file, usecols=use_cols)
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
        formated_name = entry.start_stop
        if formated_name not in graph.nodes:
            graph.nodes[formated_name] = NodeA()
        graph.nodes[formated_name].update(entry)
    return graph
