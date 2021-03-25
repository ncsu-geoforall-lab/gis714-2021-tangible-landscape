#!/usr/bin/env python3

"""
Instructions

- Functions intended to run for each scan
  need to be named run_xxxxx

- Do not modify the parameters of the run_xxx function
  unless you know what you are doing
  see optional parameters:
  https://github.com/tangible-landscape/grass-tangible-landscape/wiki/Running-analyses-and-developing-workflows#python-workflows

- All gs.run_command/read_command/write_command/parse_command
  need to be passed env parameter (..., env=env)
"""

import grass.script as gs

# Function to show significantly high and low pixels 
def run_highestPixelValues(elev, env, **kwargs):
    gs.run_command(
        'r.neighbors',
         input=elev,
         output='smooth',
         method='average',
         flags='c',
         env=env
    )
    # Calculate univariate statistics
    stats = gs.parse_command('r.univar', map='smooth', flags='g', env=env)
    
    # Parse the stats library and capture the values for mean and standard deviation
    #for value in stats:
    #    if 'mean' in value:
    #        mean = float(value[ -7: ])
    #    if 'standard deviation' in value:
    #        sd = float(value[ -7: ])
    
    # Calculate mean, standard deviation, and thresholds for high and low
    mean = float(stats['mean'])
    sd = float(stats['stddev'])
    high = str(mean + (2*sd))
    low = str(mean - (2*sd))

    # Using map algebra create a new raster map of highest and lowest pixel values versus all others
    gs.mapcalc('high_values=if(smooth >= ' + high + ')', env=env) 
    gs.mapcalc('new_values=high_values + 1', env=env) 
    gs.mapcalc('low_values=if(smooth > ' + low + ')', env=env) 
    gs.mapcalc('final_values=high_values + low_values', env=env) 
    gs.mapcalc('final_values=if(smooth > {high}), 2, if(smooth < {high} && smooth > {low}), 1, if(smooth < {low}), 0, env=env)

    # Change colors for high and low maps
    gs.run_command('r.colors', map='final_values', color='elevation', env=env)
  
# Call main function
def main():
    import os
    # Set elevation to identify highest points
    elevation = "elev_lid792_1m"
    # get the current environment variables as a copy
    env = os.environ.copy()
    # we want to run this repetetively without deleted the created files
    env["GRASS_OVERWRITE"] = "1"
    # Set region
    gs.run_command("g.region", raster=elevation, env=env) 
    # Call function
    run_highestPixelValues(elev=elevation, env=env)


if __name__ == "__main__":
  main()
