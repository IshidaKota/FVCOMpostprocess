#import os, sys
import numpy as np
#import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PyFVCOM.read import FileReader
from PyFVCOM.plot import Plotter, Time, Depth
import PyFVCOM.grid as grid


plt.rcParams['font.size'] = 12


def main():
    print("!!enter the path(s) after '../runbulk/' without '_0001.nc'!!")
    fnames = [x for x in input().split()]
    for fname in fnames:
        # Read NetCDF Result
        rslt = FileReader(f"../runbulk/{fname}_0001.nc", variables=["u", "v"])

        '''
        # Interpolate Velocity
        # rslt.data.u.shape -> (time, sigma, element)
        nv = rslt.ds.variables['nv'][:]
        triangles = nv.transpose() - 1
        node_u = grid.elems2nodes(rslt.data.u[-1,0,:], triangles)
        node_v = grid.elems2nodes(rslt.data.v[-1,0,:], triangles)
        node_uv = (node_u**2 + node_v**2)**0.5
        '''

        # Interpolate Velocity for Vertical Profile
        nv = rslt.ds.variables['nv'][:]
        triangles = nv.transpose() - 1
        node_uv_vert = []
        dum1, nz, dum2 = rslt.data.u.shape
        time = 210
        if time > dum2:
            IndexError('invalid range')
        for k in range(nz):
            node_u = grid.elems2nodes(rslt.data.u[time,k,:], triangles)
            node_v = grid.elems2nodes(rslt.data.v[time,k,:], triangles)
            node_uv = (node_u**2 + node_v**2)**0.5
            node_uv_vert.append(node_uv)
        node_uv_vert = np.array(node_uv_vert)  #(sigma, node)
        #print(rslt.data.temp.shape)
        #print(node_uv_vert.shape)

        '''
        # Plot X-Y Plain
        plot = Plotter(rslt)
        plot.plot_field(node_uv)
        plot.figure.savefig("img/uv.png")
        '''

        # Plot Vertical Profile
        timestep = 50
        # lon_lat1, lon_lat2 = (138, 33), (139, 33)     ## Miwa's mesh
        lon_lat1, lon_lat2 = (139.6837, 35.14668), (139.819068, 35.102073) ## Estuary example
        positions = np.array((lon_lat1, lon_lat2))
        indices, distances = rslt.horizontal_transect_nodes(positions)
        #c = rslt.data.temp[timestep, :, indices]
        c = node_uv_vert[:, indices]
        ## colorbar label
        #var = 'Temperature' ; unit = 'degC'  ## Manually
        var = 'VelocityNorm' ; unit = 'm/s'  ## Manually
        # var = 'temp' ; unit = fvcom.ds.variables[var].units  ## Automatically
        figsize=(20,9)
        cmap=cm.jet
        ##### End set parameters

        cb_label = ("{} ({})").format(var, unit)
        fname = fname.replace('/','')
        png = './png/uv/'+fname + str(time) + '_profile.png'
        x = distances / 1000  # to km from m
        y = rslt.grid.siglay_z[:, indices]

        plot = Depth(rslt, figsize=figsize, cb_label=cb_label, cmap=cmap)
        ## fill_seabed makes the part of the plot below the seabed gray.
        plot.plot_slice(x, y, c, fill_seabed=True, shading='gouraud')
        plot.axes.set_xlim(right=x.max())  # set the x-axis to the data range
        plot.axes.set_xlabel('Distance (km)')
        plot.axes.set_ylabel('Depth (m)')
        plot.axes.set_title(f"Velocity vertical profile < tstep={time} >")
        ## Save the figure.
        plot.figure.savefig(png, dpi=600, bbox_inches='tight')


if __name__ == '__main__':
    main()
