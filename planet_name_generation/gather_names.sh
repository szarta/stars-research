#!/bin/sh
#------------------------------------------------------------------------------
# Just builds the unique list of names from all of the other lists.
#
# Author: Brandon Arrendondo
# License: MIT
#------------------------------------------------------------------------------

cat name_lists/*.txt >> names.txt
sort -u -o names.txt names.txt
