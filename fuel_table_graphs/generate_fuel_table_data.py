#!/usr/bin/python
"""
    generate_fuel_table_data.py

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse
import logging
import math

from src.factory import build_technology
from src.model.enumerations import TechnologyId
from src.language import Language_Map
from src.language import load_language_map



__version__ = "%(prog)s 1.0.0 (Rel: 15 Jan 2017)"
default_log_format = "%(filename)s:%(levelname)s:%(asctime)s] %(message)s"


def main(argv):
    parser = argparse.ArgumentParser()

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

    load_language_map("resources/strings/english_strings.json")

    tech = build_technology()

    engines = [
        TechnologyId.SettlersDelight,
        TechnologyId.QuickJump5,
        TechnologyId.FuelMizer,
        TechnologyId.LongHump6,
        TechnologyId.DaddyLongLegs7,
        TechnologyId.AlphaDrive8,
        TechnologyId.TransGalacticDrive,
        TechnologyId.Interspace10,
        TechnologyId.TransStar10,
        TechnologyId.RadiatingHydroRamScoop,
        TechnologyId.SubGalacticFuelScoop,
        TechnologyId.TransGalacticFuelScoop,
        TechnologyId.TransGalacticSuperScoop,
        TechnologyId.TransGalacticMizerScoop,
        TechnologyId.GalaxyScoop,
        TechnologyId.EnigmaPulsar
    ]

    for id in engines:
        write_fuel_table(id, tech[id])


def write_fuel_table(id, engine):
    """
    Writes out the fuel table to be plotted by GNUPlot
    """
    engine_name = Language_Map["technology-names"][id]
    engine_name = engine_name.replace(" ", "_")
    engine_name = engine_name.replace("'", "")
    logging.debug("Writing {0}, id: {1!s}".format(engine_name, id))
    out_filepath = "{0}.dat".format(engine_name)
    ft = engine.fuel_usage_table
    with open(out_filepath, "w") as f:
        for i in xrange(len(ft)):
            fuel_value = ft[i]
            converted = convert_table_value(fuel_value)
            logging.debug(
                "val: {0}, converted_value: {1}".format(fuel_value, converted))
            f.write("{0} {1}\n".format(i, converted))


def convert_table_value(fuel_usage_value):
    """
    The graph is a little skewed, so this prepares the data for that.

    0 = 0
    1 = 25%
    2 = 50%
    3 = 100%
    4 = 200%
    5 = 400%
    6 = 800%
    7 = 1600% (not shown)

    Intermediate values scale between those values. (5.5 is 600%)
    """
    if fuel_usage_value < 25:
        return 0.04 * fuel_usage_value
    else:
        return math.log((fuel_usage_value / 12.5), 2)

if __name__ == "__main__":
    main(sys.argv[1:])
