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
from datetime import datetime


def run_sim_wave(scanned_elev, env, **kwargs):
    # This will attempt to simulate a manifestation of a wave over the region
    # represented by the tangible landscape. This wave will be represented by
    # surface pressure perturbations, with some random noise added in. This
    # will also account for the elevation using the simple '1 km -> 100 hPa'
    # rule, which works for the example data set, in which elevations are all
    # relatively close to sea level. Finally, the wave will also move at a
    # speed of 10 m/s.
    base_pres = 1.01e5 # call standard pressure at sea level 1010 hPa
    wave_amplitude = 100 # say we have a 1 hPa amplitude wave (not necessarily realistic, but want to make the effect visible in the resulting map)
    wavelength = 300 # with 300 m wavelength
    wave_vel = 10 # moving at 10 m/s
    cur_sec = float(datetime.now().strftime("%S"))
    interval = 75
    gs.mapcalc(
        'pres = {base_pres}-({scanned_elev}*10) + {wave_amplitude}*(sin((x()-{cur_sec}*{wave_vel})*360/{wavelength})) + rand(-20,20)'
        .format(base_pres = base_pres, wave_amplitude = wave_amplitude,
                wavelength = wavelength, scanned_elev=scanned_elev,
                cur_sec = cur_sec, wave_vel = wave_vel),
        seed = 'auto', env=env)
    gs.run_command(
        "r.contour",
        input='pres',
        output="contours",
        step=interval,
        flags="t",
        env=env,
    )



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

    # this will run the wave simulation
    run_sim_wave(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()