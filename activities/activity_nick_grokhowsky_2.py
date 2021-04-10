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

#!/usr/bin/env python3

import grass.script as gs


# Function to show significantly high and low pixels
def run_significantValues(elev, env, **kwargs):
    # Create rules for r.recode
    rules = ["*:-2.58: -3:-3",
            "-2.58:-1.96:-2:-2",
            "-1.96:-1.65:-1:-1",
            "-1.65:1.65:0:0",
            "1.65:1.96:1:1",
            "1.96:2.58:2:2",
            "2.58:*:3:3"]

    gs.run_command(
        "r.neighbors", input=elev, output="smooth", method="average", flags="c", env=env
    )
    # Calculate univariate statistics
    stats = gs.parse_command("r.univar", map="smooth", flags="g", env=env)

    # Calculate mean, standard deviation, and thresholds for high and low
    mean = float(stats["mean"])
    sd = float(stats["stddev"])

    # Using map algebra create a new raster map of z-scores
    gs.mapcalc(f"out = (smooth - {mean}) / {sd}", env=env)

    # Recode out raster with significance bins
    gs.write_command("r.recode", input="out", output="out", rules="-", stdin="\n".join(rules), env=env)


    # Change colors for high and low maps
    gs.run_command("r.colors", map="out", color="elevation", env=env)


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
    run_significantValues(elev=elevation, env=env)


if __name__ == "__main__":
    main()

