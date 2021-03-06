#	___CoordTransforms___
# 	Coordinates transforms script.
#
#   Thanks: the coordinate transforms are based on the Mathworks Aerospace references
#           and relevant work at pydoc.net
#

import math
import sys, getopt
import numpy as np
from math import pow, cos, sin, sqrt, degrees, radians, atan2, pi
from scipy import cos, sin, arctan, sqrt, arctan2

# 	Change based on your files and LLA ENU Origin
LLA_ENU_Point = np.array([47.135388888888890, 8.688611111111111, 919.5254262437646] )

# 	assume WGS84
wgs84_a = 6378137.0
wgs84_f = 1.0 / 298.257223563
wgs84_e2 = 2 * wgs84_f - np.power(wgs84_f,2)


# 	Coordinate conversion functions
def lla2ecef(lonLatAlt):
	# LLA2ECEF Conversion (meters)

    lonDeg, latDeg, alt = lonLatAlt
    a, e2 = wgs84_a, wgs84_e2
    lon = radians(lonDeg) 
    lat = radians(latDeg) 
    chi = sqrt(1 - e2 * sin(lat) ** 2)
    q = (a / chi + alt) * cos(lat)
    return (q * cos(lon),
            q * sin(lon),
            ((a * (1 - e2) / chi) + alt) * sin(lat))


def ecef2lla(ecef):
	# ECEF2LLA (degrees)

    x, y, z = ecef
    a, e2, f = wgs84_a, wgs84_e2, wgs84_f
    lon = atan2(y, x)
    s = sqrt(x ** 2 + y ** 2)
    step = 0
    lat = None
    latPrev = 0
    converged = False
    while not converged:
        if step == 0:
            beta = atan2(z, (1 - f) * s)  # initial guess
        else:
            beta = atan2((1 - f) * sin(lat), cos(lat))  # improved guess
        lat = atan2(z + (e2 * (1 - f) / (1 - e2)) * a * sin(beta) ** 3,
                    s - e2 * a * cos(beta) ** 3)
        if (lat - latPrev) < 1e-4:
            converged = True
        latPrev = lat
        step += 1
    N = a / sqrt(1 - e2 * sin(lat) ** 2)
    alt = s * cos(lat) + (z + e2 * N * sin(lat)) * sin(lat) - N
    return (degrees(lon),
            degrees(lat),
            alt)


def ecef2enu(LonLatAlt_orig, ecef):
    # ECEF2ENU (meters)
    x, y, z = ecef
    ox, oy, oz = lla2ecef(LonLatAlt_orig)
    dx, dy, dz = (x - ox, y - oy, z - oz)
    lonDeg, latDeg, _ = LonLatAlt_orig
    lon = radians(lonDeg)
    lat = radians(latDeg)
    return (-sin(lon) * dx + cos(lon) * dy,
            -sin(lat) * cos(lon) * dx - sin(lat) * sin(lon) * dy + cos(lat) * dz,
            cos(lat) * cos(lon) * dx + cos(lat) * sin(lon) * dy + sin(lat) * dz)


def enu2ecef(LonLatAlt_orig, enu):
    # ENU2ECEF (meters)

    e, n, u = enu
    lonDeg, latDeg, _ = LonLatAlt_orig
    lon = radians(lonDeg)
    lat = radians(latDeg)
    ox, oy, oz = lla2ecef(LonLatAlt_orig)
    return (ox - sin(lon) * e - cos(lon) * sin(lat) * n + cos(lon) * cos(lat) * u,
            oy + cos(lon) * e - sin(lon) * sin(lat) * n + cos(lat) * sin(lon) * u,
            oz + cos(lat) * n + sin(lat) * u)


def lla2enu(LonLatAlt_orig, lonLatAlt):
    return ecef2enu(LonLatAlt_orig, lla2ecef(lonLatAlt))


def enu2lla(LonLatAlt_orig, enu):
    return ecef2lla(enu2ecef(LonLatAlt_orig, enu))



def main():

	PathENU = np.array([[120.0, 100.0, 150.0, 0.0],[130.0, 110.0, 140.0, 0.0]]) # just an example

	Nx,Ny = PathENU.shape

	ECEF_X = np.zeros(Nx); ECEF_Y = np.zeros(Nx); ECEF_Z = np.zeros(Nx)
	lat = np.zeros(Nx); lon = np.zeros(Nx); alt = np.zeros(Nx)

	for i in range(0,Nx):
		lon[i], lat[i], alt[i] = enu2lla(LLA_ENU_Point,PathENU[i,0:3])
        print lon[i]
        print lat[i]
        print alt[i]

if __name__ == "__main__":
    main()
