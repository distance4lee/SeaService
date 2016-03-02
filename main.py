# coding:utf8

from ECMWF import *
from VIS import *
from WAVE import *
from region_mean import *
from wind_weather import *


def test(hours,year,month,day,prehour):
    # init ECMWF vars: rainfall,snowfall,temperature,pressure,uwind,vwind,cloud,weather,height_wave
    r,s,t,p,u,v,c,w,vis,hwave = [None for i in range(10)]
    # read ECMWF
    output = readECMWF_inbox(hours,year,month,day,prehour)
    thetime,thetime_pre,r,s,t,p,u,v,c = [
        output.get(i) for i in [
            'thetime','thetime_pre',
            'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
        ]
    ]
    del output
    ws,wd = [[uv2wswd(u[i],v[i])[j] for i in range(len(u))] for j in range(2)]
    # read VIS
    vis = readVIS_inbox(hours,year,month,day,prehour)
    # get weather_type
    w = [weather_type(r[i],s[i],c[i],v[i]) for i in range(len(r))]
    # read WAVE
    hwave = readWAVE_inbox(hours,year,month,day,prehour).get('HTSGW')
    # write out grid data
    try:
        data = np.vstack([r,s,t,p,ws,wd,w,vis,hwave]).T
        grid_fn = '%s_%s' % (thetime.strftime('%Y%m%d%H'),thetime_pre.strftime('%Y%m%d%H'))
        np.savetxt(os.path.join(OUTPUT_DIR,grid_fn), data, fmt='%1.1f') # OUTPUT_DIR
    except:
        pass


def fcst_delta_hours(fromhours,year,month,day,prehour,delta_hours=3):
    '''
        INPUTS:
            fromhours = 0,3,6,9,...,69
            year,month,day,prehour as in readECMWF_inbox, readVIS_inbox, readWAVE_inbox
        OUTPUTS:
            a file named like 'S2016022400_000_003_F2016022403.txt'
    '''
    tohours = fromhours + delta_hours
    # init ECMWF vars: rainfall,snowfall,temperature,pressure,uwind,vwind,cloud,weather,height_wave
    r,s,t,p,u,v,c,w,vis,hwave = [None for i in range(10)]
    if not fromhours:
        # fromhours = 0
        output = readECMWF_inbox(tohours,year,month,day,prehour)
        thetime,thetime_pre,r,s,t,p,u,v,c = [
            output.get(i) for i in [
                'thetime','thetime_pre',
                'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
            ]
        ]
    else:
        # fromhours get rainfall and snowfall as r0,s0
        output = readECMWF_inbox(fromhours,year,month,day,prehour)
        r0,s0 = [output.get(i) for i in ['rainfall','snowfall']]
        output = readECMWF_inbox(tohours,year,month,day,prehour)
        thetime,thetime_pre,r,s,t,p,u,v,c = [
            output.get(i) for i in [
                'thetime','thetime_pre',
                'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
            ]
        ]
        # get rainfall and snowfall during delta_hours
        r = [r[i]-r0[i] for i in range(len(r))]
        s = [s[i]-s0[i] for i in range(len(s))]
    del output
    ws,wd = [[uv2wswd(u[i],v[i])[j] for i in range(len(u))] for j in range(2)]
    vis = readVIS_inbox(tohours,year,month,day,prehour)
    w = [weather_type(r[i],s[i],c[i],v[i]) for i in range(len(r))]
    hwave = readWAVE_inbox(tohours,year,month,day,prehour).get('HTSGW')
    ''' format data in columns of
            rainfall,snowfall,temperature,pressure,
            windspeed,winddirection,weather_type,visibility,height_wave '''
    data = np.vstack([r,s,t,p,ws,wd,w,vis,hwave]).T
    del r,s,t,p,ws,wd,w,vis,hwave
    grid_fn = 'S%s_%s_%s_F%s.txt' % (
        thetime.strftime('%Y%m%d%H'),
        '0'*(3-len(str(fromhours))) + str(fromhours),
        '0'*(3-len(str(tohours))) + str(tohours),
        thetime_pre.strftime('%Y%m%d%H')
    )
    np.savetxt(os.path.join(OUTPUT_DIR,grid_fn), data, fmt='%1.1f') # OUTPUT_DIR


def fcst_72hours_every_3hours(year,month,day,prehour,
        delta_hours=3,start_hours=3,end_hours=72):
    '''
        INPUTS:
            year,month,day,prehour as in readECMWF_inbox, readVIS_inbox, readWAVE_inbox
        OUTPUS:
            24 files named from
            'S2016022400_000_003_F2016022403.txt'
            to 
            'S2016022400_069_072_F2016022700.txt'
            single file data in columns of
                rainfall (mm)
                snowfall (mm)
                temperature (degree C)
                pressure (hPa)
                windspeed (m/s)
                winddirection (int code)
                weather_type (int code)
                visibility (m)
                height_wave (m)
    '''
    TOHOURS = list(range(start_hours,end_hours+delta_hours,delta_hours))
    OUTPUTs,VISs,HWAVEs = [list(range(len(TOHOURS))) for i in range(3)]
    for i in OUTPUTs:
        hours = TOHOURS[i]
        OUTPUTs[i] = readECMWF_inbox(hours,year,month,day,prehour)
        VISs[i] = readVIS_inbox(hours,year,month,day,prehour)
        HWAVEs[i] = readWAVE_inbox(hours,year,month,day,prehour).get('HTSGW')
    for tohours in TOHOURS:
        fromhours = tohours - delta_hours
        if not fromhours:
            output = OUTPUTs[TOHOURS.index(tohours)]
            thetime,thetime_pre,r,s,t,p,u,v,c = [
                output.get(i) for i in [
                    'thetime','thetime_pre',
                    'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
                ]
            ]
        else:
            output = OUTPUTs[TOHOURS.index(fromhours)]
            r0,s0 = [output.get(i) for i in ['rainfall','snowfall']]
            output = OUTPUTs[TOHOURS.index(tohours)]
            thetime,thetime_pre,r,s,t,p,u,v,c = [
                output.get(i) for i in [
                    'thetime','thetime_pre',
                    'rainfall','snowfall','temperature','pressure','uwind','vwind','cloud'
                ]
            ]
            # get rainfall and snowfall during delta_hours
            r = [r[i]-r0[i] for i in range(len(r))]
            s = [s[i]-s0[i] for i in range(len(s))]
        del output
        ws,wd = [[uv2wswd(u[i],v[i])[j] for i in range(len(u))] for j in range(2)]
        vis = VISs[TOHOURS.index(tohours)]
        w = [weather_type(r[i],s[i],c[i],v[i]) for i in range(len(r))]
        hwave = HWAVEs[TOHOURS.index(tohours)]
        ''' format data in columns of
            rainfall,snowfall,temperature,pressure,
            windspeed,winddirection,weather_type,visibility,height_wave '''
        data = np.vstack([r,s,t,p,ws,wd,w,vis,hwave]).T
        del r,s,t,p,ws,wd,w,vis,hwave
        grid_fn = 'S%s_%s_%s_F%s.txt' % (
            thetime.strftime('%Y%m%d%H'),
            '0'*(3-len(str(fromhours))) + str(fromhours),
            '0'*(3-len(str(tohours))) + str(tohours),
            thetime_pre.strftime('%Y%m%d%H')
        )
        np.savetxt(os.path.join(OUTPUT_DIR,grid_fn), data, fmt='%1.1f') # OUTPUT_DIR


if __name__ == '__main__':
    from datetime import date,timedelta
    yestoday = datetime.today() - timedelta(days=1)
    year,month,day = yestoday.year,yestoday.month,yestoday.day
    ''' test fcst_delta_hours '''
    # start_at = datetime.now()
    # for i in range(0,25,3):
    #     fcst_delta_hours(i,year,month,day,'00')
    #     print datetime.now() - start_at
    ''' test fcst_72hours_every_3hours '''
    start_at = datetime.now()
    fcst_72hours_every_3hours(year,month,day,'00',delta_hours=3,start_hours=3,end_hours=24)
    print datetime.now() - start_at
