from graph_structure import Edge

def pretty_print(stops: list[Edge]):
    print("\n\t<===============================>")
    if stops is None or stops == []:
        print("\tNiestety nie udało się wytyczyć trasy.") 
        print("\n\t<===============================>")
        return
    start_time = ""
    start_stop = ""
    end_time = ""
    end_stop = ""
    last_line: str = ""
    print(f"\tOto twoja podróz z {stops[0].start_s.title()} do {stops[-1].end_s.title()}:\n")
    line_count = 0
    for i, s in enumerate(stops):
        if last_line != s.line:
            if last_line != "":
                line_count += 1
                end_stop = stops[i - 1].end_s
                end_time = stops[i -1].end_t.strftime("%H:%M")
                print(f"\t{line_count }.\t{last_line.upper()}:\t\t{start_stop.title()} - {start_time}\t\t ---> \t\t{end_stop.title()} - {end_time}")
            last_line = s.line
            start_stop = s.start_s
            start_time = s.start_t.strftime("%H:%M")
    line_count += 1
    end_stop = stops[-1].end_s
    end_time = stops[-1].end_t.strftime("%H:%M")
    print(f"\t{line_count}.\t{last_line.upper()}:\t\t{start_stop.title()} - {start_time}\t\t ---> \t\t{end_stop.title()} - {end_time}")
    print(f"\tLiczba przesiadek: {line_count - 1}. Czas podrózy: {int((stops[-1].end_t - stops[0].start_t).seconds / 60)} minut(y).")
    print("\t<===============================>\n")

