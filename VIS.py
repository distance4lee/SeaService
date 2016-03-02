# coding:utf8

from config import *

# fn = 'enso_20160220_fog.t00z.gvisg.grib2'


def readVIS_inbox(hours,year,month,day,prehour):
    '''
        INPUTS:
            hours = "3","6","9","12","18","24","36","72",...,"168"
            year,month,day
            prehour = "00","06","12","18"
        OUTPUTS:
            v as visibility, units in m
    '''
    thedate = date(year,month,day)
    fn = 'enso_%s_fog.t%sz.gvisg.grib2' % (
        thedate.strftime('%Y%m%d'),
        prehour,
    )
    fn_fullpath = os.path.join(VIS_DIR, fn) # VIS_DIR
    grbs = pygrib.open(fn_fullpath)
    grb_v = grbs.select(name='Visibility', level=10, forecastTime=int(hours))[0]
    v = grb_v.values # units in m
    lats,lons = grb_v.latlons()
    v,lats,lons = [i.ravel() for i in [v,lats,lons]]
    v = griddata(np.vstack((lons,lats)).T, v, (LONS,LATS), method='linear') # (LATS,LONS)
    v = [int(i) for i in v] # keep int
    return v


if __name__ == '__main__':
    hours,year,month,day,prehour = '24',2016,2,22,'00'
    v = readVIS_inbox(hours,year,month,day,prehour)
    print v