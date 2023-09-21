#first cretated by ishid @ 2023/03/14

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib import dates as mdates
import netCDF4
from pyproj import Proj
#from jdcal import gcal2jd, jd2gcal ,MJD_0
#import datetime
from mod_util import in_rect

#read 
def read_nc(ncfile_path="../runtvd/fslp01/tvdf01_w3"+"_0001.nc"):
   # ncfile_path = "../runtvd/tvdf01/tvdf01_w3"+"_0001.nc"#relative_path
    nc = netCDF4.Dataset(ncfile_path, 'r')
  #  print(nc.variables.keys()) #option
    return nc


def find_nearest_node(lon,lat,x_node= None,y_node = None):

    """
    lon:経度,lat:緯度
    """

    #covert example from https://qiita.com/spicy_HotChicken/items/4cdf303493d73e24dc14
    #<-------------
    ##Define EQA2UTM converter
    #e2u_conv=Proj(proj='utm', zone=e2u_zone, ellps='WGS84')
    ##Apply the converter
    #utmx, utmy=e2u_conv(lon, lat)
    #>-------------

    #lat,lon = ()(140.0233033,35.61095833)
    conv=Proj(proj='utm', zone=54, ellps='WGS84')
  #  print(lon,lat)
    x_station,y_station =conv(lon,lat)#[0],conv(lon,lat)[1]
   # print(x_station,y_station)

   # nc = read_nc()
   # x_node,y_node = nc.variables['x'][:],nc.variables['y'][:] #node (x,y) list, unit is m : projection is UTM 54 N
    distances_to_station = [(x-x_station)**2 + (y-y_station)**2 for x,y in zip(x_node,y_node)]
    min_dist = min(distances_to_station)
    node = distances_to_station.index(min_dist) #finally we find the node nearest station
    print(node)
    return node

def xy_num():
    nc = read_nc()
    x_node,y_node = nc.variables['x'][:],nc.variables['y'][:] #node (x,y) list, unit is m : projection is UTM 54 N

    return x_node,y_node


def read_d15n_csv(csv_file_path="./data/kaigan/observe_d15n.csv"):
    df = pd.read_csv(csv_file_path \
                     ,usecols= ['緯度\n世界測地系','経度\n世界測地系','d15 N vs. Air','測点名'])#,'水深(m)'
    
    #rename https://note.nkmk.me/python-pandas-dataframe-rename/
    #df.rename(columns={'A': 'Col_1', 'C': 'Col_3'}))
    df = df.rename(columns= \
                   {'緯度\n世界測地系':"lat",'経度\n世界測地系':"lon",'d15 N vs. Air':"d15n",'測点名':"place"}) #,'水深(m)':"depth"
    return df

def plot_map(csv_file_path='./data/kaigan/observe_d15n_east2.csv'):
    df = read_d15n_csv(csv_file_path=csv_file_path)
    import geopandas as gpd
    plt.rcParams['font.size'] =10
    fig,ax = plt.subplots()
    ax.set_aspect("equal")
    path ="C23-06_TOKYOBAY.shp"
    data = gpd.read_file(path, encoding = 'sjis')

    ax.scatter(df['lon'],df['lat'])
    data.plot(ax=ax,color="black",lw=0.7,alpha=0.6)
    for i in range(len(df['lon'])):
        ax.text(df['lon'][i],df['lat'][i],df['place'][i])

    ax.set_xlim(139.6,140.1)
    ax.set_ylim(34.9,35.7)
    fig.savefig('./png/kaigan/din_map.png',dpi=600,bbox_inches='tight')

def read_DYE(csv_file_path="./data/kaigan/observe_d15n_east.csv"):
    x_node,y_node = xy_num()

    nc_DYE_all_in = read_nc(ncfile_path="../rundye/exp31/exp0_0001.nc")
    DYE_all = nc_DYE_all_in.variables["DYE"][:,:,:]

    #dye of open boundary
    nc_obc = read_nc(ncfile_path="../rundye/exp31/exp18_0001.nc")
    DYE_obc = nc_obc.variables["DYE"][:,:,:] #time*siglay*node

    df = read_d15n_csv(csv_file_path=csv_file_path)

    obc_DYE_ratio_ave_place = []
    for lon,lat in zip(df['lon'][:],df['lat'][:]):
        node = find_nearest_node(lon,lat,x_node=x_node,y_node=y_node)
        DYE_obc_time_ave = np.average(DYE_obc[24*40:24*50,0,node])
        DYE_all_time_ave = np.average(DYE_all[24*40:24*50,0,node])

        obc_DYE_ratio =1- DYE_obc_time_ave/DYE_all_time_ave
        obc_DYE_ratio_ave_place.append(obc_DYE_ratio*100)


    print(obc_DYE_ratio_ave_place)
    df['DIN'] = obc_DYE_ratio_ave_place
    return df

def plot_DIN_map(csv_file_path='./data/kaigan/observe_d15n_east.csv'):
    df = read_d15n_csv(csv_file_path=csv_file_path)

    obc_DYE_ratio_ave_place = read_DYE()
    import geopandas as gpd
    path ="C23-06_TOKYOBAY.shp"
    data = gpd.read_file(path, encoding = 'sjis')

    #plot
    fig,ax = plt.subplots()
    data.plot(ax=ax,color="grey",lw=0.4)
    ax.scatter(df['lon'],df['lat'])#,obc_DYE_ratio_ave_place)
    for i in range(len(df['lon'])):
        ax.text(df['lon'][i],df['lat'][i],str("{:.2f}".format(obc_DYE_ratio_ave_place[i])))
    ax.set_aspect("equal")

    fig.savefig('./png/kaigan/DYE_upper_profile.png',dpi=600)

def plot_DIN_graph(csv_file_path='./data/kaigan/observe_d15n_east2.csv'):

    # df.sort_values('item') https://note.nkmk.me/python-pandas-sort-values-sort-index/
    df = read_d15n_csv(csv_file_path=csv_file_path)
    df = df.sort_values('lat', ascending=False)
    df = df.reset_index(drop=True)
    print(df['d15n'])

    df_DYE = read_DYE()
    df_DYE = df_DYE.sort_values('lat', ascending=False)


    #plot
    fig,ax = plt.subplots(figsize=(10,6))
    ax2 = ax.twinx()
    ax2.plot(df['place'],df['d15n'],c="red")

    ax.plot(df['place'],df_DYE['DIN'])

    # settings https://qiita.com/ganyariya/items/98fbedee87befc909884
   # ax.set_xlabel(rotation=90)
    plt.xticks(rotation=90) 

    fig.savefig('./png/kaigan/DYE_upper_graph.png',dpi=600)



#----------------------------------------------#
#以下漁場ごと
#----------------------------------------------#

def read_map_and_dye(path):
    nc = netCDF4.Dataset(path,'r')
    #read_dye
    #print(nc.variables['DYE'])
    dye = nc.variables['DYE'][:,:,:].data #time,siglay,node
    art1 = nc.variables['art1'][:].data # node control area の面積
    siglay = nc.variables['siglay'][:,100].data
    
    #read_map
    h = nc.variables['h'][:].data
    x = nc.variables['x'][:].data
    y = nc.variables['y'][:].data
    e2u_conv=Proj(proj='utm', zone=54, ellps='WGS84') #Convert UTM2EQA
    rslt = [e2u_conv(lon,lat,inverse=True) for lon,lat in zip(x,y)]
    lon = [rslt[i][0] for i in range(len(rslt))]
    lat = [rslt[i][1] for i in range(len(rslt))]
    
    triangles = nc.variables['nv'][:].T-1
    
    return dye,lon,lat,triangles,h,art1,siglay

def ave_concentration(path,rect,rect2_flag=False,rect2=0):
    """
    40日目から50日目におけるDYEの漁場での表層平均濃度を返す
    """
    dye,lon,lat,triangles,h,art1,siglay = read_map_and_dye(path) #dyeは引き算になったのでここで読み込まない
    in_node = [in_rect(rect,[lonn,latn]) for lonn,latn in zip(lon,lat)]
    if rect2_flag:
        in_node2=[in_rect(rect2,[lonn,latn]) for lonn,latn in zip(lon,lat)]
    ntime,nsiglay,nnode=dye.shape
    
    #calc average
    cnt,c = 0,0
    for i in range(nnode):
        if rect2_flag:
            if in_node2[i]:
             #   volume += art1[i] * h[i]
             #   for j in range(nsiglay):
             #       c[:] += dye[:,j,i] * art1[i] * (1/30) * h[i]# *ratio
                c +=   np.average(dye[24*40:24*50,0,i])
                cnt +=1     

        if in_node[i]:
           # volume += art1[i] * h[i]
           # for j in range(nsiglay):
           #     c[:] += dye[:,j,i] * art1[i] * (1/30) * h[i]# *ratio
           c +=   np.average(dye[24*40:24*50,0,i])
           cnt +=1
                
    #ave_c = np.zeros(ntime)            
    #ave_c[:] = c[:]/volume
    average_concentration = c /cnt
    
    return average_concentration

def plot_fisher_origin(rect,save_name="test",rect2=None,rect2_flag=False):
    dye_all = ave_concentration(f"../rundye/exp31/exp0_0001.nc",rect)
    ratio = []
    for i in range(1,19):
        dye_each = ave_concentration(f"../rundye/exp31/exp{i}_0001.nc",rect,rect2=rect2,rect2_flag=rect2_flag)
        r = 1 -dye_each/dye_all
        if r < 0:
            r = 0
        ratio.append(r)

    print(ratio)

    ratio = [r/sum(ratio) for r in ratio]

#    df = pd.DataFrame()
#    df['name'] = ["Arakawa","Sumidagawa","edogawa","Tamagawa","Tsurumigawa","Mamagawa","Ebigawa","Yorogawa",\
#    "Obitsugawa","Koitogawa","Muratagawa","Hanamigawa","Shibaura","Sunamachi","Ariake","Morigasaki","Kasai","Open Boundary"]
#    df['ratio'] = ratio

#    df.to_csv(f"./png/kaigan/fisher_{save_name}.csv")

    #fig,ax = plt.subplots()

    #ax.stackplot(["save_name"],ratio)

    #fig.savefig(f"./png/kaigan/fisher_{save_name}.png",dpi=600)

    return ratio
def plot():
    ratio_futtsu   =     plot_fisher_origin(rect_futtsu,save_name="futtsu")
    ratio_sanbanze =     plot_fisher_origin(rect_San1,rect2=rect_San2,rect2_flag=True,save_name="sanbanze")
    ratio_kisarazu =     plot_fisher_origin(rect_Kisarazu,save_name="kisaraze")
    #ratio_plot = np.zeros((3,4))
    #for i,ratio in enumerate([ratio_futtsu,ratio_sanbanze,ratio_kisarazu]):
    #    ratio_plot[i,0] = sum(ratio[:4])

    #    ratio_place.append([ratio[:4],ratio[5:11],ratio[12:16],ratio[17]])
    #    ratio_plot.append(ratio_place)
    #print(ratio_plot)
    fig,axs = plt.subplots(3,1)
    place = ["futtsu","sanbanze","kisarazu"]
    
    for ax,ratio in zip(axs,[ratio_futtsu,ratio_sanbanze,ratio_kisarazu]):
        ax.stackplot(place,[sum(ratio[:4]),sum(ratio[5:11]),sum(ratio[12:16]),ratio[17]])

    fig.savefig('./png/kaigan/fisher_stackplot.png',dpi=600)

#river_list = ["Arakawa","Sumidagawa","edogawa","Tamagawa","Tsurumigawa","Mamagawa","Ebigawa","Yorogawa",\
#    "Obitsugawa","Koitogawa","Muratagawa","Hanamigawa","Shibaura","Sunamachi","Ariake","Morigasaki","Kasai","Open Boundary"]


if __name__ == "__main__":
    rect_futtsu = [[139.78523, 35.31256],[139.81572, 35.32],[139.80904, 35.34579], \
                [139.77752, 35.33203]]
    rect_San1 = [[139.93942,35.64125],[139.96,35.64846],[139.94588,35.66822],[139.92355,35.66126]]
    rect_San2 = [[139.96942,35.65025],[139.9819,35.65146],[139.97288,35.66922],[139.95355,35.67126]]
    rect_Kisarazu = [[139,.85992,35.3739],[139.94,35.39],[139.93134,35.44],[139.878,35.437]]
    #plot()
    plt.rcParams['font.size'] =16
  #  plot_DIN_graph()
    plot_map()
    #plot_fisher_origin(rect_futtsu)