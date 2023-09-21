import pandas as pd
import os,sys
#import numpy as np
from pyproj import Proj
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
plt.rcParams['font.family'] = 'VL Gothic'
import netCDF4
#pyfvcom
#from PyFVCOM.grid import Domain
#from PyFVCOM.read import FileReader
#from PyFVCOM.plot import Time,Plotter



def main():
    #read pd.DataFrame
    df = pd.read_csv('./data/kokyo/kokyo2020.csv')
    df = df.dropna(subset=['塩分量(海域)','水温'])
    df = df.reset_index(drop=True)
    #get rslt

    run = sys.argv[-1]
    if len(sys.argv) == 3:
        paths = [sys.argv[1]]
    else:
        paths = [path for path in sys.argv[1:-2]]

    #plot    
    for path in paths:

        rsltf = f"../{run}/{path}_0001.nc"
        nc = netCDF4.Dataset(rsltf,'r')
      #  fvcom = FileReader(rsltf, variables=['temp', 'salinity'], zone=54)
       # plot(fvcom,df)
        plot_map(nc,df)

#plot function
def plot(fvcom,df):

    variable = ['salinity','temp']
    for var in variable:
        if var == 'salinity':
            datas = fvcom.data.salinity
            attss = fvcom.atts.salinity
            name = '塩分量(海域)'
            min = 15;max=33.5
        else:
            datas = fvcom.data.temp
            attss = fvcom.atts.temp
            name = '水温'
            min=10;max=34



        #make list for plotting place
        pointsy,pointsx = list(set(df['lat'])),list(set(df['lon']))
        n=7
        fig,axs = plt.subplots(6,n,figsize=(30,20))
        fig.suptitle(f"{attss.long_name} Red:Upper Blue:Bottom")
        u = 0;b = 0
        for i in [0,2,4]:

            ax0 = axs[i,:]
            for ax,xo,yo in zip(ax0,pointsx[n*i//2:n*(i//2+1)],pointsy[n*i//2:n*(i//2+1)]): #xo,yo:x_observation,y_observation

                tmp = df[df['lon'] ==xo]
                tmp = tmp.reset_index(drop=True)
                tmp = tmp[[depth < tdepth/2 for depth,tdepth in zip(tmp['採取水深'],tmp['全水深'])]]
                tmp = tmp.reset_index(drop=True)
        
                gauge = (xo, yo)  # a sample (lon, lat) position for Estuary example
                index = fvcom.closest_node(gauge).item()  ### narray.item(): -> scalar
                time = Time(fvcom, axes =ax,title='st.num = {}'.format(str(u)))
                time.plot_line(datas[:,2,index], color='r')
                ax.scatter(tmp['date'],tmp[name],color='black')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'));ax.set_ylim(min,max)
                u+=1

            axs1 = axs[i+1,:]
            for ax,xo,yo in zip(axs1,pointsx[n*i//2:n*(i//2+1)],pointsy[n*i//2:n*(i//2+1)]): #xo,yo:x_observation,y_observation

                tmp = df[df['lon'] ==xo]
                tmp = tmp.reset_index(drop=True)
                tmp = tmp[[depth > tdepth/2 for depth,tdepth in zip(tmp['採取水深'],tmp['全水深'])]]
                tmp = tmp.reset_index(drop=True)
        
                gauge = (xo, yo)  # a sample (lon, lat) position for Estuary example
                index = fvcom.closest_node(gauge).item()  ### narray.item(): -> scalar
                time = Time(fvcom, axes =ax,title='st.num = {}'.format(str(b)))
                time.plot_line(datas[:,28 ,index], color='blue')
                ax.scatter(tmp['date'],tmp[name],color='black')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'));ax.set_ylim(min,max)
                b+=1

        plt.tight_layout()
        fig.savefig(f'{var}_test.png')
        plt.close()

def plot_map(nc,df):
   # xs = [];ys=[]
   # for i in range(len(df['lon'])):
   #     if df['lon'][i] not in xs:
   #         xs.append(df['lon'][i])
   #         ys.append(df['lat'][i])
   # print(xs,ys)
   # num = [i for i in range(len(xs))]
    #for Ugrid component
    x =nc.variables['x'][:]
    y =nc.variables['y'][:]

    e2u_conv=Proj(proj='utm', zone=54, ellps='WGS84')
    #Convert UTM2EQA
    rslt = [e2u_conv(lon,lat,inverse=True) for lon,lat in zip(x,y)]
    x = [rslt[i][0] for i in range(len(rslt))]
    y = [rslt[i][1] for i in range(len(rslt))]
    triangles = nc.variables['nv'][:].T-1 #-1 for python index


    fig,axs = plt.subplots(figsize=(4,5))
    axs.set_aspect('equal')
    axs.set_ylabel('Latitude(degC)')
    axs.set_xlabel('Longitude(degC)')
    axs.set_title('DINの観測点')
    #plt.rcParams['font.family'] = 'VL Gothic'
    nums = ["stn51","stn43","stn8"]
    ys = [35.62,35.565,35.423]
    xs = [140.005,139.85,139.86]
    for xss,yss,num in zip(xs,ys,nums):
        axs.scatter(xss,yss,label=num)
        axs.text(xss,yss,num)
    axs.triplot(x,y,triangles,lw=0.1,color='black')
    #axs.legend(loc="best",ncols=3)
    fig.savefig('map_moniteringpost.png',bbox_inches="tight",dpi=600)
       



if __name__ == '__main__':
    main()