# coding:utf8

from config import *


def make_points_from_latslons(lons,lats):
    '''
        lats,lons in list with the same length
    '''
    points = [[lons[i],lats[i]] for i in range(len(lats))]
    return points


def points_in_region(points,region):
    '''
        MIDDLEWARE FUNCTION called by points_in_regions
        points is a list in format [(x0,y0),(x1,y1),...,(xn,yn)]
        region is a list in format [[1,1],[1,4],[3,7],[4,4],[4,1]]
    '''
    points_in_region_TrueFalse = [int(point_in_poly(point,region)) for point in points] # 1:True,0:False
    return points_in_region_TrueFalse


def points_in_regions(points,regions):
    '''
        OUTPUT for INPUT into region_means
        regions in [offshore_polys, coastal_polys]
    '''
    points_in_region_TrueFalseS = [points_in_region(points,region) for region in regions]
    return points_in_region_TrueFalseS


def region_mean(var,points_in_region_TrueFalse):
    '''
        MIDDLEWARE FUNCTION called by region_means
        var in a list with the same length of points
    '''
    var = [var[i] for i,a in enumerate(points_in_region_TrueFalse) if a]
    var_mean = round(np.mean(var), 1) # keep 1 decimal
    return var_mean


def region_means(var,points_in_region_TrueFalseS):
    '''
        FINAL FUNCTION
    '''
    var_means = [
        region_mean(var,tf) for tf in points_in_region_TrueFalseS
    ]
    return var_means


if __name__ == '__main__':
    from ECMWF import *
    hours,year,month,day,prehour = '24',2016,2,20,'00'
    output = readECMWF_inbox(hours,year,month,day,prehour)
    #'''
    lats,lons,var = [output.get(i) for i in ['lats','lons','temperature']]
    points = make_points_from_latslons(lons,lats)
    points_in_region_TrueFalseS = {
        'offshore':points_in_regions(points,offshore_polys),
        'coastal':points_in_regions(points,coastal_polys)
    }
    pkl = open('points_in_region_TrueFalseS.pkl','wb')
    pickle.dump(points_in_region_TrueFalseS, pkl)
    pkl.close()
    for regions in ['offshore','coastal']:
        print region_means(var,points_in_region_TrueFalseS.get(regions)) # points_in_region_TrueFalseS
    #'''
    # for short as below
    '''
    var = output.get('temperature')
    for regions in ['offshore','coastal']:
        print region_means(var,points_in_region_TrueFalseS.get(regions)) # points_in_region_TrueFalseS
    #'''
