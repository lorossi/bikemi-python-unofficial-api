import bikemi
b = bikemi.BikeMi()
bikes = b.getBikes()

newl = "\n"
tab = "\t"

string = ""
string += f"A total of {bikes['global_stats']['total_bikes']} bikes were found in {bikes['global_stats']['total_stations']} stations.{newl}"
string += f"Out of those, {bikes['global_stats']['bikes']} are normal, {bikes['global_stats']['electric_bikes']} are electic and {bikes['global_stats']['electric_bikes_child_seat']} are electric with a child seat.{newl}"
string += f"There are {bikes['global_stats']['bike_racks']} free bike racks. {newl}"
string += f"Complete list of stations:{newl}"
print(string)

for station in bikes["stations"]:
    string = ""
    string += f"Station {station['name']}, ID {station['ID']}, in coords {station['coordinates']['lat']}N, {station['coordinates']['lon']}E {newl}"
    string += f"{tab}Bikes: {station['bikes']['bikes']}{newl}"
    string += f"{tab}Electric bikes: {station['bikes']['electric_bikes']}{newl}"
    string += f"{tab}Electric bikes with child seat: {station['bikes']['electric_bikes_child_seat']}{newl}"
    string += f"{tab}Free racks: {station['bikes']['bike_racks']}{newl}"

    if station["probably_full"]:
        string += f"{tab}The station is probably full."
    elif station["probably_empty"]:
        string += f"{tab}The station is probably empty."

    print(string)


b.saveToFile("BikeMi.json")
