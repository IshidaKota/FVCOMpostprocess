from pyproj import Proj
import netCDF4
import matplotlib.pyplot as plt
nc = netCDF4.Dataset("../runtvd/fslp01/tvdf01_w3_0001.nc",'r')
#for Ugrid component
plt.rcParams['font.family'] = 'VL Gothic'
x =nc.variables['x'][:]
y =nc.variables['y'][:]

e2u_conv=Proj(proj='utm', zone=54, ellps='WGS84')
#Convert UTM2EQA
rslt = [e2u_conv(lon,lat,inverse=True) for lon,lat in zip(x,y)]
x = [rslt[i][0] for i in range(len(rslt))]
y = [rslt[i][1] for i in range(len(rslt))]
triangles = nc.variables['nv'][:].T-1 #-1 for python index
names = ["2020-02-01 12:00:00","2020-04-01 12:00:00","2020-06-01 12:00:00","2020-08-01 12:00:00","2020-10-01 12:00:00","2020-12-01 12:00:00"]
label = [6*30,6*90,6*150,6*210,6*270,6*330]
for name,t in zip(names,label):
    fig,axs = plt.subplots(figsize=(6,10))
    axs.set_aspect('equal')
    axs.set_ylabel('Latitude(deg)')
    axs.set_xlabel('Longitude(deg)')
    axs.set_title(f'<塩分> {name}')

    pcolor = axs.tripcolor(x,y,nc.variables['salinity'][t,28,:],triangles=triangles,vmin=10,vmax=30,cmap='jet')
    fig.colorbar(pcolor,label='Salinity(PSU)',shrink=0.73)
    fig.savefig(f"salinity_t{str(t)}_bottom.png",dpi=300,bbox_inches='tight')