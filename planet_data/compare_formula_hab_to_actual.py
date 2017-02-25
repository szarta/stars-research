#!/usr/bin/python
"""
    compare_formula_hab_to_actual.py

    Compares the planet hab formula to actual values from the Stars! game.

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse
import logging
import math
import subprocess

__version__ = "%(prog)s 1.0.1 (Rel: 21 Feb 2017)"
default_log_format = "%(filename)s:%(levelname)s:%(asctime)s] %(message)s"

# The gravity values are not linear, but still map to (0, 100) step 1
# Although the bottom-most values are a little strange in that they double
# increment
Gravity_Map = {
    "-1": "-1",
    "0.12": 0,
    "0.13": 2,
    "0.14": 4,
    "0.15": 6,
    "0.16": 8,
    "0.17": 9,
    "0.18": 11,
    "0.19": 12,
    "0.20": 13,
    "0.21": 14,
    "0.22": 15,
    "0.24": 16,
    "0.25": 17,
    "0.27": 18,
    "0.29": 19,
    "0.31": 20,
    "0.33": 21,
    "0.36": 22,
    "0.40": 23,
    "0.44": 24,
    "0.50": 25,
    "0.51": 26,
    "0.52": 27,
    "0.53": 28,
    "0.54": 29,
    "0.55": 30,
    "0.56": 31,
    "0.58": 32,
    "0.59": 33,
    "0.60": 34,
    "0.62": 35,
    "0.64": 36,
    "0.65": 37,
    "0.67": 38,
    "0.69": 39,
    "0.71": 40,
    "0.73": 41,
    "0.75": 42,
    "0.78": 43,
    "0.80": 44,
    "0.83": 45,
    "0.86": 46,
    "0.89": 47,
    "0.92": 48,
    "0.96": 49,
    "1.00": 50,
    "1.04": 51,
    "1.08": 52,
    "1.12": 53,
    "1.16": 54,
    "1.20": 55,
    "1.24": 56,
    "1.28": 57,
    "1.32": 58,
    "1.36": 59,
    "1.40": 60,
    "1.44": 61,
    "1.48": 62,
    "1.52": 63,
    "1.56": 64,
    "1.60": 65,
    "1.64": 66,
    "1.68": 67,
    "1.72": 68,
    "1.76": 69,
    "1.80": 70,
    "1.84": 71,
    "1.88": 72,
    "1.92": 73,
    "1.96": 74,
    "2.00": 75,
    "2.24": 76,
    "2.48": 77,
    "2.72": 78,
    "2.96": 79,
    "3.20": 80,
    "3.44": 81,
    "3.68": 82,
    "3.92": 83,
    "4.16": 84,
    "4.4": 85,
    "4.64": 86,
    "4.88": 87,
    "5.12": 88,
    "5.36": 89,
    "5.60": 90,
    "5.84": 91,
    "6.08": 92,
    "6.32": 93,
    "6.56": 94,
    "6.80": 95,
    "7.04": 96,
    "7.28": 97,
    "7.52": 98,
    "7.76": 99,
    "8.00": 100
}


def normalize_gravity(grav):
    return Gravity_Map[grav]


def normalize_temperature(temp):
    if(int(temp) == -1):
        return -1

    actual_temp = int(temp)
    # maps temperature from range (-200, 200) step 4 onto range (0, 100) step 1
    # y = mx + b
    # m = 1 / 4
    # b = 50
    return int((actual_temp / 4.0) + 50)


def calculate_hab_points(hab_radius, distance_to_center):
    """
    These calculations courtesy:

    m.a@stars
    http://starsautohost.org/sahforum2/index.php?t=msg&th=2299&rid=625&S=ee625fe2bec617564d7c694e9c5379c5&pl_view=&start=0#msg_19643
    """
    planet_value_points = 0
    red_value = 0
    ideality_correction = 1.0

    if distance_to_center <= hab_radius:
        ex_center = 100 * distance_to_center // hab_radius
        ex_center = 100 - ex_center
        planet_value_points += ex_center * ex_center

        margin = (distance_to_center * 2) - hab_radius
        if margin > 0:
            ideality_correction *= (hab_radius * 2) - margin
            ideality_correction /= (hab_radius * 2)
    else:
        negative = distance_to_center - hab_radius
        if negative > 15:
            negative = 15
        red_value += negative

    return (planet_value_points, red_value, ideality_correction)


def calculate_planet_value(p_grav, p_temp, p_rad,
                           r_grav_immune, r_grav_min, r_grav_max,
                           r_temp_immune, r_temp_min, r_temp_max,
                           r_rad_immune, r_rad_min, r_rad_max):

    """
    These calculations courtsey:

    m.a@stars
    http://starsautohost.org/sahforum2/index.php?t=msg&th=2299&rid=625&S=ee625fe2bec617564d7c694e9c5379c5&pl_view=&start=0#msg_19643
    """
    planet_value_points = 0
    red_value = 0
    ideality = 10000

    if(r_grav_immune):
        planet_value_points += 10000
    else:
        normalized_grav_min = normalize_gravity(r_grav_min)
        normalized_grav_max = normalize_gravity(r_grav_max)
        normalized_grav_mid = (normalized_grav_max + normalized_grav_min) / 2

        normalized_p_grav = normalize_gravity(p_grav)

        distance_to_center = abs(normalized_p_grav - normalized_grav_mid)
        hab_radius = normalized_grav_mid - normalized_grav_min

        (pv, r, ic) = calculate_hab_points(hab_radius, distance_to_center)
        planet_value_points += pv
        red_value += r
        ideality = int(ideality * ic)

    if(r_temp_immune):
        planet_value_points += 10000
    else:
        normalized_temp_min = normalize_temperature(r_temp_min)
        normalized_temp_max = normalize_temperature(r_temp_max)
        normalized_temp_mid = (normalized_temp_max + normalized_temp_min) / 2
        normalized_p_temp = normalize_temperature(p_temp)

        distance_to_center = abs(normalized_p_temp - normalized_temp_mid)
        hab_radius = normalized_temp_mid - normalized_temp_min

        (pv, r, ic) = calculate_hab_points(hab_radius, distance_to_center)
        planet_value_points += pv
        red_value += r
        ideality = int(ideality * ic)

    if(r_rad_immune):
        planet_value_points += 10000
    else:
        r_rad_mid = (int(r_rad_min) + int(r_rad_max)) / 2
        distance_to_center = abs(int(p_rad) - r_rad_mid)
        hab_radius = int(r_rad_mid) - int(r_rad_min)
        (pv, r, ic) = calculate_hab_points(hab_radius, distance_to_center)
        planet_value_points += pv
        red_value += r
        ideality = int(ideality * ic)

    if red_value != 0:
        return -1 * red_value

    planet_value_points = int(math.sqrt(planet_value_points / 3.0) + 0.9)
    planet_value_points = (planet_value_points * ideality) // 10000
    return planet_value_points


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

    grav_immune = False
    if args.r_grav_min == "-1" and args.r_grav_max == "-1":
        grav_immune = True

    temp_immune = False
    if args.r_temp_min == "-1" and args.r_temp_max == "-1":
        temp_immune = True

    rad_immune = False
    if args.r_rad_min == "-1" and args.r_rad_max == "-1":
        rad_immune = True

    matches = 0
    failures = 0
    with open(args.planets, "r") as f:
        i = 0
        for l in f:
            line = l.strip()
            if line.startswith("#"):
                continue

            i += 1
            if i == 1:
                continue

            line_arr = line.split(",")
            p_grav = line_arr[-3]
            p_temp = line_arr[-2]
            p_rad = line_arr[-1]

            if p_grav == "0" and p_temp == "0" and p_rad == "0":
                continue

            value = calculate_planet_value(
                p_grav, p_temp, p_rad,
                grav_immune, args.r_grav_min, args.r_grav_max,
                temp_immune, args.r_temp_min, args.r_temp_max,
                rad_immune, args.r_rad_min, args.r_rad_max
            )

            cmd = "./planet_hab_calculator {0!s} {1!s} {2!s} {3!s} {4!s} {5!s} {6!s} {7!s} {8!s}".format(
                normalize_gravity(args.r_grav_min),
                normalize_gravity(args.r_grav_max),
                normalize_temperature(args.r_temp_min),
                normalize_temperature(args.r_temp_max),
                args.r_rad_min, args.r_rad_max,
                normalize_gravity(p_grav),
                normalize_temperature(p_temp),
                p_rad)

            result = subprocess.check_output(cmd, shell=True)

            c_result = int(result.strip())
            actual = int(line_arr[-4].replace("%", ""))
            py_result = int(value)

            if c_result == actual and py_result == actual:
                logging.debug("{0!s}: Expected: {1!s}, CCalc: {2!s}, Actual: {3!s}".format(
                    line_arr[1], py_result, c_result, actual))

                matches += 1
            else:
                logging.debug("{0!s}: Expected: {1!s}, CCalc: {2!s}, Actual: {3!s}".format(
                    line_arr[1], py_result, c_result, actual))

                failures += 1

        logging.info("Matches: {0!s}, Failures: {1!s}".format(matches, failures))


if __name__ == "__main__":
    main(sys.argv[1:])
