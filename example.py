"""Scrape the data from the website via the reversed API."""
from modules.bikemi import Bikemi


def main():
    """Run the Main function."""
    s = Bikemi()
    if not s.scrape():
        print("Scraping failed")
        return

    for station in s.stations:
        print(station)

    print(s.global_stats)


if __name__ == "__main__":
    main()
