# coding:utf8

'''
	Work on 192.168.2.127

	cmacast on 192.168.2.125 mounted on 127, i.e.
		//192.168.2.125/cmacast on /mnt/cmacast

	ECMWF data on path:
		/mnt/cmacast/NWP_MCTR_002/ECMF_DAM/PUB/
'''

import os
import numpy as np
import pygrib
from collections import OrderedDict
from datetime import datetime,date,timedelta

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
    'MN2T6':'Minimum temperature at 2 metres since last 6 hours',
    'MX2T6':'Maximum temperature at 2 metres since last 6 hours',
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
    'LSP':'Large-scale precipitation', # Stratiform precipitation
    'CP':'Convective precipitation',
    'CAPE':'Convective available potential energy',
    # snow
    'SD':'Snow depth',
    'SF':'Snowfall',
    'RSN':'Snow density',
    # albedo
    'FAL':'Forecast albedo',
}

Nlon,Xlon,Nlat,Xlat = 105,130,2,41

