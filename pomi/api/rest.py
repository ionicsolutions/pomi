import logging

from flask import Flask, jsonify

from pomi.api.database import Database

logging.basicConfig(level=logging.DEBUG)
app = Flask("__name__")

db = Database("test.json")

pomis = {}

descriptions = { "de": {}, "en": {}}

default_response = {"de": "JSON string", "en": "JSON string"}

# TODO: Check the "/ at the end" rules for Flask
@app.route("/get")
@app.route("/get/<language:str>")
@app.route("/default")
@app.route("/default/<language:str>")
def default_pomis(language="de"):
    """Return the standard view, i.e. a list of all POMIs at the current
    location of the train. This view is cached and updated regularly."""
    return default_response[language]


@app.route("/get/<lat:float>/<lon:float>/<box_size:int>")
@app.route("/get/<lat:float>/<lon:float>/<box_size:int>/<language:str>")
def get_pomis(lat, lon, box_size, language="de"):
    """Return all POMIs at the given location within the given box
    size (kilometres).
    """
    pomis = db.fetch(lat, lon, box_size, max_num=25)
    response = {id: pomis[id] for id, distance in pomis}
    # TODO: Check whether there is a way to add the distance to the response
    # within the dict comprehension
    desc = descriptions[language]
    for id, distance in pomis:
        response[id]["distance"] = distance
        response[id].update(desc[id])
    return jsonify(response)


if __name__ == "__main__":
    # TODO: Check that db access works with threaded=True,
    # cf. sqlite3 doc 12.6.9.1. Multithreading
    # Otherwise, we need to pass the calls to the DB through a
    # queue or use a database which supports multithreading
    app.run()