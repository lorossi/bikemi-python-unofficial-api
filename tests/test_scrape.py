import unittest
import json

from modules.entities import Station, GlobalStats
from modules.bikemi import Bikemi
from modules.station_factory import StationFactory


class TestBikemi(unittest.TestCase):
    def _mockScraper(
        self,
    ) -> list[Station]:
        with open("tests/mock/raw_data.json") as f:
            json_data = json.load(f)["data"]["dockGroups"]

        return [StationFactory.from_dict(station) for station in json_data]

    def _createMockScraper(self) -> Bikemi:
        b = Bikemi()
        b._loadData = self._mockScraper
        return b

    def _loadGlobalStats(self, timestamp: float) -> GlobalStats:
        with open("tests/mock/global_stats.json", "r") as f:
            dict_data = json.load(f)

        dict_data["timestamp"] = timestamp
        return StationFactory.from_dict(dict_data, GlobalStats)

    def _loadStations(self) -> list[Station]:
        with open("tests/mock/stations.json", "r") as f:
            dict_data = json.load(f)

        return [StationFactory.from_dict(s) for s in dict_data]

    def testScrape(self):
        b = self._createMockScraper()
        self.assertTrue(b.scrape())

    def testGlobalStats(self):
        b = self._createMockScraper()
        self.assertTrue(b.scrape())

        g = self._loadGlobalStats(b.last_scrape)

        for attr in g.attributes:
            if not isinstance(getattr(b.global_stats, attr), list):
                self.assertEqual(getattr(b.global_stats, attr), getattr(g, attr))
            else:
                # the items might be in different order
                self.assertTrue(
                    all(
                        [
                            item in getattr(b.global_stats, attr)
                            for item in getattr(g, attr)
                        ]
                    )
                )

    def testStations(self):
        b = self._createMockScraper()
        self.assertTrue(b.scrape())

        stations = self._loadStations()

        for station in stations:
            self.assertTrue(station in b.stations)

    def testTimestamp(self):
        b = self._createMockScraper()
        self.assertTrue(b.scrape())
        self.assertEqual(b.last_scrape, b.global_stats.timestamp)
