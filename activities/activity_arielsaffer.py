import grass.script as gs
import datetime
# you may need to install this package
import pytz 
# you probably need to install this package
from timezonefinder import TimezoneFinder 
obj = TimezoneFinder()

# compute solar irradiance (W/m2) for a given day and hour 
# and extract the shades cast by topography, using the time zone
# of the surface location (based on NE corner)

def run_radiance_now(scanned_elev, env, **kwargs):

    # Get the current day/time
    today = datetime.datetime.today()
    # Get the lat and lon of the NE corner of the computation region
    map_loc = gs.read_command('g.region',flags='bg',raster=scanned_elev)
    long = float(map_loc.split()[4:6][0].split('=')[1])
    lat = float(map_loc.split()[4:6][1].split('=')[1])
    # Identify the time zone of the mapped region
    map_timezone = obj.timezone_at(lng=long, lat=lat)
    # Convert the current day/time to the time in that timezone
    maptime = today.astimezone(pytz.timezone(map_timezone))
    # Extract day of year and hour
    day = maptime.timetuple().tm_yday
    current_time = maptime.hour

    # precompute slope and aspect
    gs.run_command('r.slope.aspect', elevation=scanned_elev, slope='slope', aspect='aspect', env=env)
    gs.run_command('r.sun', elevation=scanned_elev, slope='slope', aspect='aspect', beam_rad='beam', day=day, time=current_time, env=env)

    # extract shade and set color to black and white
    gs.mapcalc("shade = if(beam == 0, 0, 1)", env=env)
    gs.run_command('r.colors', map='beam', color='grey')


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
    radiance_now(scanned_elev=elevation, env=env)

if __name__ == "__main__":
    main()