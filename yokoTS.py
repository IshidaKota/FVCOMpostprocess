import pandas as pd
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import netCDF4
#pyfvcom


def main():
    #get rslt
    run = sys.argv[-1]
    if len(sys.argv) == 3:
        paths = [sys.argv[1]]
    else:
        paths = [path for path in sys.argv[1:-2]]
    for path in paths:

        rsltf = f"../{run}/{path}_0001.nc"
        nc = netCDF4.Dataset(rsltf,'r')
        plot(nc)

def plot(nc):

    x ,y = nc.variables['x'][:]/1000,nc.variables['y'][:]/1000
    siglay,h = nc.variables['siglay'][:,0],nc.variables['h'][:]
    temp,salinity = nc.variables['temp'][:,:,:],nc.variables['salinity'][:,:,:]

    df = pd.read_csv(f"data/yoko/yokogicho_ts_2020_TokyoBay.csv",encoding='shift-jis')
    df = df[df['測点'] != 'b']
    jan_df = df[df['月'] == 1]
    ID,obs_x, obs_y =list(set(jan_df['測点'])), list(set(jan_df['x(km)'])),list(set(jan_df['y(km)']))

    fig,axs = plt.subplots(3,len(ID),figsize=(6,18))
    print(x[0],y[0])

    for i,id in enumerate(ID):

        dist = [((xx-obs_x[i])**2 + (yy-obs_y[i])**2)**0.5 for xx,yy in zip(x,y)]
        min_dist = min(dist)
        ind = dist.index(min_dist)
        depth = h[ind]

        slice_df = df[df['測点'] == id]
        #res = max(slice_df['水深'])/depth
        print(ind,depth,id,max(slice_df['水深']))

        #axs[i].plot(temp[:,ind,1])

    


if __name__ == '__main__':
    main()