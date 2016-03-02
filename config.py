# coding:utf8

'''
    Work on 192.168.2.127

    cmacast on 192.168.2.125 mounted on 127, i.e.
        //192.168.2.125/cmacast on /mnt/cmacast

    ECMWF data on path:
        /mnt/cmacast/NWP_MCTR_002/ECMF_DAM/PUB/
'''

import os
import pickle
import numpy as np
import pygrib
from collections import OrderedDict
from datetime import datetime,date,timedelta
from scipy.interpolate import griddata

from ispointinpoly import point_in_poly
from sea_dicts import *


CMACAST_DIR = '/mnt/cmacast'
ECMWF_DIR = 'NWP_MCTR_002/ECMF_DAM/PUB/'

ECMWF_FULLPATH = os.path.join(CMACAST_DIR,ECMWF_DIR)

ELE_SFC_nameECMF = {
    # temperature
    '2T':'2 metre temperature',
    '2D':'2 metre dewpoint temperature',
    'SKT':'Skin temperature',
    'SSTK':'Sea surface temperature',
    # cloud
    'TCC':'Total cloud cover',
    'LCC':'Low cloud cover',
    # pressure
    'MSL':'Mean sea level pressure',
    # wind
    '10U':'10 metre U wind component',
    '10V':'10 metre V wind component',
    # precipitation
    'TP':'Total precipitation',
    'TCW':'Total column water',
    'TCWV':'Total column water vapour',
    'LSP':'Large-scale precipitation',
    'CP':'Convective precipitation',
    'CAPE':'Convective available potential energy',
    # snow
    'SD':'Snow depth',
    'SF':'Snowfall',
    'RSN':'Snow density',
    # albedo
    'FAL':'Forecast albedo',
}

ELE_WAVE_nameGFS = {
    'HTSGW': 'Significant height of combined wind waves and swell',
    'PERPW': 'Primary wave mean period',
    'WVHGT': 'Significant height of wind waves',
    'WVPER': 'Mean period of wind waves',
    'SWELL': 'Significant height of swell waves',
    'SWPER': 'Mean period of swell waves'
}

Nlon,Xlon,Nlat,Xlat = 105,130,2,41
grid_delta = 0.125


VIS_DIR = '/home/enso/noaa/visibility'
WAVE_DIR = '/home/enso/noaa/wave'

try:
    lats_lons = pickle.load(open('lats_lons.pkl','rb'))
    LATS,LONS = [lats_lons.get(i) for i in ('lats','lons')]
    POINTS = [[LONS[i],LATS[i]] for i in range(len(LATS))]
    # POINTS = np.loadtxt('points.txt')
    points_in_region_TrueFalseS = pickle.load(open('points_in_region_TrueFalseS.pkl','rb'))
except:
    print('!!! No pkl found !!!')


OUTPUT_DIR = '/home/enso/SeaService_output'
