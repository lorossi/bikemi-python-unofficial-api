import requests
import datetime
import json

# BikeMi api - scraper for BikeMi website
class BikeMi:
    def __init__(self):
        self.bikemi = {}
        # BikeMi map url
        self.url = "https://www.bikemi.com/it/mappa-stazioni.aspx"
        # threshold set to know if the station is probably full or empty.
        # this is a completely empiric value set by my experience
        self.probability_threshold = 2
        # delimiters used to identify map position in page source and bikes
        #   info in table
        self.delimiters = {
            "map" : { # identify map
                    "start":
                    {
                        "string": '<div id="station-map" style="background-color:Gray;width:100%;height:480px;">',
                        "skip": 4 # lines to skip (forward)
                    },
                "end": {
                        "string": '</script><div id="station-map-search">',
                        "skip": -2
                    }
                },
            "table" : { # identify table in map
                "start": {
                    "string": "\\u003ctd\\u003e"
                },
                "end": {
                    "string": "\\u003c/td"
                },
                "elements": [
                    {
                        "position": 29, # line in map
                        "name": "bike_racks" # variable name
                    },
                    {
                        "position": 28,
                        "name": "bikes"
                    },
                    {
                        "position": 36,
                        "name": "electric_bikes"
                    },
                    {
                        "position": 44,
                        "name": "electric_bikes_child_seat"
                    }
                ]
            },

            "id": {
                "start": {
                    "string": "\\u003e"
                },
                "end": {
                    "string": " -"
                }
            }
        }


    def getBikes(self):
        self.bikemi = {}
        try:
            # try to load the page
            r = requests.get(self.url)
            self.bikemi["timestamp"] = datetime.datetime.now().isoformat()

            if r.status_code != 200:
                # something went wrong...
                raise

            self.bikemi["status"] = r.status_code
        except:
            # cannot load page for some reasongs
            self.bikemi["status"] = 404
            return self.bikemi

        self.bikemi["global_stats"] = {}
        self.bikemi["stations"] = []

        # split the body line by line
        html = r.text.splitlines()

        for x in range(len(html)):
            if self.delimiters["map"]["start"]["string"] in html[x]:
                # we found the first line of the map
                start = x + self.delimiters["map"]["start"]["skip"]
            elif self.delimiters["map"]["end"]["string"] in html[x]:
                # we found the last line of the map
                end = x + self.delimiters["map"]["end"]["skip"]
                break

        map = html[start:end]
        bikes_stats = {}

        for line in map:
            # each station is exactly one line long inside the map
            new_station = {}

            m = line.split(",")
            # each of these elements is comma separated
            icon = m[0].split("'")[1] # url is in quotes
            lat = float(m[1])
            lon = float(m[2])
            name = m[3].replace("'", "").strip() #lots of unnecessary quotes
            # now we want to work on the table containing infos about the
            #   station
            table = m[4].split("\\r\\n")

            bikes = {}
            total = 0 # total number of bikes
            start_delim = self.delimiters["table"]["start"]["string"]
            end_delim = self.delimiters["table"]["end"]["string"]
            for element in self.delimiters["table"]["elements"]:
                start = table[element["position"]].find(start_delim)
                start += len(self.delimiters["table"]["start"]["string"])
                end = table[element["position"]].find(end_delim)

                # parse the found number
                number = int(table[element["position"]][start:end])
                bikes[element["name"]] = number

                # add this data to the global stats dict
                if element["name"] in bikes_stats:
                    bikes_stats[element["name"]] += number
                else:
                    bikes_stats[element["name"]] = number

                # calculate the number of bikes inside a station
                if "racks" not in element["name"]:
                    total += number

            # extract the id of the station from its container
            id_container = table[2]
            start_delim = self.delimiters["id"]["start"]["string"]
            end_delim = self.delimiters["id"]["end"]["string"]
            start = id_container.find(start_delim)
            start += len(start_delim)
            end = id_container.find(end_delim)

            try:
                # we try to parse to int
                # this might actually break if they decide to use letters in ids
                id = int(id_container[start:end])
            except:
                id = id_container[start:end]

            # sometimes the number of registered bikes is wrong because
            #   their system doesn't take track of broken bikes
            #   so we want to show if, according to my calculations,
            #   the bike rack moght be full or empy
            probably_empty = (total <= self.probability_threshold)
            probably_full = (total >= (bikes_stats["bike_racks"] - self.probability_threshold))


            # create a new dict
            new_station = {
                "name": name,
                "ID": id,
                "coordinates": {
                    "lat": lat,
                    "lon": lon
                },
                "bikes" : bikes,
                "probably_empty": probably_empty,
                "probably_full": probably_full,
                "icon": icon,
            }
            # append the new dict to the lsit
            self.bikemi["stations"].append(new_station)

        # add some stats
        self.bikemi["global_stats"] = bikes_stats
        total = 0

        # calculate total number of bikes
        for b in bikes_stats:
            if not "racks" in b:
                total += bikes_stats[b]

        # add this stat
        self.bikemi["global_stats"]["total_bikes"] = total
        self.bikemi["global_stats"]["total_stations"] = len(map)
        return self.bikemi


    # save self.bikemi to file
    def saveToFile(self, path="BikeMi.json"):
        with open(path, 'w') as json_file:
            json.dump(self.bikemi, json_file)
