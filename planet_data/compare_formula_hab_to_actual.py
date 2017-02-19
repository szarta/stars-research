#!/usr/bin/python
"""
    compare_formula_hab_to_actual.py

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse
import logging

__version__ = "%(prog)s 1.0.0 (Rel: 19 Feb 2017)"
default_log_format = "%(filename)s:%(levelname)s:%(asctime)s] %(message)s"

# The gravity values are not linear, but still map to (0, 100) step 1
# Although the bottom-most values are a little strange in that they double
# increment
Gravity_Map = {
    0.12: 0,
    0.13: 2,
    0.14: 4,
    0.15: 6,
    0.16: 8,
    0.17: 9,
    0.18: 11,
    0.19: 12,
    0.20: 13,
    0.21: 14,
    0.22: 15,
    0.24: 16,
    0.25: 17,
    0.27: 18,
    0.29: 19,
    0.31: 20,
    0.33: 21,
    0.36: 22,
    0.40: 23,
    0.44: 24,
    0.50: 25,
    0.51: 26,
    0.52: 27,
    0.53: 28,
    0.54: 29,
    0.55: 30,
    0.56: 31,
    0.58: 32,
    0.59: 33,
    0.60: 34,
    0.62: 35,
    0.64: 36,
    0.65: 37,
    0.67: 38,
    0.69: 39,
    0.71: 40,
    0.73: 41,
    0.75: 42,
    0.78: 43,
    0.80: 44,
    0.83: 45,
    0.86: 46,
    0.89: 47,
    0.92: 48,
    0.96: 49,
    1.00: 50,
    1.04: 51,
    1.08: 52,
    1.12: 53,
    1.16: 54,
    1.20: 55,
    1.24: 56,
    1.28: 57,
    1.32: 58,
    1.36: 59,
    1.40: 60,
    1.44: 61,
    1.48: 62,
    1.52: 63,
    1.56: 64,
    1.60: 65,
    1.64: 66,
    1.68: 67,
    1.72: 68,
    1.76: 69,
    1.80: 70,
    1.84: 71,
    1.88: 72,
    1.92: 73,
    1.96: 74,
    2.00: 75,
    2.24: 76,
    2.48: 77,
    2.72: 78,
    2.96: 79,
    3.20: 80,
    3.44: 81,
    3.68: 82,
    3.92: 83,
    4.16: 84,
    4.40: 85,
    4.64: 86,
    4.88: 87,
    5.12: 88,
    5.36: 89,
    5.60: 90,
    5.84: 91,
    6.08: 92,
    6.32: 93,
    6.56: 94,
    6.80: 95,
    7.04: 96,
    7.28: 97,
    7.52: 98,
    7.76: 99,
    8.00: 100
}


def normalize_gravity(grav):
    return Gravity_Map(grav)


def normalize_temperature(temp):
    # maps temperature from range (-200, 200) step 4 onto range (0, 100) step 1
    # y = mx + b
    # m = 1 / 4
    # b = 50
    return (temp / 4.0) + 50


def calculate_clicks_from_center_to_edge(min, max):
    pass


def calculate_clicks_from_center(planet_val, race_center):
    if race_center > planet_val:
        return race_center - planet_val
    else:
        return planet_val - race_center


def calculate_planet_value(p_grav, p_temp, p_rad, r_grav_min, r_grav_max,
                           r_temp_min, r_temp_max, r_rad_min, r_rad_max):

    normalized_grav_min = normalize_gravity(r_grav_min)
    normalized_grav_max = normalize_gravity(r_grav_max)
    normalized_mid = normalized_grav_min + ((normalized_grav_max - normalized_grav_min) / 2)

    normalized_p_grav = normalize_gravity(p_grav)
    clicks_from_center = calculate_clicks_from_center(normalized_p_grav, normalized_mid)
    total_clicks_from_center_to_edge = calculate_clicks_from_center_to_edge(


    g_val = clicks_from_center / total_clicks_from_center_to_edge


    return 0


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("planets", help="csv of planet file")
    parser.add_argument("r_grav_min", help="Race's gravity min value")
    parser.add_argument("r_grav_max", help="Race's gravity max value")
    parser.add_argument("r_temp_min", help="Race's temperature min value")
    parser.add_argument("r_temp_max", help="Race's temperature max value")
    parser.add_argument("r_rad_min", help="Race's radiation min value")
    parser.add_argument("r_rad_max", help="Race's radiation max value")

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument("--version", action="version", version=__version__,
                        help="show the version and exit")

    args = parser.parse_args()

    logging.basicConfig(format=default_log_format)
    if(args.verbose):
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    with open(args.planets, "r") as f:
        i = 0
        for l in f:
            line = l.strip()
            if line.beginswith("#"):
                continue

            i += 1
            if i == 1:
                continue

            line_arr = line.split(",")
            p_grav = line_arr[-3]
            p_temp = line_arr[-2]
            p_rad = line_arr[-1]
            value = calculate_planet_value(
                p_grav, p_temp, p_rad,
                args.r_grav_min, args.r_grav_max,
                args.r_temp_min, args.r_temp_max,
                args.r_rad_min, args.r_rad_max
            )

            logging.info("Expected: {0!s}, Actual: {1!s}".format(
                value, line_arr[-4]))

if __name__ == "__main__":
    main(sys.argv[1:])
