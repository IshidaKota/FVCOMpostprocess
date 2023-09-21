from pyproj import Proj
import netCDF4
import matplotlib.pyplot as plt
from module.ncVariablesConverter import convertCoordsToLonlat,convertJulianToDate
from datetime import timedelta as tdelta
from datetime import datetime
#revised by Kota Ishida 2023/9/11

#拡張性のメモ
#陸地を塗りつぶす　cartopy



def horizontal_contour(nc,variable,layer=28,plotDate="2020-03-01 12:00:00",simStartDate="2020-01-01 0:00:00",outputInterval=1,vmin=10,vmax=35,dpi=300):
    """
    nc: netCDF file(include path)
    variable(str): the variable you want to plot. e.g.)"salinity"
    simStartDate:start date of simulation e.g.)yyyy-mm-dd hh:mm:ss
    plotDate: specify time you want to plot. make sure the time is included in your simulation! e.g.)yyyy-mm-dd hh:mm:ss
    outputInteval:(hours) specify your nc output time interval. unit is hour.
    vmin: min val of variable you plot
    vmax: max val of variable you plot
    layer: sigma layer number you plot
    """

    #prepare coordinates. Since unstructured grid model uses, we need triagle data.
    lon,lat = convertCoordsToLonlat(nc)
    triangles = nc.variables['nv'][:].T-1 #-1 for python index

    #convert UTC time to time index of netCDF output
    simStartDate = datetime.strptime(simStartDate,"%Y-%m-%d %H:%M:%S")
    plotDate = datetime.strptime(plotDate,"%Y-%m-%d %H:%M:%S")
    plotDate_inSimulation = (plotDate-simStartDate).total_seconds()/60/60
    timeIndex = int(plotDate_inSimulation/outputInterval)

    #draw figure
    fig,ax = plt.subplots(figsize=(6,10))
    ax.set_aspect('equal')
    ax.set_ylabel('Latitude(deg)')
    ax.set_xlabel('Longitude(deg)')
    ax.set_title(f'Bottom Salinity\n {plotDate}')

    pcolor = ax.tripcolor(lon,lat,nc.variables[variable][timeIndex,layer,:],triangles=triangles,vmin=vmin,vmax=vmax,cmap='jet')
    fig.colorbar(pcolor,label=variable,shrink=0.73)

    #save figure
    fig.savefig(f"Horizontal{variable}_{plotDate}_{layer}.png",dpi=dpi,bbox_inches='tight')

def main():
    ncfilePath = "../runtvd/fslp01/tvdf01_w3_0001.nc"
    nc = netCDF4.Dataset(ncfilePath,'r')
    horizontal_contour(nc,"salinity")


if __name__ == "__main__":
    main()