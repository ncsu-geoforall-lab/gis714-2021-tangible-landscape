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


def run_ponds(scanned_elev, env, **kwargs):
    repeat = 20
    input_dem = scanned_elev
    output = "tmp_filldir"
    for i in range(repeat):
        gs.run_command(
          'r.fill.dir', 
          input=input_dem, 
          output=output, 
          direction="tmp_dir", 
          env=env
        )
        input_dem = output
    # filter depression deeper than 0.1 m to
    gs.mapcalc('{new} = if({out} - {scan} > 0.1, {out} - {scan}, null())'.format(
                                                                                 new='ponds', 
                                                                                 out=output,
                                                                                 scan=scanned_elev
                                                                                ), env=env)
    gs.write_command(
      'r.colors', 
      map='ponds', 
      rules='-', 
      stdin='0% aqua\n100% blue', 
      env=env
    )
# this part is for testing without TL


def run_waterflow(scanned_elev, env, **kwargs):
    # first we need to compute x- and y-derivatives
    gs.run_command(
      'r.slope.aspect', 
      elevation=scanned_elev, 
      dx='scan_dx', 
      dy='scan_dy', 
      env=env
    )
    gs.run_command(
      'r.sim.water', 
      elevation=scanned_elev, 
      dx='scan_dx', 
      dy='scan_dy',
      rain_value=250, 
      depth='flow', 
      env=env
    )


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
    gs.run_command("g.copy", raster=[elev_resampled, "scan_saved"], env=env)

    # Test functions
    run_ponds(
      scanned_elev=elev_resampled, 
      env=env
    )
    run_waterflow(
      scanned_elev=elev_resampled, 
      env=env
    )


if __name__ == "__main__":
    main()
