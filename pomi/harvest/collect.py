import pomi.harvest.osm as osm
import pomi.harvest.wikipedia as wikipedia

# TODO: Move to configuration file
MIN_POMIS = 3

MAX_POMIS = 20

DEFAULT_LENGTH = 2 # kilometres
MAX_LENGTH = 30  # kilometres

LANGUAGES = ["de", "en"]


def find_pomis(lat, lon, box_size=DEFAULT_LENGTH):

    while True:
        pomis = osm.get_pomis(lat, lon, box_size)

        num_of_pomis = len(pomis)

        if num_of_pomis < MIN_POMIS:
            if box_size >= MAX_LENGTH:
                break
            else:
                box_size = max(box_size * 1.5, MAX_LENGTH)
        elif num_of_pomis > MAX_POMIS:
            box_size = min(box_size * 0.5, DEFAULT_LENGTH)
            break
        else:
            break

    return pomis, box_size


def aggregate_information(pomis):



    for language in LANGUAGES:
        wikipedia.get_information(language, page_title)