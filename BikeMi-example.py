import bikemi

b = bikemi.BikeMi()
bikes = b.getBikes()

newl = "\n"
tab = "\t"

string = ""
string += f"The whole search took {bikes['elapsed_time']} seconds. "
string += f"Timestamp: {bikes['timestamp']}{newl}"
string += f"A total of {bikes['global_stats']['bikes']['total_bikes']} bikes have been found.{newl}"
string += f"Out of those, {bikes['global_stats']['bikes']['bikes']} are normal, {bikes['global_stats']['bikes']['electric_bikes']} are electric and {bikes['global_stats']['bikes']['electric_bikes_child_seat']} are electric with a child seat.{newl}"
string += f"There are {bikes['global_stats']['bikes']['bike_racks']} free bike racks. {newl}"
string += f"A total of {bikes['global_stats']['stations']['total_stations']} stations have been found.{newl}"
string += f"Out of those, {bikes['global_stats']['stations']['full']} are full, {bikes['global_stats']['stations']['empty']} are empty, {bikes['global_stats']['stations']['probably_full']} might be full and {bikes['global_stats']['stations']['probably_empty']} might be empty.{newl}"
string += f"Complete list of stations:{newl}"
print(string)

for station in bikes["stations"]:
    string = ""
    string += f"Station {station['name']}, ID: {station['ID']}, in coords {station['coordinates']['lat']}°N, {station['coordinates']['lon']}°E {newl}"
    string += f"{tab}Bikes: {station['bikes']['bikes']}{newl}"
    string += f"{tab}Electric bikes: {station['bikes']['electric_bikes']}{newl}"
    string += f"{tab}Electric bikes with child seat: {station['bikes']['electric_bikes_child_seat']}{newl}"
    string += f"{tab}Free racks: {station['bikes']['bike_racks']}{newl}"

    if station["status"]["full"]:
        string += f"{tab}The station is full.{newl}"
    elif station["status"]["empty"]:
        string += f"{tab}The station is empty.{newl}"
    elif station["status"]["probably_full"]:
        string += f"{tab}The station is probably empty.{newl}"
    elif station["status"]["probably_empty"]:
        string += f"{tab}The station is probably empty.{newl}"

    string += f"{tab}Icon used: {station['icon']['name']}{newl}"
    print(string)

# find closest station to coordinates
lat = 45.4692247
lon = 9.1797775
closest, distance = b.findClosest(lat, lon)
string = ""
string += f"Closest station to lat {lat}°N lon {lon}°E, {distance}km away:{newl}"
string += f"Station {closest['name']}, ID: {closest['ID']}, in coords {closest['coordinates']['lat']}°N, {closest['coordinates']['lon']}°E {newl}"
string += f"{tab}Bikes: {closest['bikes']['bikes']}{newl}"
string += f"{tab}Electric bikes: {closest['bikes']['electric_bikes']}{newl}"
string += f"{tab}Electric bikes with child seat: {closest['bikes']['electric_bikes_child_seat']}{newl}"
string += f"{tab}Free racks: {closest['bikes']['bike_racks']}{newl}"
if closest["status"]["full"]:
    string += f"{tab}The station is full.{newl}"
elif closest["status"]["empty"]:
    string += f"{tab}The station is empty.{newl}"
elif closest["status"]["probably_full"]:
    string += f"{tab}The station is probably empty.{newl}"
elif closest["status"]["probably_empty"]:
    string += f"{tab}The station is probably empty.{newl}"

print(string)

# save data to json file
b.saveToFile("BikeMi.json")
