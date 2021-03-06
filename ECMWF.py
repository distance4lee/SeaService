# coding:utf8

from config import *

# fn = 'W_NAFP_C_ECMF_20160117175539_P_C1D01171200011712011.bz2'


def wait_for_readable(f, max_wait_time=120):
    def isReadable(f):
        return int(oct(os.stat(f).st_mode)[-1]) >= 4
    if not isReadable(f):
        w = 0
        while w < max_wait_time:
            if isReadable(f):
                break
            else:
                import time
                time.sleep(1)
                w += 1


def readECMWF_inbox(hours,year,month,day,prehour):
    '''
        INPUTS:
            hours = "3","6","9","12","18","24","36","72",...
            year,month,day
            prehour = "00" or "12"
        OUTPUTS:
            output in a dict
    '''
    thetime = datetime(year,month,day,int(prehour))
    thetime_pre = thetime + timedelta(hours=int(hours))
    fn = 'W_NAFP_C_ECMF_*_P_C1D{}00{}001'.format(
        thetime.strftime('%m%d%H'),
        thetime_pre.strftime('%m%d%H'),
    )
    fn_fullpath = glob.glob(os.path.join(ECMWF_FULLPATH, fn))
    fn_fullpath = fn_fullpath[0] if fn_fullpath else ''
    if fn_fullpath:
        wait_for_readable(fn_fullpath)
    else:
        f_bz2 = glob.glob(os.path.join(ECMWF_FULLPATH, fn + '.bz2'))
        f_bz2 = f_bz2[0] if f_bz2 else ''
        if f_bz2:
            os.system('bunzip2 -k {}'.format(f_bz2))
            fn_fullpath = f_bz2[:-4]
    grbs = pygrib.open(fn_fullpath)
    # precipitation
    grb_r = grbs.select(nameECMF='Total precipitation')[0]
    r = grb_r.values*1000.0 # mm
    r[r<0] = 0
    # lats.ravel(), lons.ravel(), points_in_box is the index of points in lats.ravel() or lons.ravel()
    lats,lons = grb_r.latlons()
    lats,lons = [i.ravel() for i in [lats,lons]]
    points_in_box = [i for i in range(len(lats)) if Nlat<=lats[i]<=Xlat and Nlon<=lons[i]<=Xlon] # Nlon,Xlon,Nlat,Xlat
    # snowfall
    grb_s = grbs.select(nameECMF='Snowfall')[0]
    s = grb_s.values*1000.0 # mm
    s[s<0] = 0
    # temperature
    grb_t = grbs.select(nameECMF='2 metre temperature')[0]
    t = grb_t.values - 273.15 # degree C
    # pressure
    grb_p = grbs.select(nameECMF='Mean sea level pressure')[0]
    p = grb_p.values/100.0 # hPa
    # cloud
    grb_c = grbs.select(nameECMF='Total cloud cover')[0]
    c = grb_c.values
    # wind
    grb_u = grbs.select(nameECMF='10 metre U wind component')[0]
    grb_v = grbs.select(nameECMF='10 metre V wind component')[0]
    u,v = grb_u.values,grb_v.values
    # take data for points in the box, maintain 1 decimal
    r,s,t,p,c,u,v = [i.ravel() for i in [r,s,t,p,c,u,v]]
    lats,lons = [
        [round(i[points_in_box[j]],3) for j in range(len(points_in_box))] for i in [lats,lons]
    ]
    r,s,t,p,c,u,v = [
        [round(i[points_in_box[j]],1) for j in range(len(points_in_box))] for i in [r,s,t,p,c,u,v]
    ]
    output = {
        'thetime':thetime, # forecast time UTC
        'thetime_pre':thetime_pre, # forecasted time UTC
        'lats':lats, # list of lats in box, same as below
        'lons':lons,
        'rainfall':r,
        'snowfall':s,
        'temperature':t,
        'pressure':p,
        'uwind':u,
        'vwind':v,
        'cloud':c,
    }
    return output


if __name__ == '__main__':
    hours, year, month, day, prehour = '24', 2016, 8, 31, '12'
    output = readECMWF_inbox(hours, year, month, day, prehour)
    # write 'lats_lons.pkl' and 'points.txt'
    lons, lats = [output.get(i) for i in ['lons', 'lats']]
    lats_lons = {'lats':lats, 'lons':lons}
    pkl = open('lats_lons.pkl', 'wb')
    pickle.dump(lats_lons, pkl)
    pkl.close()
    points = np.vstack([lons, lats]).T
    np.savetxt('points.txt', points, fmt='%1.3f')
    '''
    import pickle
    lats_lons = pickle.load(open('lats_lons.pkl', 'rb'))
    lats, lons = [lats_lons.get(i) for i in ('lats', 'lons')]

    grid_x,grid_y = np.mgrid[Nlon:Xlon+grid_delta:grid_delta,Nlat:Xlat+grid_delta:grid_delta] # grid_delta
    points2 = np.vstack([grid_x.T.ravel(),grid_y.T.ravel()[::-1]]).T

    points2 == points
    '''
