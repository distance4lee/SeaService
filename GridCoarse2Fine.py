#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''Simple
@author: Li Jiapeng <distance4lee@gmail.com>
@license: LGPLv3+
'''

import os
import sys
import numpy as np
import pygrib
from datetime import date,datetime,timedelta
from scipy.interpolate import griddata

class GridCoarse2Fine(object):

	def __init__( self,  DesLons, DesLone, DesLats, DesLate, DesDxy ):

		self.__lons = np.arange( DesLons, DesLone+DesDxy, DesDxy )
		self.__lats = np.arange( DesLats, DesLate+DesDxy, DesDxy )
		self.__grid_lons, self.__grid_lats = np.meshgrid(self.__lons,self.__lats)

	def GrbDataLoader( self, FileName, VarName, Fh, Lev ):
		
		try:
			print 'Processing Forecast Time: ', Fh
			grbfile = pygrib.open(FileName)
			data = grbfile.select(name=VarName, forecastTime=Fh, level=Lev)[0]
			lats,lons = data.latlons()
			lats = lats.reshape(lats.shape[0]*lats.shape[1],1)
			lons = lons.reshape(lons.shape[0]*lons.shape[1],1)
			self.__data = data.values.reshape(data.values.shape[0]*data.values.shape[1],1)
			self.__coord = np.hstack((lons, lats))
		except:
			print 'MISSING FILE: ', FileName
			pass

	def Coarse2Fine( self, FileName, VarName, Fh, Lev = 0 ):
		
		try:
			self.GrbDataLoader( FileName, VarName, Fh, Lev )
			DesData = griddata( self.__coord, self.__data, (self.__grid_lons, self.__grid_lats), method='cubic')
		except:
			DesData = np.ones(self.__lons.shape[0]*self.__lats.shape[0]).reshape(self.__lats.shape[0], self.__lons.shape[0],1)*-999.0
			pass

		return DesData, self.__grid_lons, self.__grid_lats

def GetOutFname( varname, dtInit, fh ):
	outdir = '/home/enso/noaa/output/'
	dtFcst = dtInit + timedelta(fh)
	fname = 'enso.%s.I%s.%s.F%s.dat' % ( varname, dtInit.strftime('%Y%m%d%H'), str(fh).zfill(3), dtFcst.strftime('%Y%m%d%H'))

	return fname
	
def usage():
	print '-----------------------------------------------'
	print 'usage:                                         '
	print '      python GridCoarse2Fine.py yyyymmddHH [UTC]'
	print '                                               '
	print '-----------------------------------------------'
	
if __name__ == '__main__':
	
	try:
		dt = sys.argv[1]
	except:
		usage()
		exit()
	
	print 'Processing Time: ', dt

	dtInit = datetime.strptime( dt, '%Y%m%d%H' )
	OUTDIR = '/home/enso/noaa/output/'
	os.system('mkdir -p %s' % ( OUTDIR+dtInit.strftime('%Y%m%d%H') ))

	DATADIR = '/home/enso/noaa/visibility/'
	fn = 'enso_%s_fog.t%sz.gvisg.grib2' % ( dtInit.strftime('%Y%m%d'),dtInit.strftime('%H'))
	fn_fullpath = DATADIR + fn
	print fn_fullpath

	GridC2F = GridCoarse2Fine( 106, 128, 2, 42, 0.125 )

	for fh in range(3,75,3):
		fname = OUTDIR + dtInit.strftime('%Y%m%d%H') + '/' + GetOutFname( 'visibility', dtInit, fh )
		print fname
		Output, _, _ = GridC2F.Coarse2Fine( fn_fullpath, 'Visibility', fh, 10 )
		np.savetxt( fname, Output[:,:,0], fmt='%7.1f' )
