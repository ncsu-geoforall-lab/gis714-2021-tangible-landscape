#!/usr/bin/env python3

"""
This activity will generate a topographic index map that indicates spatial zones of possible water accumulation .
"""

import grass.script as gs


def run_topoindex(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.topidx",
        input=scanned_elev,
        output="topoindex",
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

    run_topoindex(
        scanned_elev=elevation,
        env=env,
    )


if __name__ == "__main__":
    main()
