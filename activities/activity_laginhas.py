#!/usr/bin/env python3

"""
Comparing differences for resampling methods: average & median.
"""
import grass.script as gs


def run_resamplediffs(scanned_elev, env, **kwargs):
    raster_region = gs.raster_info(scanned_elev)
    res = (raster_region["nsres"] + raster_region["ewres"]) / 2
    env2 = env.copy()
    env2["GRASS_REGION"] = gs.region_env(res=res * 3)
    gs.run_command(
        "r.resamp.stats",
        input=scanned_elev,
        output="elev_avg",
        method="average",
        env=env2,
    )
    gs.run_command(
        "r.resamp.stats",
        input=scanned_elev,
        output="elev_med",
        method="median",
        env=env2,
    )
    gs.mapcalc("elev_diff=abs(elev_avg - elev_med)", env=env2)
    gs.run_command("r.colors", map="elev_diff", color="reds", env=env2)


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
    run_resamplediffs(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
