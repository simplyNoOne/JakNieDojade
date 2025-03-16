import os
import sys
import pickle
from process_data import *
from constants import *
from graph_structure import *
from algorithms import dijkstra, astar
from utils import pretty_print

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



    start_time = datetime.datetime.strptime("12:26:00", "%H:%M:%S")

    print("DIJKSTRA1")
    path, cost = dijkstra(graph, "pl. bema", "dh astra", start_time, graph.get_time_cost)

    pretty_print(path)
    print(cost, file=sys.stderr)

    print("ASTAR1")
    path, cost = astar(graph, "pl. grunwaldzki", "michalczyka", start_time, graph.get_time_cost)

    pretty_print(path)
    print(cost, file=sys.stderr)

    print("DIJKSTRA2")
    path, cost = dijkstra(graph, "pl. grunwaldzki", "dh astra", start_time, graph.get_switch_cost)

    pretty_print(path)
    print(cost, file=sys.stderr)

    print("ASTAR2")
    path, cost = astar(graph, "pl. grunwaldzki", "michalczyka", start_time, graph.get_switch_cost)

    pretty_print(path)
    print(cost, file=sys.stderr)


if __name__ == "__main__":
    main()
