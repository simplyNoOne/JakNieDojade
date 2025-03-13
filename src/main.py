import os
import pickle
from process_data import *
from constants import *
from graph_structure import *
from algorithms import dijkstra, astar


def main():
    if os.path.exists(pickle_file):
        print("Pickle file exists. Loading data...")
        with open(pickle_file, "rb") as f:
            graph = pickle.load(f)
    else:
        print("Pickle file does not exist. Creating new pickle file...")
        
        if not os.path.exists(formated_file):
            print("Formating csv first...")
            format_csv()
        rows = get_data_from_csv()
        graph = get_structure_from_set(rows)
        with open(pickle_file, "wb") as f:
            pickle.dump(graph, f)



    start_time = datetime.datetime.strptime("07:56:00", "%H:%M:%S")

    print("DIJKSTRA")
    path, cost = dijkstra(graph, "pl. grunwaldzki", "dh astra", start_time)

    for p in path:
        print(p.line, p.start_s, p.start_t,p.end_s, p.end_t, sep=", ")
    print(cost)

    print("ASTAR")
    path, cost = astar(graph, "pl. grunwaldzki", "dh astra", start_time)

    for p in path:
        print(p.line, p.start_s, p.start_t,p.end_s, p.end_t, sep=", ")
    print(cost)


if __name__ == "__main__":
    main()
