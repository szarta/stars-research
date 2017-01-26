#!/usr/bin/python
"""
    get_map_stats.py

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import os
import argparse
import math
import logging
import numpy as np
from collections import Counter


def calculate_dimensions(points):
    max_across = 0
    min_across = 3000

    for point in points:
        (x, y) = point

        if x < min_across:
            min_across = x

        if y < min_across:
            min_across = y

        if x > max_across:
            max_across = x

        if y > max_across:
            max_across = y

    universe_length = max_across - min_across
    universe_size = 0
    if universe_length <= 400:
        universe_size = 400
    elif universe_length <= 800:
        universe_size = 800
    elif universe_length <= 1200:
        universe_size = 1200
    elif universe_length <= 1600:
        universe_size = 1600
    else:
        universe_size = 2000

    return universe_size


def get_bucket(point):
    (x, y) = point
    x -= 1000
    y -= 1000

    return (x / 100, y / 100)


def distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def build_density_buckets(universe_size, points):
    expected_buckets = universe_size / 100
    density_buckets = [[0 for x in range(expected_buckets)] for y in range(expected_buckets)]

    for point in points:
        (x, y) = point

        b = get_bucket(point)
        (i, j) = b
        density_buckets[i][j] = density_buckets[i][j] + 1

    return density_buckets


def get_universe_bounds(points):
    max_x = 0
    max_y = 0
    min_x = 3000
    min_y = 3000

    for p in points:
        (x, y) = p

        if x < min_x:
            min_x = x

        if y < min_y:
            min_y = y

        if y > max_y:
            max_y = y

        if x > max_x:
            max_x = x

    return (min_x, max_x, min_y, max_y)


def get_planet_distances(points):
    distances = []

    marked = {}

    for p in points:
        marked[p] = [p]

    for p in points:
        for q in points:
            if(not q in marked[p]):
                dist = distance(p, q)
                distances.append(dist)
                marked[p].append(q)
                marked[q].append(p)

    return distances


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('maps', nargs="+")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        format='[map_stats:%(levelname)s:%(asctime)s] %(message)s')

    if(args.verbose):
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    for map in args.maps:
        with open(map, "r") as m:
            logging.debug("Parsing {0!s}".format(map))

            points = []
            for l in m:
                line = l.strip()
                if not(line.startswith("#")):
                    line_args = line.split()
                    x = int(line_args[1])
                    y = int(line_args[2])
                    points.append((x, y))

            universe_size = calculate_dimensions(points)
            num_planets = len(points)
            total_expected_buckets = (universe_size ** 2) / (100 ** 2)
            universe_density = (num_planets * 1.0) / total_expected_buckets
            density_buckets = build_density_buckets(universe_size, points)
            (min_x, max_x, min_y, max_y) = get_universe_bounds(points)
            planet_distances = get_planet_distances(points)
            min_planet_distance = min(planet_distances)
            avg_distances = sum(planet_distances) / len(planet_distances)
            std_dev_distances = np.std(np.array(planet_distances))

            # average of non-zero density squares
            non_zero_buckets = []
            zero_bucket_count = 0
            for b in density_buckets:
                for y in b:
                    if y == 0:
                        zero_bucket_count += 1
                    else:
                        non_zero_buckets.append(y)

            avg_non_zero_buckets = (sum(non_zero_buckets) * 1.0) / len(non_zero_buckets)
            max_non_zero_buckets = max(non_zero_buckets)

            logging.debug("Size of Universe = {0!s}".format(universe_size))
            logging.debug("Num Planets = {0!s}".format(num_planets))
            logging.debug("Density per 100 square light year = {0!s}".format(
                universe_density))

            logging.debug("Density map: ")
            for b in density_buckets:
                logging.debug(b)

            logging.debug("Density numbers: ")
            density_values = []
            for b in density_buckets:
                for j in b:
                    density_values.append(j)

            c = Counter(density_values)
            with open("histo.csv", "a") as f:
                for i in xrange(9):
                    if i in c.keys():
                        f.write("{0!s},".format(c[i]))
                    else:
                        f.write("0,")

                f.write("0\n")

            logging.debug("Min x: {0!s}, Max x: {1!s}".format(
                min_x, max_x))

            logging.debug("Min y: {0!s}, Max y: {1!s}".format(
                min_y, max_y))

            logging.debug("Min distance = {0!s}".format(
                min_planet_distance))

            logging.debug("Average distance = {0!s}".format(avg_distances))
            logging.debug("Standard deviation = {0!s}".format(std_dev_distances))

            if(not os.path.exists("out.csv")):
                with open("out.csv", "a") as f:
                    f.write("{0!s},{1!s},{2!s},{3!s},{4!s},{5!s},{6!s},{7!s},{8!s},{9!s},{10!s},{11!s},{12!s},{13!s}\n".format(
                        "path", "universe_size", "num_planets",
                        "universe_density", "min_x", "max_x", "min_y", "max_y",
                        "min_planet_distance", "avg_distance",
                        "std_dev_distance", "zero_bucket_count",
                        "avg_non_zero_buckets", "max_non_zero_buckets"))

            with open("out.csv", "a") as f:
                f.write("{0!s},{1!s},{2!s},{3!s},{4!s},{5!s},{6!s},{7!s},{8!s},{9!s},{10!s},{11!s},{12!s},{13!s}\n".format(
                    map, universe_size, num_planets, universe_density,
                    min_x, max_x, min_y, max_y,
                    min_planet_distance, avg_distances, std_dev_distances,
                    zero_bucket_count, avg_non_zero_buckets,
                    max_non_zero_buckets))


if __name__ == "__main__":
    main(sys.argv[1:])
