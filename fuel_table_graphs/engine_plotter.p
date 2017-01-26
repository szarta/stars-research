#
# engine_plotter.p
#
# This is a gnuplot script that creates the graphs for engine fuel tables.
#
# Engine fuel tables go from 0 to 6, representing:
#   [0, 25%, 50%, 100%, 200%, 400%, 800%]
#
# Because gnuplot has trouble with logplots and 0 for a value.
#
# I use another script to generate the fuel tables from the actual engine
# build-ups.  The graph looks similar enough to the originals, I edit in the
# damage zones for Warp 9-10 and the battle speed after generating here.
#
# They are a little large than the originals, by design.
#
# :author: Brandon Arrendondo
# :license: MIT
#
set terminal pngcairo transparent truecolor font "Arial Bold,10" size 350, 250
#set terminal pngcairo truecolor font "Arial Bold,10" size 350, 250
set output "out.png"

set title "Fuel Usage vs. Warp Speed"
set grid
set xrange [0:10]
set xlabel "Warp Speed"

# This sets the y scale to have percent signs, commented because I am manually
# setting the y labels
#set format y '%2.0f%%'

set yrange [0:6.5]
set ytics ("" 0, "25%%" 1, "50%%" 2, "100%%" 3, "200%%" 4, "400%%" 5, "800%%" 6)

# Log scale has problems with 0
#set logscale y 2

f(x) = 3
#engine = "fuel_table/Settlers_Delight.dat"
#engine = "fuel_table/Quick_Jump_5.dat"
#engine = "fuel_table/Fuel_Mizer.dat"
#engine = "fuel_table/Long_Hump_6.dat"
#engine = "fuel_table/Daddy_Long_Legs_7.dat"
#engine = "fuel_table/Alpha_Drive_8.dat"
#engine = "fuel_table/Trans-Galactic_Drive.dat"
#engine = "fuel_table/Interspace-10.dat"
#engine = "fuel_table/Trans-Star_10.dat"
#engine = "fuel_table/Radiating_Hydro-Ram_Scoop.dat"
#engine = "fuel_table/Sub-Galactic_Fuel_Scoop.dat"
#engine = "fuel_table/Trans-Galactic_Fuel_Scoop.dat"
#engine = "fuel_table/Trans-Galactic_Super_Scoop.dat"
#engine = "fuel_table/Trans-Galactic_Mizer_Scoop.dat"
#engine = "fuel_table/Galaxy_Scoop.dat"
engine = "fuel_table/Enigma_Pulsar.dat"

set xtic scale 1 1

plot f(x) notitle lt rgb "#000000", engine using 1:2 with lines notitle lt rgb "#000081"
