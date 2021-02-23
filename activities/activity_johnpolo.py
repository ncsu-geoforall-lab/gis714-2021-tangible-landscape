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


def run_topo_par(scanned_elev, morphmap, select_meth, env, **kwargs):
    gs.run_command('r.param.scale', input=scanned_elev, output=morphmap, method=select_meth, env=env, overwrite=True)
    

# this part is for testing without TL
def main():
    import os

    # get the current environment variables as a copy
    env = os.environ.copy()
    # we want to run this repetetively without deleted the created files
    env["GRASS_OVERWRITE"] = "1"

    elevation = "elev_lid792_1m"
    select_meth = 'profc'
    
    run_topo_par(scanned_elev=elevation, morphmap='feat_verticalcurv', select_meth=select_meth, env=env)

if __name__ == "__main__":
    main()
