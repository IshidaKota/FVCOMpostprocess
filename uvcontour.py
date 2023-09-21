import os, sys
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PyFVCOM.read import FileReader
from PyFVCOM.plot import Plotter, Time, Depth
import PyFVCOM.grid as grid


plt.rcParams['font.size'] = 12

def main(case):

    # Read NetCDF Result
    rslt = FileReader("../runtvd/fslp01/tvdf01_hp03_0001.nc", variables=["u", "v"])

    # Interpolate Velocity
    time, sigma, element = rslt.data.u.shape 
    nv = rslt.ds.variables['nv'][:]
    triangles = nv.transpose() - 1
    for i in range(element):
    node_u = grid.elems2nodes(rslt.data.u[1000,0,:], triangles)
    node_v = grid.elems2nodes(rslt.data.v[1000,0,:], triangles)
    node_uv = (node_u**2 + node_v**2)**0.5

    # Plotter
    plot = Plotter(rslt)
    plot.plot_quiver(u,v)
    plot.figure.savefig("uv.png")


if __name__ == '__main__':
    main()
