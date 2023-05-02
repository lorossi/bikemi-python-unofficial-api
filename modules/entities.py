"""Entities for the BikeMI API endpoints."""

import re

from customdataclass import Dataclass


class AvailableVehicleCategory(Dataclass):
    """Available vehicle category."""

    category: str
    count: int


class AvailableDockCategory(Dataclass):
    """Available dock category."""

    category: str
    count: int


class AvailabilityInfo(Dataclass):
    """Availability info."""

    available_vehicles: int
    available_docks: int
    available_dock_categories: list[AvailableDockCategory]
    available_vehicle_categories: list[AvailableVehicleCategory]


class Coord(Dataclass):
    """Coordinates."""

    lat: float
    lng: float


class Station(Dataclass):
    """Station."""

    id: str
    name: str
    title: str
    state: str
    sub_title: str
    enabled: bool
    availability_info: AvailabilityInfo
    coord: Coord

    @property
    def clean_title(self) -> str:
        """Return a clean title."""
        no_prefix = re.sub(r"(^[0-9]+) - ", "", self.title)
        no_v_prefix = re.sub(r"V[0-9]+ - ", "", no_prefix)
        no_dash = re.sub(r"\s*-\s*", ", ", no_v_prefix)
        no_double_spaces = re.sub(r"\s+", " ", no_dash)
        return no_double_spaces.strip().title()


class GlobalStats(Dataclass):
    """Global stats."""

    timestamp: float
    available_vehicles: int
    available_docks: int
    available_dock_categories: list[AvailableDockCategory]
    available_vehicle_categories: list[AvailableVehicleCategory]
    full_stations_count: int
    empty_stations_count: int
    total_stations_count: int
