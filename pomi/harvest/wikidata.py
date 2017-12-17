"""Collect information on Points of Mild Interest from Wikidata."""
import requests


def fetch_wikidata(wikidata_id):
    query_string = "https://www.wikidata.org/wiki/" \
                   "Special:EntityData/{:s}.json".format(wikidata_id)

    try:
        response = requests.get(query_string).json()
    except (ConnectionError, TimeoutError) as e:
        # TODO: Handle this more gracefully
        raise e
    # TODO: Catch JSON parsing issues
    else:
        return response["entities"][wikidata_id]


def get_property(wdata, property):
    try:
        return wdata[property][0]["mainsnak"]["datavalue"]["value"]
    except KeyError:
        return None


def get_image(wdata):
    return get_property(wdata, "P18")


def is_human(wdata):
    return get_property(wdata, "P31") == "Q5"


def get_wikipedia_article(wdata, language):
    try:
        return wdata["sitelinks"]["{:s}wiki".format(language)]["title"]
    except KeyError:
        return ""


def get_description(wdata, language):
    try:
        return wdata["descriptions"][language]["value"]
    except KeyError:
        return ""
