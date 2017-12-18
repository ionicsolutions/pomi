"""Collection of functions for working with geo coordinates."""
import math

OVERLAP_THRESHOLD = 0.8

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


def distance(lat0, lon0, lat1, lon1):
    """This only works for small distances!"""
    return (lat0 - lat1)**2 + (lon0 - lon1)**2


def calculate_box(lat, lon, box_size):
    height = km_to_lat(box_size, lat)
    width = km_to_lon(box_size) / 2
    return lat - height/2, lon - width/2, lat + height/2, lon + width/2


def generate_sliding_boxes(lat0, lon0, lat1, lon1, box_size, yield1=False):
    vector_lat, vector_lon = lat1 - lat0, lon1 - lon0

    llat, llon = (lat_to_km(vector_lat, lat0 + vector_lat/2),
                  lon_to_km(vector_lon))

    if not max(llat/box_size, llon/box_size) < OVERLAP_THRESHOLD:
        num_of_steps = int(max(llat/box_size, llon/box_size)
                           /(1 - OVERLAP_THRESHOLD))
        step_lat, step_lon = vector_lat/num_of_steps, vector_lon/num_of_steps
        for i in range(num_of_steps):
            yield lat0 + i * step_lat, lon0 + i * step_lon
    else:
        yield1 = True

    if yield1:
        yield lat1, lon1
