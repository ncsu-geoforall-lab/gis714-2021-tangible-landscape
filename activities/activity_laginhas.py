#!/usr/bin/env python3

"""
This function visualizes differences in a file that has been resampled to a coarse resolution using two different resample interpolation methods: nearest neighbor and bilinear.
"""
import grass.script as gs

def run_resamplediffs(scanned_elev, env, **kwargs):
    gs.run_command('r.resamp.interp', input='elevation', output='elev_4nn', method='nearest', overwrite=True)
    gs.run_command('r.resamp.interp', input='elevation', output='elev_4bi', method='bilinear', overwrite=True)
    gs.mapcalc('elev_diff=elev_4nn - elev_4bi', env=env, overwrite=True)
    gs.run_command('r.colors.stddev', map='elev_diff', env=env)

# this part is for testing without TL
def main():
    import os

    # get the current environment variables as a copy
    env = os.environ.copy()
    # we want to run this repetetively without deleted the created files
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    # resampling to have similar resolution as with TL
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)
    run_resamplediffs(scanned_elev=elevation, env=env)

if __name__ == "__main__":
    main()