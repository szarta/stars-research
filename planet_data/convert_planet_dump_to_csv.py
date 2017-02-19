#!/usr/bin/python
"""
    convert_planet_dump_to_csv.py

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse
import logging
import re

__version__ = "%(prog)s 1.0.0 (Rel: 19 Feb 2017)"
default_log_format = "%(filename)s:%(levelname)s:%(asctime)s] %(message)s"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("planets", help="Planet dump file (e.g. Game.pla)")
    parser.add_argument("universe", help="Universe dump file (e.g. Game.map)")

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

    planet_info = {}

    with open(args.universe, "r") as f:
        i = 0
        for l in f:
            i += 1
            if i == 1:
                continue

            line = l.strip()
            line_arr = re.split(r'\t+', line)
            planet_name = line_arr[3]
            planet_id = line_arr[0]
            planet_x = line_arr[1]
            planet_y = line_arr[2]
            planet_info[planet_name] = {}
            planet_info[planet_name]["id"] = planet_id
            planet_info[planet_name]["x"] = planet_x
            planet_info[planet_name]["y"] = planet_y

    with open(args.planets, "r") as f:
        i = 0
        for l in f:
            i += 1
            if i == 1:
                continue

            line = l.strip()
            line_arr = re.split(r'\t+', line)
            planet_name = line_arr[0]
            homeworld = "1"
            planet_value = "{0!s}".format(line_arr[5])
            if(line_arr[1] == "0"):
                homeworld = "0"
                planet_value = line_arr[2]

            ironium = line_arr[-3]
            boranium = line_arr[-2]
            germanium = line_arr[-1]

            planet_info[planet_name]["homeworld"] = homeworld
            planet_info[planet_name]["value"] = planet_value
            planet_info[planet_name]["ironium_c"] = ironium
            planet_info[planet_name]["boranium_c"] = boranium
            planet_info[planet_name]["germanium_c"] = germanium

            planet_info[planet_name]["gravity"] = "0"
            planet_info[planet_name]["temperature"] = "0"
            planet_info[planet_name]["radiation"] = "0"

    with open("out.csv", "w") as out:
        out.write(
            "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}".format(
                "Planet Id", "Planet Name", "X", "Y", "Homeworld",
                "Ironium MC", "Boranium MC", "Germanium MC",
                "Planet Value", "Gravity", "Temperature", "Radiation\n"))

        for planet_name in planet_info.keys():
            p = planet_info[planet_name]
            out.write(
                "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(
                    p["id"], planet_name, p["x"], p["y"], p["homeworld"],
                    p["ironium_c"], p["boranium_c"], p["germanium_c"],
                    p["value"],
                    p["gravity"], p["temperature"], p["radiation"]))


if __name__ == "__main__":
    main(sys.argv[1:])
