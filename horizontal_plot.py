from pyproj import Proj
nc = netCDF4.Dataset("./exp31/exp0_0001.nc",'r')
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
axs.set_ylabel('Latitude(deg)')
axs.set_xlabel('Longitude(deg)')
axs.set_title('(a)<風力:観測値>定常状態での表層のDIN濃度分布')

pcolor = axs.tripcolor(x,y,nc.variables['DYE'][40,0,:],triangles=triangles,vmin=0,vmax=200,cmap='jet')
fig.colorbar(pcolor,label='DIN濃度(μM)',shrink=0.73)
fig.savefig("./thesis/DIN_t40_upper_wvar.png",dpi=300,bbox_inches='tight')