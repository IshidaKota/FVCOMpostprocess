#dev_fvcom_2d_ds.ipynbのデータを元に作成することを想定。鉛直コンターはpyfvcomを用いる。
#pyfvcom
from PyFVCOM.plot import Depth
#from PyFVCOM.grid import unstructured_grid_depths
from PyFVCOM.read import FileReader
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation
#dev_fvcom_2d_ds
#import mod_fvcom
#other
#import pandas as pd
#from holoviews import opts
#import holoviews as hv
import matplotlib.pyplot as plt
import numpy as np
import sys
from pyproj import Proj
import pandas as pd
#import math
#import os
import netCDF4

#plt.rcParams()
###############################################
def main(variable):
    anim =True;plot=False
    start,stop,slice = 0,24*30*12,12
    #times = [i for i in range(start,stop,slice)]
    print('start making vertical contour...')
    f = f"../runtvd/fslp01/tvdf01_ncep_0001.nc"
    fvcom_pyfvcom = FileReader(f, variables=['salinity','temp'])#,dims={'time': times})

    ##### Start set parameters
    ratio = 24
    timestep = [30*ratio,90*ratio,150*ratio,210*ratio,240*ratio,270*ratio]

    lon_lat1, lon_lat2 = (140.0105, 35.6261), (139.6956, 35.3261) 
    positions = np.array((lon_lat1, lon_lat2)) 
    indices, distances = fvcom_pyfvcom.horizontal_transect_nodes(positions)
    print(f"start={indices[0]}, end={indices[-1]}")
    #補正
    p = Proj(proj='utm',zone=54,ellps='WGS84', preserve_units=False)
    x1,y1 =p(lon_lat1[0],lon_lat1[1])[0],p(lon_lat1[0],lon_lat1[1])[1]
    x2,y2 =p(lon_lat2[0],lon_lat2[1])[0],p(lon_lat2[0],lon_lat2[1])[1]
    true_dist =((x1-x2)**2 + ((y1-y2)**2)) **0.5
    for i in range(len(distances)):
        distances[i] = true_dist*distances[i]/distances[-1]

    lon_lat1, lon_lat2 =(139.6956, 35.3261)   , (139.7936, 35.2521) ## Estuary example
    x1,y1 =p(lon_lat1[0],lon_lat1[1])[0],p(lon_lat1[0],lon_lat1[1])[1]
    x2,y2 =p(lon_lat2[0],lon_lat2[1])[0],p(lon_lat2[0],lon_lat2[1])[1]
    true_dist1 =((x1-x2)**2 + ((y1-y2)**2)) **0.5
    positions = np.array((lon_lat1, lon_lat2)) 
    indices1, distances1 = fvcom_pyfvcom.horizontal_transect_nodes(positions)
    print(f"start1={indices1[0]}, end1={indices1[-1]}")
    for i in range(len(distances1)):
        distances1[i] = (true_dist1*distances1[i]/distances1[-1]) +true_dist
    
    lon_lat1, lon_lat2 =(139.7936, 35.2521) , (139.7069, 35.0455) 
    x1,y1 =p(lon_lat1[0],lon_lat1[1])[0],p(lon_lat1[0],lon_lat1[1])[1]
    x2,y2 =p(lon_lat2[0],lon_lat2[1])[0],p(lon_lat2[0],lon_lat2[1])[1]
    true_dist2 =((x1-x2)**2 + ((y1-y2)**2)) **0.5
    positions = np.array((lon_lat1, lon_lat2)) 
    indices2, distances2 = fvcom_pyfvcom.horizontal_transect_nodes(positions)
    for i in range(len(distances2)):
        distances2[i] = true_dist2*distances2[i]/distances2[-1] +true_dist1+true_dist
    print(f"start2={indices2[0]}, end2={indices2[-1]}")

    
    #print(distances,distances1,distances2)
    indices.extend(indices1);indices.extend(indices2)
    distances_all = np.r_[distances, distances1,distances2]
    #print(distances_all)
    if plot:
        for i,t in enumerate(timestep):
        
            if variable == 'temperature':
                c = fvcom_pyfvcom.data.temp[t, :, indices]
                ## colorbar label
                var = 'Temperature' ; unit = 'degC'  ## Manually
            elif variable == 'salinity':
                c = fvcom_pyfvcom.data.salinity[t, :, indices]
                ## colorbar label
                var = 'salinity' ; unit = 'PSU'  ## Manually
            figsize=(20,9);cmap = 'jet'
            #cmap=cm.balance
            ##### End set parameters

            cb_label = ("{} ({})").format(var, unit)
            png ='./png/vertical/'+var + 'profile.png'
            x = distances_all / 1000  # to km from m
            y = fvcom_pyfvcom.grid.siglay_z[:, indices]
        # print(len(x),np.size(y),np.size(c))
            plot = Depth(fvcom_pyfvcom, figsize=figsize, cb_label=cb_label, cmap=cmap)
            ## fill_seabed makes the part of the plot below the seabed gray.
            if variable == 'salinity':
                plot.plot_slice(x, y, c, fill_seabed=True, shading='gouraud',norm=Normalize(vmin=25,vmax=35))
            else:
                plot.plot_slice(x, y, c, fill_seabed=True, shading='gouraud')
            #plot.plot_slice(x, y, c, fill_seabed=True, edgecolors='white')
            plot.axes.set_xlim(right=x.max())  # set the x-axis to the data range
            plot.axes.set_xlabel('Distance (km)')
            plot.axes.set_ylabel('Depth (m)')
            ## Save the figure.
            plot.figure.savefig(png, dpi=300, bbox_inches='tight')
            #print(f"saved figure,{png}")
            #plt.close()

    if anim:
        
        if variable == 'temperature':
            c = fvcom_pyfvcom.data.temp[:, :, indices]
            ## colorbar label
            var = 'Temperature' ; unit = 'degC'  ## Manually
        elif variable == 'salinity':
            c = fvcom_pyfvcom.data.salinity[:, :, indices]
            ## colorbar label
            var = 'salinity' ; unit = 'PSU'  ## Manually

        figsize=(20,9);cmap = 'jet'
        cb_label = ("{} ({})").format(var, unit)
        fig,ax = plt.subplots()
        plot = Depth(fvcom_pyfvcom, axes=ax,figsize=figsize, cb_label=cb_label, cmap=cmap)
     
        x = distances_all / 1000  # to km from m
        y = fvcom_pyfvcom.grid.siglay_z[:, indices]
        plot.plot_slice(x, y, c[0,:], axes=ax,fill_seabed=True, shading='gouraud',norm=Normalize(vmin=10,vmax=20))

        date_ary =pd.date_range("2020-01-01 00:00:00", periods=366*24+1, freq="H")[start:stop+24] 

        #count = len(c[:,0])
       # count = len(c[:,0])/slice
        count = 10
        def update(frame):
            ax.cla()
            #plot.plot_slice(x, y, c[frame,:], fill_seabed=True, axes=ax,shading='gouraud',norm=Normalize(vmin=10,vmax=20))
            plot.plot_slice(x, y, c[frame*slice,:], fill_seabed=True, axes=ax,shading='gouraud',norm=Normalize(vmin=10,vmax=20))
            ax.set_title(date_ary[frame*slice])
        savename = 'test'
        #fig.suptitle('水温鉛直コンター')
        anim = FuncAnimation(fig, update,save_count=count-1,interval=200)
        plt.tight_layout()
        anim.save(f'./png/{savename}_temp.gif',writer="ffmpeg",dpi=200)

def plot_map(nc):
    #for Ugrid component
    x =nc.variables['x'][:]
    y =nc.variables['y'][:]

    e2u_conv=Proj(proj='utm', zone=54, ellps='WGS84')
    #Convert UTM2EQA
    rslt = [e2u_conv(lon,lat,inverse=True) for lon,lat in zip(x,y)]
    x = [rslt[i][0] for i in range(len(rslt))]
    y = [rslt[i][1] for i in range(len(rslt))]
    triangles = nc.variables['nv'][:].T-1 #-1 for python index


    fig,axs = plt.subplots(figsize=(6,10))
    axs.set_aspect('equal')
    axs.set_ylabel('Latitude(degC)')
    axs.set_xlabel('Longitude(degC)')
    axs.set_title('Mesh and Lines for Vertical Contour')
    #plt.rcParams['font.family'] = 'VL Gothic'

    axs.plot([140.0105,139.6956 ],[35.6261, 35.3261],c='blue')
    axs.plot([139.6956, 139.7936]   , [35.3261, 35.2521],c='blue')
    axs.plot([139.7936, 139.7069] , [35.2521, 35.0455],c='blue')
    axs.triplot(x,y,triangles,lw=0.1,color='black')
    axs.legend(loc="best",ncols=3)
    fig.savefig('map_vc.png')
       


if __name__ == '__main__':
    nc = netCDF4.Dataset('../runtvd/fslp01/tvdf01_ncep_0001.nc','r')
    main('salinity')
    #main('temperature')
    plot_map(nc)
