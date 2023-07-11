from geopy.distance import geodesic
from typing import Tuple

def get_distance_between_points(coord1: Tuple, coord2: Tuple) -> float:
    return round(geodesic(coord1, coord2).kilometers, 2)
