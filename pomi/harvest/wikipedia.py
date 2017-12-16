"""Collect information on Points of Mild Interest from Wikipedia."""
import urllib.parse
import requests
import random

__all__ = ["get_information"]

# TODO: Move to configuration file
# if True (False) retrieve Wikipedia excerpt as HTML (plain text)
EXCERPT_AS_HTML = True


def get_information(language, page_title):
    query_string = build_query(page_title)
    response = query_wikipedia_api(language, query_string)
    return extract_pomi_information(response)


def build_query(page_title):
    parameters = {
        "format": "json",
        "action": "query",
        "titles": page_title,
        "prop": "extracts|images|info",
        "imlimit": 10,
        "exintro": "",  # only retrieve article introduction
        "inprop": "url"  # retrieve encoded article URL
    }

    if not EXCERPT_AS_HTML:
        parameters["explaintext"] = ""

    query_string = urllib.parse.urlencode(parameters)

    return query_string


def query_wikipedia_api(language, query_string):
    query_url = \
        "https://{:s}.wikipedia.org/w/api.php?{:s}".format(language,
                                                           query_string)

    try:
        response = requests.get(query_url).json()
    except (ConnectionError, TimeoutError) as e:
        # TODO: Handle this more gracefully
        raise e
    # TODO: Catch JSON parsing issues

    return response


def extract_pomi_information(response):
    pomi_information = {}

    page_id = next(iter(response["query"]["pages"]))

    if page_id != "-1":
        page = response["query"]["pages"][page_id]

        pomi_information["wikipediaTitle"] = page["title"]
        pomi_information["wikipediaDescription"] = page["extract"]
        pomi_information["wikipediaUrl"] = page["fullurl"]

        if "images" in page:
            image_id = random.randint(0, len(page["images"]))
            pomi_information["wikipediaImage"] = page["images"][str(image_id)]

    return pomi_information
