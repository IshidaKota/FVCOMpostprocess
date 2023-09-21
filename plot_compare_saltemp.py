##initialized by ishid 2023/03/11 
##revised by ishid 2023/03/14


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib import dates as mdates
import netCDF4
from pyproj import Proj
from jdcal import jd2gcal ,MJD_0
import datetime

#read 
def read_nc(ncfile_path="../runtvd/fslp01/tvdf01_w3"+"_0001.nc"):
   # ncfile_path = "../runtvd/tvdf01/tvdf01_w3"+"_0001.nc"#relative_path
    nc = netCDF4.Dataset(ncfile_path, 'r')
  #  print(nc.variables.keys()) #option
    return nc



#find nearest node of Kemigawa
def find_nearest_node(lat,lon):
    """
    find the nearest point of station. since Proj4 is not activated, convert lat_lon(WGS84) to UTM.
    """
    #This function does not work currently (Proj)
    #lat,lon = ()(140.0233033,35.61095833)
    #conv = Proj(proj='utm',zone=54,ellps='WGS84', preserve_units=False) #since proj4 is not activated ,convert latlon to UTM54.
    #x_kemi,y_kemi =conv(lon,lat)[0],conv(lon,lat)[1] #kemi=kemigawa
    #print(x_kemi,y_kemi)
    x_kemi, y_kemi = 411540.94,3941238.486
    nc = read_nc() #read mesh imformation
    x_node,y_node = nc.variables['x'],nc.variables['y'] #node (x,y) list
    distances_to_kemi = [(x-x_kemi)**2 + (y-y_kemi)**2 for x,y in zip(x_node,y_node)] #calc distances from specific point
    print(distances_to_kemi[:10])
    min_dist = min(distances_to_kemi) # find minimum distances
    print(min_dist)
    node = distances_to_kemi.index(min_dist) #finally we find the node nearest kemigawa
    print(node)
    return node

# read csv of observed data
def read_observe_data(variable,siglay):
    if variable =="temp":
        var = "temperature"
    else :
        var = "salinity"
   # print(var)
    df  = pd.read_csv('./data/interp/chibaharo_'+var+'ext_2020.csv')
    date = pd.to_datetime(df.columns[1:])
    data = df.iloc[siglay,1:]
    return date,data
    

#plot
def plot_vertically(variable,siglay,lat=140.0233033,lon=35.61095833,calc_label=None):
    fig,ax = plt.subplots()

    nc = read_nc() #specify your nc result file name as ncfile_path=""
    node = find_nearest_node(lat,lon)
    calc_var = nc.variables[variable][:,siglay,node]

    calc_date = [jd2gcal(MJD_0,time) for time in nc.variables['Itime']] #ymd
    calc_datetime = [datetime.datetime(calc_date[i][0],calc_date[i][1],calc_date[i][2],\
            hour=int(nc.variables['Itime2'][i]/3600000)) for i in range(len(nc.variables['Itime']))] #ymd+h

    ax.plot(calc_datetime,calc_var,label="calculation")

    obs_datetime,obs_var = read_observe_data(variable,siglay)

    increase = 20
    ax.plot(obs_datetime,obs_var+increase,label="observation")
   # ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    ax.tick_params(labelleft=False)
    ax.legend()

    #p = np.linspace(0, max(max(calc_var),max(obs_var)), 100)
    #q = p*0+ increase
    #ax.plot(p,q,c="black",lw=0.1)

    #save
    png = "result"+variable+str(siglay)+".png"
    fig.savefig(png,dpi=600,bbox_inches='tight')
    return None


def calc_corr(x,y):
    """
    x,y: list or array_like 
    """

    x,y = pd.Series(x),pd.Series(y)
    if len(x)!=len(y):
        raise ValueError("length of x does not match to y!")
    else:
        corr = x.corr(y)
    return corr

def plot_xy(variable,siglay,lat=140.0233033,lon=35.61095833,min_value_plot=0,ticks=[]):

    fig,ax = plt.subplots(figsize=(6,6))
    ax.set_aspect("equal")


    nc = read_nc() #specify your nc result file name as ncfile_path="ncfile path"
    node = find_nearest_node(lat,lon)
    calc_var = nc.variables[variable][:,siglay,node]

    calc_date = [jd2gcal(MJD_0,time) for time in nc.variables['Itime']] #ymd
    calc_datetime = [datetime.datetime(calc_date[i][0],calc_date[i][1],calc_date[i][2],\
            hour=int(nc.variables['Itime2'][i]/3600000)) for i in range(len(nc.variables['Itime']))] #ymd+h
    
    obs_datetime,obs_var = read_observe_data(variable,siglay)
    obs_datetime = list(obs_datetime)


    #find where
    o_plot = []
    for i,c_datetime in enumerate(calc_datetime):
        if c_datetime in obs_datetime:
            j = obs_datetime.index(c_datetime)
            o_plot.append(obs_var[j])
   # print(len(o_plot),len(calc_var))

    max_val = max(max(calc_var),max(obs_var))


    #plot
    ax.scatter(o_plot,calc_var[:len(o_plot)],s=0.3)

    #calc corr and write text
    #corr = calc_corr(o_plot,calc_var[:len(o_plot)])
 
    #ax.text(max_val-5,min_value_plot+5,"{:.3f}".format(corr))

    #plot x = y
    p = np.linspace(min_value_plot, max_val, 100)
    q = p
    ax.plot(p,q,c="black",lw=1)

    ax.set_ylim(min_value_plot, max_val)
    ax.set_xlim(min_value_plot, max_val)
    #labels
    #ax.set_xlabel(variable + "-Observation")
    #ax.set_ylabel(variable + "-Calculation")
    #ax.legend()
    plt.xticks(ticks)
    plt.yticks(ticks)
    #save
    save_path = "result_scatter_"+variable+str(siglay)+".png"
    fig.savefig(save_path,dpi=600,bbox_inches='tight')

        

def plot_irochi():
    df = pd.read_csv("./data/kaigan/kisarazu_irochi.csv")
    fig,ax = plt.subplots(figsize=(8,4))

    ax.bar(df['year'],df['number'])
  #  plt.xticks(df['year'],df['year'][::5])
    plt.yticks([0,3000000,6000000,9000000],[0,300,600,900])
    fig.savefig('./png/kaigan/irochi.png',dpi=600)
if __name__ == "__main__":
    plt.rcParams['font.size'] = 18
   # plot_vertically("temp",2)
   # plot_vertically("temp",28)
   # plot_vertically("salinity",2)
   # plot_vertically("salinity",28)

    plot_xy("temp",2,min_value_plot=10,ticks=[10,15,20,25,30])
    plot_xy("temp",28,min_value_plot=10,ticks=[10,15,20,25,30])
    plot_xy("salinity",2,min_value_plot=15,ticks=[15,20,25,30])
    plot_xy("salinity",28,min_value_plot=20,ticks=[20,25,30])
 #   plot_irochi()