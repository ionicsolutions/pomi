"""Find and collect Points of Mild Interest."""
import math
import json

import pomi.harvest.osm as osm
import pomi.coordinates as coord

# TODO: Move to configuration file
# search parameters, need to be optimized
MIN_POMIS = 3
MAX_POMIS = 20
DEFAULT_LENGTH = 2 # kilometres
MAX_LENGTH = 30  # kilometres

LANGUAGES = ["de", "en"]


class Collector:

    def __init__(self, fname=None):
        """Basic storage of collected POMIs."""
        if fname is None:
            self.pomis = {}
        else:
            with open(fname, "r") as datafile:
                self.pomis = json.load(datafile)

    def add(self, pomis):
        self.pomis.update({str(pomi["id"]): pomi for pomi in pomis})

    def __len__(self):
        return len(self.pomis)

    def all(self):
        for pomi in self.pomis.values():
            yield pomi

    def dump(self, fname):
        with open(fname, "w") as datafile:
            json.dump(self.pomis, datafile, indent=4)


def collect_pomis_along_route(waypoints, box_size=DEFAULT_LENGTH,
                              collector=Collector()):
    """This method assumes closely spaced waypoints and therefore does not
    update the number of steps. For situations where the *box_size* changes
    significantly during the iteration, this will lead to missed pomis or
    unnecessarily many calls to `find_pomis`.
    TODO: Check whether this is a good assumption given the track data we have
    access to
    """
    for point1, point2 in zip(waypoints, waypoints[1:]):
        for lat, lon in coord.generate_sliding_boxes(*point1, *point2, box_size):
            pomis, box_size = find_pomis(lat, lon, box_size)
            collector.add(pomis)


def find_pomis(lat, lon, box_size=DEFAULT_LENGTH):

    while True:
        pomis = osm.get_pomis(lat, lon, box_size)

        num_of_pomis = len(pomis)

        if num_of_pomis < MIN_POMIS:
            if box_size >= MAX_LENGTH:
                break
            else:
                box_size = max(math.sqrt(2) * box_size, MAX_LENGTH)
        elif num_of_pomis > MAX_POMIS:
            box_size = min(box_size/math.sqrt(2), DEFAULT_LENGTH)
            break
        else:
            break

    return pomis, box_size
