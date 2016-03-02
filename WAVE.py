#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''Simple
@author: Li Jiapeng <distance4lee@gmail.com>
@original code: Ren Yu 
@license: LGPLv3+
'''

from config import *


def readWAVE_inbox(hours,year,month,day,prehour):
    '''
        INPUTS:
            hours = "3","6","9","12","18","24","36","72",...,"168"
            year,month,day
            prehour = "00","06","12","18"
        OUTPUTS:
            HTSGW: Significant height of combined wind waves and swell(有效波高), units: meter
            PERPW: Primary wave mean period(平均周期), units: second
            WVHGT: Significant height of wind waves(风浪有效波高), units: meter
            WVPER: Mean period of wind waves(风浪平均周期), units: second
            SWELL: Significant height of swell waves(涌浪有效波高), units: meter
            SWPER: Mean period of swell waves(涌浪平均周期), units: second

            All elements packed in dict
    '''
    # varlist = ['HTSGW','PERPW','WVHGT','WVPER','SWELL','SWPER']
    varlist = ['HTSGW',]

    output={}

    thedate = date(year,month,day)
    fn = 'enso_%s_gwes.mean.t%sz.grib2' % (
        thedate.strftime('%Y%m%d'),
        prehour,
    )
    fn_fullpath = os.path.join(WAVE_DIR, fn) # WAVE_DIR
    grbs = pygrib.open(fn_fullpath)

    for var in varlist:
        grb_v = grbs.select(name=ELE_WAVE_nameGFS.get(var), level=0, forecastTime=int(hours))[0]
        v = grb_v.values
        lats,lons = grb_v.latlons()
        v,lats,lons = [i.ravel() for i in [v,lats,lons]]
        # mind that 9999.0 as missing values
        v = [i if i<9990 else 0 for i in v]
        v = griddata(np.vstack((lons,lats)).T, v, (LONS,LATS), method='linear') # (LATS,LONS)
        v = [round(i,1) for i in v] # keep 1 decimal
        v = [i if i else 9999 for i in v]
        output.update({var:v})

    return output


if __name__ == '__main__':
    from datetime import date,timedelta
    yestoday = datetime.today() - timedelta(days=1)
    year,month,day = yestoday.year,yestoday.month,yestoday.day
    hours = '3'
    prehour = '00'
    output = readWAVE_inbox(hours,year,month,day,prehour)
    print output
