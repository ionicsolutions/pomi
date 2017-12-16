import math

OVERLAP_THRESHOLD = 0.9

# Earth's perimeter is 40.008 km -> 40.008 km/360° = 113.13 km/°
# see http://www.iaktueller.de/exx.php

def km_to_lat(length, lat):
    return length / (111.13 * math.cos(lat / 180 * math.pi))


def lat_to_km(delta_lat, lat):
    return delta_lat * 111.13 * math.cos(lat / 180 * math.pi)


def km_to_lon(length):
    return length / 111.13


def lon_to_km(lon):
    return lon * 111.13


def calculate_box(lat, lon, box_size):
    height = km_to_lat(box_size, lat)
    width = km_to_lon(box_size) / 2
    return lat - height/2, lon - width/2, lat + height/2, lon + width/2


def shift_box(lat0, lon0, box_size, lat1, lon1):
    vector_lat, vector_lon = lat1 - lat0, lon1 - lon0

    llat, llon = (lat_to_km(vector_lat, lat0 + vector_lat/2),
                  lon_to_km(vector_lon))

    if max(llat/box_size, llon/box_size) < OVERLAP_THRESHOLD:
       # we can go in one step
    else:
        num_of_steps = max(llat/box_size, llon/box_size)/OVERLAP_THRESHOLD

