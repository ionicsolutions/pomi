import sqlite3
import json

from pomi.coordinates import calculate_box, distance

# TODO: Move to configuration file/some common place
TYPES = ["biography", "heritage", "geography"]

MAX_BOX_SIZE = 20

class Database:
    """In-memory SQLite database to store POMIs for fast searching.

    When starting the API, the POMIs are loaded into the database
    from the JSON file which contains the POMIs collected for the
    route.

    Note that the number of objects along a given route will be
    a few 10000 at most, while the number of users will not
    exceed about 1000 even if everybody on an ICE train is using
    the tool. Additionally, note that the vast majority of users will
    use (one of) the standard view(s) which is pre-computed by the API.
    Therefore I believe that the performance will be sufficient.

    (This JSON file is also kept in memory as a dictionary object
    from which the POMI information is returned. The database is
    only used for searching.)
    """

    def __init__(self, fname=None):
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE pomis
                          (id int, lat real, lon real, type text)""")

        self.conn.commit()

        if fname is not None:
            self._load_data(fname)

    def _load_data(self, fname):
        with open(fname, "r") as pomifile:
            pomis = json.load(pomifile)
            self.add(pomis)

    def add(self, pomis):
        entries = [(int(id), pomi["lat"], pomi["lon"], pomi["type"])
                    for id, pomi in pomis.items()]
        self.c.executemany("INSERT INTO pomis VALUES (?, ?, ?, ?)",
                           entries)
        self.conn.commit()

    def all(self):
        self.c.execute("SELECT id FROM pomis")
        return [row[0] for row in self.c.fetchall()]

    def fetch(self, lat, lon, box_size, max_num=-1, types=TYPES):
        for type_ in types:
            if type_ not in TYPES:
                raise ValueError("Unknown type '{:s}'.".format(type_))

        box_size = max(box_size, MAX_BOX_SIZE)

        lat0, lon0, lat1, lon1 = calculate_box(lat, lon, box_size)

        self.c.execute("""SELECT * FROM pomis WHERE
                          lat > ? AND lat < ? AND lon > ? AND lon < ?""",
                       (lat0, lat1, lon0, lon1))
        query_result = self.c.fetchall()

        result = [(str(row[0]), distance(lat, lon, row[1], row[2]))
                  for row in query_result
                  if row[3] in types]
        result.sort(key=lambda x: x[1])

        if max_num > 0:
            return result[:max_num]
        else:
            return result

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    pomis = {"14334" : {"lat": 22.33, "lon": 34.6, "type": "heritage"} }

    db = Database()
    db.add(pomis)

    print(db.all())
    print(db.fetch(22.328, 34.6, 2))
