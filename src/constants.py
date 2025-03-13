from collections import namedtuple

pickle_file = "data/.cached.pkl"

data_file = "data/raw.csv"

use_cols = ["line", "departure_time", "arrival_time", 
                "start_stop", "end_stop", "start_stop_lat", "start_stop_lon", 
                "end_stop_lat", "end_stop_lon"]

Rowtuple = namedtuple("Rowtuple", use_cols)
