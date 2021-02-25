#!/usr/bin/env python3

"""
This activity will draw a map that illustrates any concave topography in the raster.
"""

import grass.script as gs


def run_topo_par(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.param.scale",
        input=scanned_elev,
        output="feat_verticalcurv",
        method="profc",
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
    # resampling to have similar resolution as with TL
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)

    run_topo_par(
        scanned_elev=elevation,
        env=env,
    )


if __name__ == "__main__":
    main()
