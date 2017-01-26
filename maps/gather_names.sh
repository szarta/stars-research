#!/bin/sh
#------------------------------------------------------------------------------
# Iterates over each map file in the subdirectories and pulls out each planet
# names, putting them into names.txt
#
# I wrote this to data-mine the original planet names used in Stars!
#
# Author: Brandon Arrendondo
# License: MIT
#------------------------------------------------------------------------------

for i in $(find -type f -name "*.map")
do
    awk 'NR>1 {print $1=$2=$3=""; print $0}' $i | sed -e "/^\s*$/d" | sed -e "s/^\s*//" >> names.txt
done

fromdos names.txt
sort -u -o names.txt names.txt
