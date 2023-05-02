"""Station Factory Module."""
import json

from .entities import (
    AvailabilityInfo,
    AvailableDockCategory,
    AvailableVehicleCategory,
    Coord,
    Station,
)


class StationFactory:
    """Station Factory."""

    @staticmethod
    def from_dict(
        json_data: dict,
        dest_class: type[Station | AvailabilityInfo | AvailableVehicleCategory | Coord]
        | None = None,
    ) -> (
        type[Station | AvailabilityInfo | AvailableVehicleCategory | Coord]
        | list[type[Station | AvailabilityInfo | AvailableVehicleCategory | Coord]]
    ):
        """Create a Station from a dict.

        Args:
            json_data (dict): The dict to create the Station from.
            dest_class (type[Station | AvailabilityInfo | AvailableVehicleCategory \
                | Coord], optional): The destination class. Defaults to None.

        Returns:
            type[Station | AvailabilityInfo | AvailableVehicleCategory | Coord] | \
                list[type[Station | AvailabilityInfo | AvailableVehicleCategory | \
                Coord]]: The created class or list of classes.
        """
        if dest_class is None:
            dest_class = Station

        attributes_mappings = {
            "subTitle": "sub_title",
            "availabilityInfo": "availability_info",
            "availableVehicleCategories": "available_vehicle_categories",
            "availableDocksCategories": "available_dock_categories",
            "availableVehicles": "available_vehicles",
            "availableDocks": "available_docks",
            "lng": "lng",
        }

        class_mapping = {
            "coord": Coord,
            "availability_info": AvailabilityInfo,
            "available_vehicle_categories": AvailableVehicleCategory,
            "available_dock_categories": AvailableDockCategory,
        }

        # rename the availableVirtualDocks and availablePhysicalDocks to \
        # availableDocksCategories to better match the class name

        if "availableVirtualDocks" in json_data:
            json_data["availableDocksCategories"] = [
                {
                    "category": "virtual",
                    "count": json_data["availableVirtualDocks"],
                },
                {
                    "category": "physical",
                    "count": json_data["availablePhysicalDocks"],
                },
            ]

            del json_data["availableVirtualDocks"]
            del json_data["availablePhysicalDocks"]

        cleaned_data = {}
        for k, v in json_data.items():
            clean_key = attributes_mappings.get(k, k)
            if clean_key in class_mapping:
                ...
                if isinstance(v, list):
                    cleaned_data[clean_key] = [
                        StationFactory.from_dict(x, class_mapping[clean_key]) for x in v
                    ]
                else:
                    cleaned_data[clean_key] = StationFactory.from_dict(
                        v, class_mapping[clean_key]
                    )
            else:
                cleaned_data[clean_key] = v

        return dest_class(**cleaned_data)

    @staticmethod
    def from_json(
        json_data: str,
        dest_class: type[Station | AvailabilityInfo | AvailableVehicleCategory | Coord]
        | None = None,
    ) -> Station:
        """Create a Station from a json string."""
        dict_data = json.loads(json_data)

        return StationFactory.from_dict(dict_data, dest_class=dest_class)
