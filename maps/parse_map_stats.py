#!/usr/bin/python
"""
    parse_map_stats.py

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("map_stats")
    args = parser.parse_args()

    stats = {}

    with open(args.map_stats, "r") as f:
        first_line = f.readline().strip()
        header_row = first_line.split(",")

        for header_item in header_row:
            stats[header_item] = []

        for l in f:
            line = l.strip()
            line_arr = line.split(",")

            for i in xrange(len(line_arr)):
                if i == 0:
                    stats[header_row[i]].append(line_arr[i])
                else:
                    stats[header_row[i]].append(float(line_arr[i]))

    print "Min x range: {0!s}, {1!s}".format(
        min(stats["min_x"]), max(stats["min_x"]))

    print "Max x range: {0!s}, {1!s}".format(
        min(stats["max_x"]), max(stats["max_x"]))

    print "Min y range: {0!s}, {1!s}".format(
        min(stats["min_y"]), max(stats["min_y"]))

    print "Max y range: {0!s}, {1!s}".format(
        min(stats["max_y"]), max(stats["max_y"]))

    print "Range of min distances: {0!s}, {1!s}".format(
        min(stats["min_planet_distance"]), max(stats["min_planet_distance"]))

    print "Average of min distances: {0!s}".format(
        sum(stats["min_planet_distance"]) / len(stats["min_planet_distance"]))

    print "Range zero buckets: {0!s}, {1!s}".format(
        min(stats["zero_bucket_count"]), max(stats["zero_bucket_count"]))

    print "Average zero buckets: {0!s}".format(
        sum(stats["zero_bucket_count"]) / len(stats["zero_bucket_count"]))

    print "Average non zero bucket size: {0!s}".format(
        sum(stats["avg_non_zero_buckets"]) / len(stats["avg_non_zero_buckets"]))

    print "Max bucket range: {0!s}, {1!s}".format(
        min(stats["max_non_zero_buckets"]), max(stats["max_non_zero_buckets"]))

    print "Average of average distance: {0!s}".format(
        sum(stats["avg_distance"]) / len(stats["avg_distance"]))

    print "Average of standard deviations: {0!s}".format(
        sum(stats["std_dev_distance"]) / len(stats["std_dev_distance"]))

if __name__ == "__main__":
    main(sys.argv[1:])
