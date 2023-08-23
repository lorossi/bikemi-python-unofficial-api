# Bikemi Unofficial API

*I sincerely hope ATM won't ban my IP for this.*

## Description

This module extracts the data for every station from the [Bikemi](http://www.bikemi.com) website.

By instantiating the `Bikemi` class and calling the `scrape` method, the module will download the data from the website and parse it.
If the method is not explicitly called, the data will be downloaded and parsed only while accessing the attributes of the `Bikemi` class.
The data can then be retrieved as a list of instances of the `Station` class, containing more details (some encapsulated in other classes) about the station.
Global statistics about the whole network are also returned.

Available attributes:

- `last_scrape`: `int` containing the timestamp of the last time the data was downloaded and parsed
- `raw_data`: `dict` containing the raw data downloaded from the website
- `stations`: `list[Station]`, containing the data for every station
- `global_stats`: `GlobalStats` containing global statistics about the whole network

All classes can be serialized and deserialized from and to the following formats:

- `json`
- `yaml`
- `toml`

All classes are implemented using my ![customdataclass](https://github.com/lorossi/customdataclass) module, which is a better (I believe) version of the `dataclass` module from the standard library.
Check the documentation for more details.

### Structure of the data

#### Global Data

Global data is contained in the `GlobalStats` class, which contains the following attributes:

- `timestamp`: `float` containing the timestamp of the last time the data was downloaded and parsed
- `available_vehicles`: `int` containing the total number of available vehicles in the whole network
- `available_docks`: `int` containing the total number of available docking stations in the whole network
- `available_dock_categories`: `list[AvailableDockCategory]` containing the number of available docking stations for each category
- `available_vehicles_categories`: `list[AvailableVehicleCategory]` containing the number of available vehicles for each category
- `full_stations_count`: `int` containing the number of stations that are full
- `empty_stations_count`: `int` containing the number of stations that are empty
- `total_stations_count`: `int` containing the total number of stations in the whole network

#### Station

Station data is contained in the `Station` class, which contains the following attributes:

- `id`: `int` containing the ID of the station
- `name`: `str` containing the name of the station
- `title`: `str` containing the title of the station
- `clean_title`: `str` containing the cleaned title of the station
- `state`: `str` containing the state of the station
- `sub_title`: `str` containing the subtitle of the station
- `enabled`: `bool` containing whether the station is enabled or not
- `availability_info`: `AvailabilityInfo` containing the availability information for the station
- `coord`: `Coord` containing the coordinates of the station

#### AvailabilityInfo

Availability information is contained in the `AvailabilityInfo` class, which contains the following attributes:

- `available_vehicles`: `int` containing the number of available vehicles
- `available_docks`: `int` containing the number of available docking stations
- `available_dock_categories`: `list[AvailableDockCategory]` containing the number of available docking stations for each category
- `available_vehicle_categories`: `list[AvailableVehicleCategory]` containing the number of available vehicles for each category

#### AvailableDockCategory

Available docking stations for a category is contained in the `AvailableDockCategory` class, which contains the following attributes:

- `category`: `str` containing the category of the docking station
- `count`: `int` containing the number of available docking stations for the category

#### AvailableVehicleCategory

Available vehicles for a category is contained in the `AvailableVehicleCategory` class, which contains the following attributes:

- `category`: `str` containing the category of the vehicle
- `count`: `int` containing the number of available vehicles for the category

#### Coord

Coordinates are contained in the `Coord` class, which contains the following attributes:

- `lat`: `float` containing the latitude of the station
- `lon`: `float` containing the longitude of the station

## Code example

```python
from bikemi import Bikemi

def main():
    bikemi = Bikemi()
    if not bikemi.scrape():
        print("Error while scraping data")
        return

    for station in bikemi.stations:
      print(station)

    print(global_stats)
```

## Requirements

The module requires the packages listed in `requirements.txt` to be installed.

### Installation

```bash
pip install -r requirements.txt
```

## License

This module is released under the MIT license. See [LICENSE](LICENSE.md) for more details.
