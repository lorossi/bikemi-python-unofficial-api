"""Scraper module."""
from __future__ import annotations

import time

import requests

from modules.entities import (
    AvailableDockCategory,
    AvailableVehicleCategory,
    GlobalStats,
    Station,
)
from modules.station_factory import StationFactory


class Bikemi:
    """Scraper class."""

    _last_scrape: int = 0
    _scrape_interval = 60
    _stations: list[Station] = list()

    def _refreshScrape(f, *_, **__):
        """Refresh scrape if needed.

        Decorator to be placed before any method that uses the stations list.
        """

        def wrapper(self, *args, **kwargs):
            if time.time() - self._last_scrape >= self._scrape_interval:
                self.scrape()
            return f(self, *args, **kwargs)

        return wrapper

    def __init__(
        self,
        proxy_address: str = None,
        proxy_user: str = None,
        proxy_password: str = None,
    ) -> Bikemi:
        """Initialize the scraper."""
        self._url: str = "https://core.urbansharing.com/public/api/v1/graphql"
        self._proxy_address = proxy_address
        self._proxy_user = proxy_user
        self._proxy_password = proxy_password

        if self._proxy_address is not None:
            if self._proxy_user is not None and self._proxy_password is not None:
                self._proxy = {
                    "http": f"http://{self._proxy_user}:{self._proxy_password}"
                    f"@{self._proxy_address}",
                    "https": f"https://{self._proxy_user}:{self._proxy_password}"
                    f"@{self._proxy_address}",
                }
            else:
                self._proxy = {
                    "http": f"http://{self._proxy_address}",
                    "https": f"https://{self._proxy_address}",
                }
        else:
            self._proxy = None

        self._query: str = "query { dockGroups { id name title state subTitle enabled \
                        availabilityInfo { availableVehicles availableDocks \
                        availableVirtualDocks availablePhysicalDocks \
                        availableVehicleCategories { category count } } \
                        coord { lat lng } } } "
        self._headers = {"systemId": "milan-bikemi"}
        self._stations: list[Station] = None

    def scrape(self) -> bool:
        """Scrape the data."""
        if time.time() - self._last_scrape < self._scrape_interval:
            return True

        self._stations = self._loadData()
        self._last_scrape = time.time()
        return len(self._stations) > 0

    def _loadData(self) -> list[Station]:
        r = requests.get(
            self._url,
            params={"query": self._query},
            headers=self._headers,
            proxies=self._proxy,
        )
        self._raw_data = r.json()
        return [StationFactory.from_dict(s) for s in r.json()["data"]["dockGroups"]]

    @property
    def last_scrape(self) -> float:
        """Return the last scrape timestamp."""
        return self._last_scrape

    @property
    @_refreshScrape
    def stations(self) -> list[Station]:
        """Return the stations list."""
        return self._stations

    @property
    @_refreshScrape
    def global_stats(self) -> GlobalStats:
        """Return the global stats."""
        docks_categories = set(
            [
                c.category
                for s in self._stations
                for c in s.availability_info.available_dock_categories
            ]
        )

        vehicles_categories = set(
            [
                c.category
                for s in self._stations
                for c in s.availability_info.available_vehicle_categories
            ]
        )

        return GlobalStats(
            timestamp=self._last_scrape,
            available_vehicles=sum(
                [s.availability_info.available_vehicles for s in self._stations]
            ),
            available_docks=sum(
                [s.availability_info.available_docks for s in self._stations]
            ),
            available_dock_categories=[
                AvailableDockCategory(category=c, count=self._countDocks(c))
                for c in docks_categories
            ],
            available_vehicle_categories=[
                AvailableVehicleCategory(category=c, count=self._countVehicles(c))
                for c in vehicles_categories
            ],
            full_stations_count=len(
                [s for s in self._stations if s.availability_info.available_docks == 0]
            ),
            empty_stations_count=len(
                [
                    s
                    for s in self._stations
                    if s.availability_info.available_vehicles == 0
                ]
            ),
            total_stations_count=len(self._stations),
        )

    @property
    @_refreshScrape
    def raw_data(self) -> dict:
        """Return the raw data."""
        return self._raw_data

    def _countDocks(self, category: str) -> int:
        """Count the docks for a given category."""
        return sum(
            [
                sum(
                    [
                        c.count
                        for c in s.availability_info.available_dock_categories
                        if c.category == category
                    ]
                )
                for s in self._stations
            ]
        )

    def _countVehicles(self, category: str) -> int:
        """Count the vehicles for a given category."""
        return sum(
            [
                sum(
                    [
                        c.count
                        for c in s.availability_info.available_vehicle_categories
                        if c.category == category
                    ]
                )
                for s in self._stations
            ]
        )
