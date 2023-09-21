import netCDF4
import pandas as pd


paths = ['tvdf01_t'+str(i) for i in range(1,8)]
df = pd.DataFrame()
for path in paths:
    nc = netCDF4.Dataset(f'../runtvd/fslp01/{path}_0001.nc','r')
    index = 9
    zeta = nc.variables['zeta'][:,index]

    

    df[path] = zeta

df.to_csv('tide_concat_Tokyo.csv')