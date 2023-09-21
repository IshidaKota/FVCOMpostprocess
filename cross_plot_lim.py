#plot different simulations at the same time.
import pandas as pd
import matplotlib.pyplot as plt
import sys
#import matplotlib.colors as mcolors
from matplotlib import dates as mdates
#import numpy as np
import datetime
plt.rcParams['font.family'] = 'VL Gothic'
plt.rcParams['font.size'] = 14

def main():


    place = 'chibaharo'
    variables = ['salinity','temperature']
    units = ['PSU','degC']
    print("--------enter the label of eachfile------")
    files = [sys.argv[i] for i in range(1,len(sys.argv))]
    labels = [x for x in input().split()]
    num = "".join([file[-1] for file in files])
   # css_colors = mcolors.BASE_COLORS
   # uni_colors=["#FF4B00","#005AFF","#03AF7A","#40C4FF","#F6AA00","#FFF100","#990099"]
    uni_colors=["#FF4B00","#005AFF","#990099","#03AF7A","#F6AA00","#FFF100","#40C4FF",]
    alpha = 1
    if len(files) == 1:
        alpha=0.7
    

    print(files)
    start,stop = 1,2100
    for variable,unit in zip(variables,units):
        fig,axs=plt.subplots(1,2,figsize=(16,6),facecolor="white")
        #if variable=='salinity':
        #    plt.suptitle('風力の変化による塩分の変化')  
        #else:
        #    plt.suptitle('風力の変化による水温の変化') 
        sxmin='2020-02-01'
        sxmax='2020-05-31'
        xmin = datetime.datetime.strptime(sxmin, '%Y-%m-%d')
        xmax = datetime.datetime.strptime(sxmax, '%Y-%m-%d')
        #plt.xlim([xmin,xmax])
        #for j,place in enumerate(places):
        df = pd.read_csv('./data/interp/'+place+'_'+variable+'ext_2020.csv')
        dates = pd.to_datetime(df.columns[1:])

        #upper
        axs[0].set_ylabel(variable+' ('+unit+')',)
        #axs[0].set_xlabel('Date')
        axs[0].set_title(f"<表層>{place}")
        axs[0].set_ylim(9,35)
        axs[0].set_xlim(xmin,xmax)
        #bottom
        axs[1].set_ylabel(variable+' ('+unit+')',)
        #axs[1].set_xlabel('Date')
        axs[1].set_title(f"<底層> {place}")
        axs[1].set_ylim(9,35)
        axs[1].set_xlim(xmin,xmax)

        #plot
        if place == 'chiba1buoy' and variable == 'salinity':
            tmp = pd.read_csv('./data/interp/chiba1buoykokyo.csv')
            axs[0].plot(dates[:],df.iloc[2,1:],color="black",linestyle='solid',linewidth=1.0,alpha=0.8,label='観測値')
            date = pd.to_datetime(tmp['date'])
            axs[1].scatter(date,tmp['塩分量(海域)'][:],color='red',label='観測値(公共用水域)')
            print(type(tmp['date'][0]))
        if place == 'kawasaki' and variable == 'salinity':
            tmp = pd.read_csv('./data/interp/chiba1buoykokyo.csv')
            axs[0].plot(dates[:],df.iloc[2,1:],color="black",linestyle='solid',linewidth=1.0,alpha=0.8,label='観測値')
            date = pd.to_datetime(tmp['date'])
            axs[1].scatter(date,tmp['塩分量(海域)'][:],color='red',label='観測値(公共用水域)')
        else:
            axs[0].plot(dates[:],df.iloc[2,1:],color="black",linestyle='solid',linewidth=1.0,alpha=0.8,label='観測値')
            axs[1].plot(dates[:],df.iloc[28,1:],color="black",linestyle='solid',linewidth=1.0,alpha=0.8,label='観測値')

        for file,color,Label in zip(files,uni_colors,labels):
            path ='./df/result/'+place+variable+'_'+file+'_.csv'
            df = pd.read_csv(path)
            column = pd.to_datetime(df['date'])

            if '0' in df.columns:
                axs[0].plot(column[1:],df['0'][1:],color=color,alpha=alpha,label=Label,linewidth=1.0)
            else:
                axs[0].plot(column[:],df['2'][:],color=color,alpha=alpha,label=Label,linewidth=1.0)
            
            axs[1].plot(column[:],df['28'][:],color=color,alpha=alpha,label=Label,linewidth=1.0)

            axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            axs[0].legend(ncols=2,framealpha=0)#;axs[0].grid();axs[1].set_ylim(15,35)

            axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            axs[1].legend(ncols=2,framealpha=0)#;axs[1].grid();axs[1].set_ylim(15,35)

            # if variable == 'temperature':
            #     axs[0].set_ylim(9,35)
            #     axs[1].set_ylim(9,35)
    #fig.legend()

    # axs[3,1].legend(bbox_to_anchor=(0.5,-0.1), loc='upper center',ncols=2)
    #axs[3,1].text(1.05,1,'赤丸は公共用水域の観測値')
    #plt.legend(bbox_to_anchor=(1.05,1), loc='upper left', borderaxespad=0, fontsize=20)
        plt.tight_layout()
        fig.savefig('./png/cross_plot/slice'+variable+'_'+num+files[0]+'.png',\
        bbox_inches='tight', pad_inches=0.1,dpi=600)


    #diff
    """
    if len(files) ==2:
        for variable in variables:

            #case salinity or case temperature
            fig,axs = plt.subplots(1,4,figsize=(14,3),sharey='all')
            plt.suptitle(f'difference of {variable} : {labels[1]} - {labels[0]}')
            for place,ax in zip(places,axs):
                paths = ['./df/result/'+place+variable+'_'+file+'_.csv' for file in files]
                df1   = pd.read_csv(paths[0])
                df2   = pd.read_csv(paths[1])
                ratio =np.round((1+len(df2))/(1+len(df1)))
                if ratio < 1:
                    ratio = np.round((1+len(df1))/(1+len(df2)))
                #ratio = 24
                ratio = int(ratio)
                for siglay,label in zip([2,4],['upper','bottom']):
                    if len(df2)>=len(df1):
                        diff = [df2.iat[ratio*i,siglay]-df1.iat[i,siglay] for i in range(len(df1))]
                    else:
                        diff = [df2.iat[i,siglay]-df1.iat[ratio*i,siglay] for i in range(1,len(df2))]
                    ax.plot(diff,label = label);ax.set_title(f"{place}")
                    ax.set_ylabel(f"{variable}");ax.set_xlabel("*4 hours  since 2020/1/1");ax.legend()
                ax.plot([0 for i in range(len(df2))],color='black',linewidth=0.1)
            #plt.xticks([i for i in range(len(diff))],[i for i in range(int(len(diff)/6))])
            plt.tight_layout()
            fig.savefig('./png/cross_plot/diff_'+variable+'_'+num+'.png',\
                            bbox_inches='tight', pad_inches=0.1,dpi=300)
                
            #bottom
    """

if __name__ == '__main__':
    main()


 