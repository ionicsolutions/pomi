"""Find Points of Mild Interest on OpenStreetMap using the Overpass API."""
import requests
import urllib.parse
from pomi.coordinates import calculate_box

__all__ = ["get_pomis"]

# TODO: Move to configuration file
# include only nodes with the following tags
INCLUDE = ["wikidata"]
# exclude nodes with the following tags
EXCLUDE = ["place"]
# if specified, collect the value of the following tags
COLLECT = ["cemetary", "memorial"]


def get_pomis(lat, lon, box_size):
    box = calculate_box(lat, lon, box_size)
    query_string = build_query(INCLUDE, EXCLUDE, box)
    response = query_overpass(query_string)
    return extract_pomis(response, INCLUDE, COLLECT)


def build_query(include, exclude, box):
    query_string = "node"
    for key in include:
        query_string += '["{:s}"]'.format(key)
    for key in exclude:
        query_string += '["{:s}"!~".*"]'.format(key)
    query_string += "({:f},{:f},{:f},{:f});".format(*box)
    return query_string


def query_overpass(query_string):
    query_args = urllib.parse.urlencode(
        {"data": "[out:json];{:s}out;".format(query_string)})
    query_url = "http://overpass-api.de/api/interpreter?{:s}".format(query_args)

    try:
        response = requests.get(query_url).json()
    except (ConnectionError, TimeoutError) as e:
        # TODO: Handle this more gracefully
        raise e
    # TODO: Catch JSON parsing issues
    else:
        return response


def extract_pomis(response, require_tags=(), collect_tags=()):
    pomis = []
    for node in response.elements:
        if not node["type"] == "node":
            continue

        pomi = {"id": int(node["id"]),
                "lat": float(node["lat"]),
                "lon": float(node["lon"])}

        if collect_tags:
            pomi["qualifiers"] = {}
            for tag in collect_tags:
                try:
                    pomi["qualifiers"][tag] = node["tags"][tag]
                except KeyError:
                    pass

        for tag in require_tags:
            try:
                pomi[tag] = node["tags"][tag]
            except KeyError:
                break
        else:
            # all required tags were found
            pomis.append(pomi)

        continue

    return pomis
