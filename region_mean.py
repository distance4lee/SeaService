# coding:utf8

from coding import *


def make_points_from_latslons(lats,lons):
    '''
        lats,lons in list with the same length
    '''
    points = [(lons[i],lats[i]) for i in range(len(lats))]
    return points


def points_in_dict(points,poly):
    '''
        points is a list in format [(x0,y0),(x1,y1),...,(xn,yn)]
        poly is a list in format [[1,1],[1,4],[3,7],[4,4],[4,1]]
    '''
    points_in_dict_TrueFalse = [point_in_poly(i) for i in poly]
    return points_in_dict_TrueFalse


def region_mean(var,points_in_dict_TrueFalse):
    '''
        var in a list with the same length of points
    '''
    var = [var[i] for i,a in enumerate(points_in_dict_TrueFalse) if a]
    var_mean = np.mean(var)
    return var_mean


