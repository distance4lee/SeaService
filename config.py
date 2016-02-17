# coding:utf8

'''
	Work on 192.168.2.127

	cmacast on 192.168.2.125 mounted on 127, i.e.
		//192.168.2.125/cmacast on /mnt/cmacast

	ECMWF data on path:
		/mnt/cmacast/NWP_MCTR_002/ECMF_DAM/PUB/
'''

import os
from datetime import datetime,date,timedelta
import pygrib


CMACAST_DIR = '/mnt/cmacast'
ECMWF_DIR = 'NWP_MCTR_002/ECMF_DAM/PUB/'

ECMWF_FULLPATH = os.path.join(CMACAST_DIR,ECMWF_DIR)

