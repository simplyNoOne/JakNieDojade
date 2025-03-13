import os
import pickle
from process_data import *
from constants import *
from graph_structure import *
from algorithms import dijkstra


def main():
    if os.path.exists(pickle_file):
        print("Pickle file exists. Loading data...")
        with open(pickle_file, "rb") as f:
            graph = pickle.load(f)
    else:
        print("Pickle file does not exist. Creating new pickle file...")
        
        rows = get_raw_data_from_csv()
        graph = get_structure_from_set(rows)
        with open(pickle_file, "wb") as f:
            pickle.dump(graph, f)

    print(graph.get_first_for("Paprotna", "Irysowa").line)
        
    print(len(graph.nodes))
    print(len(graph.nodes["Paprotna"].connected_nodes["Obornicka (Wołowska)"].connecting_edges))

    start_time = datetime.datetime.strptime("11:56:00", "%H:%M:%S")

    path, cost = dijkstra(graph, "Paprotna", "Lawendowa", start_time)

    for p in path:
        print(p.line, p.start_s, p.start_t,p.end_s, p.end_t, sep=", ")
    print(cost)


if __name__ == "__main__":
    main()
