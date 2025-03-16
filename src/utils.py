from graph_structure import Edge

def pretty_print(stops: list[Edge]):
    start_time = ""
    start_stop = ""
    end_time = ""
    end_stop = ""
    last_line: str = ""
    for i, s in enumerate(stops):
        if last_line != s.line:
            if last_line != "":
                end_stop = stops[i - 1].end_s
                end_time = stops[i -1].end_t.strftime("%H:%M")

                print(last_line.upper() + ": " + start_stop.title() + " - " + start_time + " ---> " + end_stop.title() + " - " + end_time)
            last_line = s.line
            start_stop = s.start_s
            start_time = s.start_t.strftime("%H:%M")
    
    end_stop = stops[-1].end_s
    end_time = stops[-1].end_t.strftime("%H:%M")
    print(last_line.upper() + ": " + start_stop.title() + " - " + start_time + " ---> " + end_stop.title() + " - " + end_time)

