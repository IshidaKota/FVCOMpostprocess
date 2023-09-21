import matplotlib.pyplot as plt
import netCDF4
from matplotlib.animation import FuncAnimation
#import matplotlib
import pandas as pd
#import numpy as np
import sys

#plotの間隔
tstep=6 #
start,stop = 0,30
windon = False

#ncfileの読み込み
path =sys.argv[1] #"../runtvd/fslp01/tvdf01_w3"
#savename = "final"
nc = netCDF4.Dataset(f'{path}_0001.nc','r')
print(nc.variables.keys())



#for Ugrid component
x =nc.variables['x'][:]/1000 #m to km 
y =nc.variables['y'][:]/1000
triangles = nc.variables['nv'][:].T-1 #-1 for python index




item = nc.variables['temp'][::tstep,0,:]


#日付のラベル用　手動で合わせる
date_ary =pd.date_range("2020-01-01 00:00:00", periods=366*24+1, freq="H")

#cmapの上限，下限
vmin = 10
vmax= 30

#描画長さ
count= 10
if windon:
        #nc_avefileの読み込み
    nc_ave = netCDF4.Dataset(f'../runtvd/input/input_0121_slp01/TokyoBay_wnd18.nc','r')
    print(nc_ave.variables.keys())
    print(len(nc_ave.variables['uwind_speed'][:,100]))
    u_wind = nc_ave.variables['uwind_speed'][start:stop,100]
    v_wind = nc_ave.variables['vwind_speed'][start:stop,100]  

    fig,axs = plt.subplots(1,2,figsize=(8,6))
    axs[0].set_aspect('equal')
    axs[0].set_ylabel('Y(km)')
    axs[0].set_xlabel('X(km)')
    plt.rcParams['font.family'] = 'VL Gothic'

    #initialize
    pcolor = axs[0].tripcolor(x,y,item[0,:],triangles=triangles,vmin=vmin,vmax=vmax,cmap='jet')
    fig.colorbar(pcolor,label='Temperature(degC)')

    #update function
    def update(frame):
        axs[1].cla()
        axs[1].quiver(u_wind[frame*tstep//24],v_wind[frame*tstep//24],scale=20)
        axs[0].set_title(date_ary[frame*tstep]) #4:ncファイルの出力間隔が四時間
        axs[0].tripcolor(x,y,item[frame,:],triangles=triangles,cmap='jet',vmin=vmin,vmax=vmax)
        
    axs[1].tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    fig.suptitle('表層水温');axs[1].set_title('Wind_speed');axs[1].legend()
    anim = FuncAnimation(fig, update,save_count=count-1,interval=200)
    plt.tight_layout()
    anim.save(f'./png/upper_{savename}_temp.gif',writer="ffmpeg",dpi=200)

else:
    fig,axs = plt.subplots(figsize=(8,6))
    axs.set_aspect('equal')
    axs.set_ylabel('Y(km)')
    axs.set_xlabel('X(km)')
    plt.rcParams['font.family'] = 'VL Gothic'
    plt.rcParams['font.size'] = '16'

    #initialize
    pcolor = axs.tripcolor(x,y,item[0,:],triangles=triangles,vmin=vmin,vmax=vmax,cmap='jet')
    fig.colorbar(pcolor,label='Temperature')

    #update function
    def update(frame):
        
        axs.set_title(f"{date_ary[frame*tstep*4]}") 
       # axs.set_title(f"Salinity (PSU) (day={frame})")
        axs.tripcolor(x,y,item[frame,:],triangles=triangles,cmap='jet',vmin=vmin,vmax=vmax)
        
    
    #fig.suptitle(sys.argv[2])
    anim = FuncAnimation(fig, update,save_count=count-1,interval=100)
    plt.tight_layout()
    anim.save(f'./png/temp_upper.gif',writer="ffmpeg",dpi=300)
