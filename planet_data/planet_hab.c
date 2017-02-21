/*
 * planet_hab.c
 *
 * This is the code posted on:
 * http://starsautohost.org/sahforum2/index.php?t=msg&th=2299&rid=625&S=ee625fe2bec617564d7c694e9c5379c5&pl_view=&start=0#msg_19643
 *
 * I enabled the second path for ideality calculation, since the original path
 * did not calculate the correct values (interpret the double cast correctly).
 *
 * Compile using gcc -std=gnu99 planet_hab.c -lm
 */
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#define BYTE char
#define WORD short

#define IMMUNE(a) ((a)==-1)

//simplified for this. Initialized somewhere else
struct playerDataStruct 
{
  BYTE lowerHab[3];	 // from 0 to 100 "clicks", -1 for immunity
  BYTE upperHab[3];
} player;

//in: an array of 3 bytes from 0 to 100
//out: a signed integer between -45 and 100
//hey, it was the Jeffs idea! Smile
signed long planetValueCalc(BYTE* planetHabData)
{
  signed long planetValuePoints=0,redValue=0,ideality=10000;	//in fact, they are never < 0
  WORD planetHab,habUpper,habLower,habCenter;
  WORD Excentr,habRadius,margin,Negativ,dist2Center;

  for (WORD i=0; i<3; i++) {
    habUpper = player.upperHab[i];
    if (IMMUNE(habUpper)) {			//perfect hab
      planetValuePoints += 10000;
    }
    else {	//the messy part
      habLower  = player.lowerHab[i];
      habCenter = (habUpper+habLower)/2;	//no need to precalc
      planetHab = planetHabData[i];

/*
 note: this version makes the basic assumption that habitability is
 symmetrical around the center, that is, the ideal center is located
 in the middle of the lower and upper boundaries, and both halves
 have the same value. The original algorithm seems able to cope with
 weirder definitions, i.e: bottom is 20, top is 80, center is 65,
 and hab value stretches proportionally to the different length of
 both "halves"...
*/

      dist2Center = abs(planetHab-habCenter);
      // 6
      habRadius = habCenter-habLower;
      // 10

      if (dist2Center<=habRadius) {		/* green planet */
	Excentr = 100*dist2Center/habRadius;	//note: implicit conversion to integer
	Excentr = 100 - Excentr;		//kind of reverse excentricity
	planetValuePoints += Excentr*Excentr;
	margin = dist2Center*2 - habRadius;
	if (margin>0) {		//hab in the "external quarters". dist2Center > 0.5*habRadius
	  //ideality *= (double)(3/2 - dist2Center/habRadius);	//decrease ideality up to ~50%
	
	  ideality *= habRadius*2 - margin;	//better suited for integer math
	  ideality /= habRadius*2;
	
	}
      } else {					/* red planet */
	Negativ = dist2Center-habRadius;
	if (Negativ>15) Negativ=15;
	redValue += Negativ;
      }
    }
  }

  if (redValue!=0) return -redValue;
  fprintf(stderr, "%d\n", planetValuePoints);

  planetValuePoints = sqrt((double)planetValuePoints/3)+0.9;	//rounding a la Jeffs
  fprintf(stderr, "%d\n", planetValuePoints);
  planetValuePoints = planetValuePoints * ideality/10000;	//note: implicit conversion to integer
  fprintf(stderr, "%d\n", ideality);

  return planetValuePoints;		//Thanks ConstB for starting this
}

int main(int argc, const char *argv[])
{
    if(argc != 10)
    {
        fprintf(stderr, "%s: Syntax: %s <grav_lower> <grav_upper> <temp_lower> <temp_upper> <rad_lower> <rad_upper> <p_grav> <p_temp> <p_rad>\n",
            argv[0], argv[0]);
        return 0;
    }

    player.lowerHab[0] = atoi(argv[1]);
    player.upperHab[0] = atoi(argv[2]);
    player.lowerHab[1] = atoi(argv[3]);
    player.upperHab[1] = atoi(argv[4]);
    player.lowerHab[2] = atoi(argv[5]);
    player.upperHab[2] = atoi(argv[6]);

    BYTE planetHabData[3];
    planetHabData[0] = atoi(argv[7]);
    planetHabData[1] = atoi(argv[8]);
    planetHabData[2] = atoi(argv[9]);

    printf("%d\n", (int)planetValueCalc(planetHabData));
    return 0;
}
