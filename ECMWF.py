# coding:utf8

from config import *


# fn = 'W_NAFP_C_ECMF_20160117175539_P_C1D01171200011712011.bin'

def readECMWF(hours,year,month,day,prehour):
    thedate = datetime(year,month,day,int(prehour))
    thedate_pre = thedate + timedelta(hours=int(hours))
    fn = 'W_NAFP_C_ECMF_*_P_C1D%s00%s001.bin' % (
        thedate.strftime('%m%d%H'),
        thedate_pre.strftime('%m%d%H'),
    )
    fn_fullpath = os.popen('ls %s' % os.path.join(ECMWF_FULLPATH, fn)).read()
    fn_fullpath = fn_fullpath.replace('\n','')
    grbs = pygrib.open(fn_fullpath)
    # precipitation
    grb_r = grbs.select(nameECMF='Total precipitation')[0]
    r = grb_r.values*1000.0 # mm
    r[r<0] = 0
    lats,lons = grb_r.latlons()
    # snowfall
    grb_s = grbs.select(nameECMF='Snowfall')[0]
    s = grb_s.values*1000.0 # mm
    s[s<0] = 0
    # temperature
    grb_t = grbs.select(nameECMF='2 metre temperature')[0]
    t = grb_t.values - 273.15 # degree C
    # 

    return thedate,lats,lons,r


if __name__ == '__main__':
    # 00h to 24h
    hours,year,month,day,prehour = '24',2016,2,16,'00'
    thedate,lats,lons,r = readECMWF(hours,year,month,day,prehour)
