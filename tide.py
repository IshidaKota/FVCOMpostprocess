import pandas as pd
import netCDF4
import matplotlib.pyplot as plt
import datetime
from jdcal import gcal2jd, jd2gcal ,MJD_0
from matplotlib import dates as mdates
#import numpy as np
from pyproj import Proj

#read 
def read_nc(ncfile_path="../runtvd/fslp01/tvdf01_w3"+"_0001.nc"):
    nc = netCDF4.Dataset(ncfile_path, 'r')
    return nc



def find_nearest_node(lon,lat,ncfile_path="../runtvd/fslp01/tvdf01_w3"+"_0001.nc"):#,x_node= None,y_node = None):

    """
    return: index of the nearest node from the station.
    lon:経度,lat:緯度
    """

    #covert example from https://qiita.com/spicy_HotChicken/items/4cdf303493d73e24dc14
    #<-------------
    ##Define EQA2UTM converter
    #e2u_conv=Proj(proj='utm', zone=e2u_zone, ellps='WGS84')
    ##Apply the converter
    #utmx, utmy=e2u_conv(lon, lat)
    #>-------------

    conv=Proj(proj='utm', zone=54, ellps='WGS84')
    x_station,y_station =conv(lon,lat)
    nc = read_nc(ncfile_path=ncfile_path)
    x_node,y_node = nc.variables['x'][:],nc.variables['y'][:]

    distances_to_station = [(x-x_station)**2 + (y-y_station)**2 for x,y in zip(x_node,y_node)]
    min_dist = min(distances_to_station)
    node = distances_to_station.index(min_dist) 

    return node

# read csv of observed data
def read_observed_data(csvfile_path='./data/Chibakencho2020.csv'):

    df = pd.read_csv(csvfile_path) #実測潮位

    date = pd.to_datetime(df['date'])
    elevation = df['elev']

    return date,elevation

#plot
def plot_tide(start="2020-1-1",stop="2020-12-31",lat=35.56667,lon=140.05,ncfile_path="../runtvd/fslp01/tvdf01_w3_0001.nc",png_save_path='./png/zeta/test.png',title="Elevation @ Chiba Kencho",date_formatter="%m"):

    #prepare dataset
    nc = read_nc(ncfile_path=ncfile_path) #retrun netCDF4.Dataset

    index = find_nearest_node(lon,lat) #return index (int)

    simulated_date =  [jd2gcal(MJD_0,time) for time in nc.variables['Itime']] #ymd
    simulated_datetime = [datetime.datetime(Itime[0],Itime[1],Itime[2],hour=int(Itime2/3600000)) for Itime,Itime2 in zip(simulated_date,nc.variables['Itime2'])] #ymd+h
    simulated_elevation = nc.variables['zeta'][:,index] 


    observed_date,observed_elevation = read_observed_data()

    #plot 
    fig,ax = plt.subplots()
    
    ax.plot(observed_date,observed_elevation,label='observation')
    ax.plot(simulated_datetime,simulated_elevation,label='simulation')
    
    #specify starttime and endtime
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    stop_date = datetime.datetime.strptime(stop, '%Y-%m-%d')

    ax.set_xlim(start_date,stop_date)
    ax.legend()

    #set label,title
    ax.set_xlabel("Start={},Stop={}".format(start,stop))
    ax.set_ylabel('Elevation(m)')
    ax.set_title(title)

    formatter = mdates.DateFormatter(date_formatter)
    ax.xaxis.set_major_formatter(formatter)

    #save figure
    fig.savefig(png_save_path,bbox_inches='tight',dpi=600)




if __name__ == '__main__':

    """
    start         : start date of plot (%Y-%m-%d)
    stop          : stop date of plot (%Y-%m-%d)
    lat,lon       : station point
    ncfile_path   : path to the simulation netCDF file
    png_save_path : path to the png save place
    title         : title of plot
    date_formatter: x label date formatter
    """

    plot_tide(start="2020-1-1",stop="2020-12-31",lat=35.566667,lon=140.05,ncfile_path="../runtvd/fslp01/tvdf01_w3_0001.nc",png_save_path='./png/zeta/test.png',title="Elevation @ Chiba Kencho",date_formatter="%m")




"""
def main():
# plot observation
# df = pd.read_csv('./data/tide_2020_Tokyo_obs.csv')
df = pd.read_csv('./data/Chibakencho2020.csv') #実測潮位
date = pd.to_datetime(df['date'])
tide_obs = df['elev']
#paths = ['tvdf01_t4','tvdf01_t8','tvdf01_t5','tvdf01_t6','tvdf01_t7']
#ways = ['minus10cm','minus10cm&SSH=0cm','minus12cm','minus15cm','minus18cm']
paths = ['fslp01/tvdf01_air','slp01/tvd01','slp01/tvd01_w15','slp01/tvd01_w20']
ways = ['AirPress on ','wind1.0','wind1.5','wind2.0']
fig,axs = plt.subplots(2,len(paths),figsize=(30,14))
axs0 = axs[0,:]
for ax,path,way in zip(axs0,paths,ways):
    # plot simulation
    index = 634
    nc = netCDF4.Dataset(f'../runtvd/{path}_0001.nc','r')

    zeta = nc.variables['zeta'][:,index]

    dates_float = [jd2gcal(MJD_0,nc.variables['Itime'][i]) for i in range(len(nc.variables['Itime']))] #ymd
    dates_sim = [datetime.datetime(dates_float[i][0],dates_float[i][1],dates_float[i][2],\
        hour=int(nc.variables['Itime2'][i]/3600000)) for i in range(len(nc.variables['Itime']))] #ymd+h

    #plot


    ax.plot(dates_sim[1:],zeta[1:],label= way,alpha=0.5)
    ax.plot(date[1:],tide_obs[1:], label = 'observation',alpha=0.3)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    ax.set_xlabel('Elevation(m)')
    ax.set_title(f"<{way}>")
    ax.legend();ax.grid()


axs1 = axs[1,:]
for ax,path,way in zip(axs1,paths,ways):
    # plot simulation

    #nc = netCDF4.Dataset(f'../runtvd/{path}_0001.nc','r')

    # zeta = nc.variables['zeta'][:,index]

    dates_float = [jd2gcal(MJD_0,nc.variables['Itime'][i]) for i in range(len(nc.variables['Itime']))] #ymd
    dates_sim = [datetime.datetime(dates_float[i][0],dates_float[i][1],dates_float[i][2],\
        hour=int(nc.variables['Itime2'][i]/3600000)) for i in range(len(nc.variables['Itime']))] #ymd+h
    start = 1000;stop=1100
    diff = np.zeros(stop-start)
    for i in range(start,stop):
        diff[i] = zeta[i]-tide_obs[i]

    ax.plot(dates_sim[start:stop],diff,label= way,alpha=0.5)


    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    ax.set_xlabel('Diff of Elevation(m)')
    ax.set_title(f"Difference of elev < {way} >")
    ax.legend();ax.grid()
plt.tight_layout()
fig.savefig(f'tide_all.png')   
"""