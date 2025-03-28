import os
import sys
import time
import pickle
import argparse
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

    parser = argparse.ArgumentParser(description="JakNieDojade")

    parser.add_argument('start_stop', type=str, help="Start station (A)")
    parser.add_argument('end_stop', type=str, help="End station (B)")
    parser.add_argument('arrival_time', type=str, help="Time of arrival at the start station (format: HH:MM)")
    parser.add_argument('criterion', type=str, choices=['t', 'p'], help="Optimization criterion: 't' for minimizing travel time, 'p' for minimizing line changes")

    args = parser.parse_args()

    start_time = datetime.datetime.strptime(args.arrival_time, "%H:%M")

    if args.criterion == "t":
        path, cost = dijkstra(graph, args.start_stop, args.end_stop, start_time, graph.get_time_cost)
    else:
        path, cost = astar(graph, args.start_stop, args.end_stop, start_time, graph.get_switch_cost)

    pretty_print(path)
    print("Cost function value: ", cost, file=sys.stderr)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds", file=sys.stderr)
