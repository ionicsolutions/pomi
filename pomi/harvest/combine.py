import json

import pomi.harvest.wikipedia as wikipedia
import pomi.harvest.wikidata as wikidata
import pomi.harvest.commons as commons

# TODO: Move to configuration file/some common place and versonify
TYPES = ["biography", "heritage", "geography"]

LANGUAGES = ["de", "en"]
THUMBNAIL_SIZE = 64

datafile = "test.json"

pomis = json.load(datafile)

descriptions = {}

for pomi, props in pomis.items():
    wdata = wikidata.fetch_wikidata(props["wikidata"])

    # TODO: Download images and store them, save the local path
    # to the image instead of the Commons URLs
    # TODO: Find a way to deal with the license requirements

    filename = wikidata.get_image(wdata)
    if filename is None:
        try:
            filename = props["wikipediaImage"]
        except KeyError:
            # TODO: Find a suitable placeholder image
            filename = "Placeholder"
    props["imageUrl"] = commons.generate_image_file_url(filename)
    props["imageInfoUrl"] = commons.generate_image_info_url(filename)
    props["thumbnailUrl"] = commons.generate_thumbnail_url(filename,
                                                           size=THUMBNAIL_SIZE)

    for language in LANGUAGES:
        descriptions[language] = {}
        desc = descriptions[language]
        for id, properties in pomis.items():
            desc[id] = wikipedia.get_information(language,
                                                 wikidata.get_wikipedia_article(wdata,
                                                                                language))
            desc[id]["wikidataDescription"] = wikidata.get_description(wdata,
                                                                       language)