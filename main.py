# coding:utf8

from ECMWF import *
from VIS import *
from region_mean import *
from wind_weather import *


def main(hours,year,month,day,prehour):
    # init vars: rainfall,snowfall,temperature,pressure,uwind,vwind,cloud,weather
    r,s,t,p,u,v,v,c,w = [None for i in range(9)]
    # read ECMWF
    try:
        output = readECMWF_inbox(hours,year,month,day,prehour)
        thetime,thetime_pre,r,s,t,p,u,v,c = [
            output.get(i) for i in [
                'thetime','thetime_pre',
                'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
            ]
        ]
        del output
        ws,wd = [[uv2wswd(u[i],v[i])[j] for i in range(len(u))] for j in range(2)]
    except:
        print('!!! readECMWF_inbox Error !!!')

    # output = readECMWF_inbox(hours,year,month,day,prehour)
    # thetime,thetime_pre,r,s,t,p,u,v,c = [
    #     output.get(i) for i in [
    #         'thetime','thetime_pre',
    #         'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
    #     ]
    # ]
    # del output
    # ws,wd = [[uv2wswd(u[i],v[i])[j] for i in range(len(u))] for j in range(2)]

    # read VIS
    try:
        v = readVIS_inbox(hours,year,month,day,prehour)
    except:
        print('!!! readVIS_inbox Error !!!')
    # get weather_type
    w = [weather_type(r[i],s[i],c[i],v[i]) for i in range(len(r))]
    # write out grid data
    try:
        data = np.vstack([r,t,p,ws,wd,w]).T
        grid_fn = '%s_%s' % (thetime.strftime('%Y%m%d%H'),thetime_pre.strftime('%Y%m%d%H'))
        np.savetxt(os.path.join(OUTPUT_DIR,grid_fn), data, fmt='%1.1f')
    except:
        pass


if __name__ == '__main__':
    main('3',2016,2,21,'00')