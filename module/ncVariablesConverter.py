#from jdcal import jd2gcal, MJD_0
from datetime import datetime as dt
from datetime import timedelta
from pyproj import Proj

def covertJulianToDate(nc):
    """
    ユリウス時間を通常の日付に変換する。
    fvcomの時間はItime(days)とItime2(msec)からなる。ユリウス時間を採用している。
    基準日が分かっている(1857-11-17 0:00:00)ため、そこからtimeDeltaにより計算する
    """
    Itime  = nc.variables['Itime'][:]
    Itime2 = nc.variables['Itime2'][:]
    MJD_0 = dt(1857,11,17,0,0,0)
    date = [MJD_0 + timedelta(days = int(itime))+ timedelta(milliseconds=int(itime2)) \
            for itime,itime2 in zip(Itime,Itime2)]

    return date

def convertCoordsToLonlat(nc):
    """
    xy座標をlonlatに変換する。
    nc : result file of netCDF4 format
    zone : UTM zone (Tokyo=54)
    """

    x =nc.variables['x'][:]
    y =nc.variables['y'][:]

    e2u_conv=Proj(proj='utm', zone=54, ellps='WGS84')

    rslt = [e2u_conv(lon,lat,inverse=True) for lon,lat in zip(x,y)]
    lon = [rslt[i][0] for i in range(len(rslt))]
    lat = [rslt[i][1] for i in range(len(rslt))]

    return lon,lat

#debug
def main():
    import netCDF4
    nc = netCDF4.Dataset("../sample.nc",'r')
    #print(nc.variables)
    date = covertJulianToDate(nc)
    print(date[:5])


if __name__ == "__main__":
    main()



"""
{'nprocs': <class 'netCDF4._netCDF4.Variable'>
int32 nprocs()
    long_name: number of processors
unlimited dimensions:
current shape = ()
filling on, default _FillValue of -2147483647 used, 'partition': <class 'netCDF4._netCDF4.Variable'>
int32 partition(nele)
    long_name: partition
unlimited dimensions:
current shape = (5645,)
filling on, default _FillValue of -2147483647 used, 'x': <class 'netCDF4._netCDF4.Variable'>
float64 x(node)
    long_name: nodal x-coordinate
    units: meters
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'y': <class 'netCDF4._netCDF4.Variable'>
float64 y(node)
    long_name: nodal y-coordinate
    units: meters
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'lon': <class 'netCDF4._netCDF4.Variable'>
float64 lon(node)
    long_name: nodal longitude
    standard_name: longitude
    units: degrees_east
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'lat': <class 'netCDF4._netCDF4.Variable'>
float64 lat(node)
    long_name: nodal latitude
    standard_name: latitude
    units: degrees_north
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'xc': <class 'netCDF4._netCDF4.Variable'>
float64 xc(nele)
    long_name: zonal x-coordinate
    units: meters
unlimited dimensions:
current shape = (5645,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'yc': <class 'netCDF4._netCDF4.Variable'>
float64 yc(nele)
    long_name: zonal y-coordinate
    units: meters
unlimited dimensions:
current shape = (5645,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'lonc': <class 'netCDF4._netCDF4.Variable'>
float64 lonc(nele)
    long_name: zonal longitude
    standard_name: longitude
    units: degrees_east
unlimited dimensions:
current shape = (5645,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'latc': <class 'netCDF4._netCDF4.Variable'>
float64 latc(nele)
    long_name: zonal latitude
    standard_name: latitude
    units: degrees_north
unlimited dimensions:
current shape = (5645,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'siglay': <class 'netCDF4._netCDF4.Variable'>
float64 siglay(siglay, node)
    long_name: Sigma Layers
    standard_name: ocean_sigma/general_coordinate
    positive: up
    valid_min: -1.0
    valid_max: 0.0
    formula_terms: sigma: siglay eta: zeta depth: h
unlimited dimensions:
current shape = (30, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'siglev': <class 'netCDF4._netCDF4.Variable'>
float64 siglev(siglev, node)
    long_name: Sigma Levels
    standard_name: ocean_sigma/general_coordinate
    positive: up
    valid_min: -1.0
    valid_max: 0.0
    formula_terms: sigma:siglay eta: zeta depth: h
unlimited dimensions:
current shape = (31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'h': <class 'netCDF4._netCDF4.Variable'>
float64 h(node)
    long_name: Bathymetry
    standard_name: sea_floor_depth_below_geoid
    units: m
    positive: down
    grid: Bathymetry_Mesh
    coordinates: x y
    type: data
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'nv': <class 'netCDF4._netCDF4.Variable'>
int32 nv(three, nele)
    long_name: nodes surrounding element
unlimited dimensions:
current shape = (3, 5645)
filling on, default _FillValue of -2147483647 used, 'iint': <class 'netCDF4._netCDF4.Variable'>
int32 iint(time)
    long_name: internal mode iteration number
unlimited dimensions: time
current shape = (2197,)
filling on, default _FillValue of -2147483647 used, 'time': <class 'netCDF4._netCDF4.Variable'>
float64 time(time)
    long_name: time
    units: days since 1858-11-17 00:00:00
    format: defined reference date
    time_zone: UTC
unlimited dimensions: time
current shape = (2197,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'Itime': <class 'netCDF4._netCDF4.Variable'>
int32 Itime(time)
    units: days since 1858-11-17 00:00:00
    format: defined reference date
    time_zone: UTC
unlimited dimensions: time
current shape = (2197,)
filling on, default _FillValue of -2147483647 used, 'Itime2': <class 'netCDF4._netCDF4.Variable'>
int32 Itime2(time)
    units: msec since 00:00:00
    time_zone: UTC
unlimited dimensions: time
current shape = (2197,)
filling on, default _FillValue of -2147483647 used, 'Times': <class 'netCDF4._netCDF4.Variable'>
|S1 Times(time, DateStrLen)
    time_zone: UTC
unlimited dimensions: time
current shape = (2197, 26)
filling on, default _FillValue of  used, 'zeta': <class 'netCDF4._netCDF4.Variable'>
float64 zeta(time, node)
    long_name: Water Surface Elevation
    units: meters
    positive: up
    standard_name: sea_surface_height_above_geoid
    grid: Bathymetry_Mesh
    coordinates: time lat lon
    type: data
    location: node
unlimited dimensions: time
current shape = (2197, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'nbe': <class 'netCDF4._netCDF4.Variable'>
int32 nbe(three, nele)
    long_name: elements surrounding each element
unlimited dimensions:
current shape = (3, 5645)
filling on, default _FillValue of -2147483647 used, 'ntsn': <class 'netCDF4._netCDF4.Variable'>
int32 ntsn(node)
    long_name: #nodes surrounding each node
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of -2147483647 used, 'nbsn': <class 'netCDF4._netCDF4.Variable'>
int32 nbsn(maxnode, node)
    long_name: nodes surrounding each node
unlimited dimensions:
current shape = (11, 3210)
filling on, default _FillValue of -2147483647 used, 'ntve': <class 'netCDF4._netCDF4.Variable'>
int32 ntve(node)
    long_name: #elems surrounding each node
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of -2147483647 used, 'nbve': <class 'netCDF4._netCDF4.Variable'>
int32 nbve(maxelem, node)
    long_name: elems surrounding each node
unlimited dimensions:
current shape = (9, 3210)
filling on, default _FillValue of -2147483647 used, 'a1u': <class 'netCDF4._netCDF4.Variable'>
float64 a1u(four, nele)
    long_name: a1u
unlimited dimensions:
current shape = (4, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'a2u': <class 'netCDF4._netCDF4.Variable'>
float64 a2u(four, nele)
    long_name: a2u
unlimited dimensions:
current shape = (4, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'aw0': <class 'netCDF4._netCDF4.Variable'>
float64 aw0(three, nele)
    long_name: aw0
unlimited dimensions:
current shape = (3, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'awx': <class 'netCDF4._netCDF4.Variable'>
float64 awx(three, nele)
    long_name: awx
unlimited dimensions:
current shape = (3, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'awy': <class 'netCDF4._netCDF4.Variable'>
float64 awy(three, nele)
    long_name: awy
unlimited dimensions:
current shape = (3, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'art2': <class 'netCDF4._netCDF4.Variable'>
float64 art2(node)
    long_name: Area of elements around a node
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'art1': <class 'netCDF4._netCDF4.Variable'>
float64 art1(node)
    long_name: Area of Node-Base Control volume
unlimited dimensions:
current shape = (3210,)
filling on, default _FillValue of 9.969209968386869e+36 used, 'u': <class 'netCDF4._netCDF4.Variable'>
float64 u(time, siglay, nele)
    long_name: Eastward Water Velocity
    standard_name: eastward_sea_water_velocity
    units: meters s-1
    grid: fvcom_grid
    type: data
    coordinates: time siglay latc lonc
    mesh: fvcom_mesh
    location: face
unlimited dimensions: time
current shape = (2197, 30, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'v': <class 'netCDF4._netCDF4.Variable'>
float64 v(time, siglay, nele)
    long_name: Northward Water Velocity
    standard_name: Northward_sea_water_velocity
    units: meters s-1
    grid: fvcom_grid
    type: data
    coordinates: time siglay latc lonc
    mesh: fvcom_mesh
    location: face
unlimited dimensions: time
current shape = (2197, 30, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'tauc': <class 'netCDF4._netCDF4.Variable'>
float64 tauc(time, nele)
    long_name: bed stress magnitude from currents
    note1: this stress is bottom boundary condtion on velocity field
    note2: dimensions are stress/rho
    units: m^2 s^-2
    grid: fvcom_grid
    type: data
    coordinates: time latc lonc
    mesh: fvcom_mesh
    location: face
unlimited dimensions: time
current shape = (2197, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'temp': <class 'netCDF4._netCDF4.Variable'>
float64 temp(time, siglay, node)
    long_name: temperature
    standard_name: sea_water_temperature
    units: degrees_C
    grid: fvcom_grid
    coordinates: time siglay lat lon
    type: data
    mesh: fvcom_mesh
    location: node
unlimited dimensions: time
current shape = (2197, 30, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'salinity': <class 'netCDF4._netCDF4.Variable'>
float64 salinity(time, siglay, node)
    long_name: salinity
    standard_name: sea_water_salinity
    units: 1e-3
    grid: fvcom_grid
    coordinates: time siglay lat lon
    type: data
    mesh: fvcom_mesh
    location: node
unlimited dimensions: time
current shape = (2197, 30, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'viscofm': <class 'netCDF4._netCDF4.Variable'>
float64 viscofm(time, siglay, nele)
    long_name: Horizontal Turbulent Eddy Viscosity For Momentum
    units: m 2 s-1
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 30, 5645)
filling on, default _FillValue of 9.969209968386869e+36 used, 'viscofh': <class 'netCDF4._netCDF4.Variable'>
float64 viscofh(time, siglay, node)
    long_name: Horizontal Turbulent Eddy Viscosity For Scalars
    units: m 2 s-1
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 30, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'km': <class 'netCDF4._netCDF4.Variable'>
float64 km(time, siglev, node)
    long_name: Turbulent Eddy Viscosity For Momentum
    units: m 2 s-1
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'kh': <class 'netCDF4._netCDF4.Variable'>
float64 kh(time, siglev, node)
    long_name: Turbulent Eddy Viscosity For Scalars
    units: m 2 s-1
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'kq': <class 'netCDF4._netCDF4.Variable'>
float64 kq(time, siglev, node)
    long_name: Turbulent Eddy Viscosity For Q2/Q2L
    units: m 2 s-1
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'q2': <class 'netCDF4._netCDF4.Variable'>
float64 q2(time, siglev, node)
    long_name: Turbulent Kinetic Energy
    units: m2 s-2
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'q2l': <class 'netCDF4._netCDF4.Variable'>
float64 q2l(time, siglev, node)
    long_name: Turbulent Kinetic Energy X Turbulent Macroscale
    units: m3 s-2
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'l': <class 'netCDF4._netCDF4.Variable'>
float64 l(time, siglev, node)
    long_name: Turbulent Macroscale
    units: m3 s-2
    grid: fvcom_grid
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 31, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used, 'DYE': <class 'netCDF4._netCDF4.Variable'>
float64 DYE(time, siglay, node)
    long_name: Water Surface Elevation
    units: meters
    positive: up
    standard_name: sea_surface_height_above_geoid
    grid: SigmaLayer_Mesh
    coordinates: x y
    type: data
unlimited dimensions: time
current shape = (2197, 30, 3210)
filling on, default _FillValue of 9.969209968386869e+36 used}


"""