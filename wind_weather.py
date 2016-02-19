# coding:utf8

from config import *


WIND_DIRECT = {
	'N':[337.5,22.5],
	'NE':[22.5,67.5],
	'E':[67.5,112.5],
	'SE':[112.5,157.5],
	'S':[157.5,202.5],
	'SW':[202.5,247.5],
	'W':[247.5,292.5],
	'NW':[292.5,223.7]
}

WIND_DIRECT_CODE = {
	0:"C",
	1:"NE",
	2:"E",
	3:"SE",
	4:"S",
	5:"SW",
	6:"W",
	7:"NW",
	8:"N",
	9:"Whirl",
	-1:"Unknown"
}

WEATHER_TYPE_CODE = {
	99:'Unknown',
	0:'Sunny',
	1:'Cloudy',
	2:'Overcast',
	18:'Foggy',
	903:'Rain',
	913:'Snow'
}


def dgree2direction(wd):
	if 0<wd<=22.5 or 337.5<wd<=360:
		wd = 8    # N
	elif 22.5<wd<=67.5:
		wd = 1    # NE
	elif 67.5<wd<=112.5:
		wd = 2    # E
	elif 112.5<wd<=157.5:
		wd = 3    # SE
	elif 157.5<wd<=202.5:
		wd = 4    # S
	elif 202.5<wd<=247.5:
		wd = 5    # SW
	elif 247.5<wd<=292.5:
		wd = 6    # W
	elif 292.5<wd<=337.5:
		wd = 7    # NW
	return wd


def uv2wswd(u,v):
	'''
		INPUTS:
			u,v units in m/s
		OUTPUTS:
			ws in term of wind speed, units in m/s
			wd in term of wind direction, in int code
	'''
	try:
		ws = round(np.sqrt(u*u + v*v),1)
		if ws:
			if v > 0:
				wd = round(np.asin(u/ws)/np.pi*180, 1)
			else:
				wd = round(180-np.asin(u/ws)/np.pi*180, 1)
			if wd < 0:
				wd += 360
			if wd > 360:
				wd -= 360
			wd = dgree2direction(wd) # wind direction
		else:
			wd = 0 # No wind and No wind direction
	except:
		ws = wd = -1 # Unknown
	return ws,wd


def weather_type(rainfall, snowfall, cloud, visiability):
	'''
		INPUTS:
			raingfall and snowfall units in mm
			cloud means cloud fraction
			visibility units in km
		OUTPUTS:
			wt in priority of Snow,Rain,Frog,Sunny/Cloudy/Overcast, in int code
	'''
	try:
		if rainfall or snowfall:
			if snowfall >= 0.5*rainfall:
				wt = 913  # Snow
			else:
				wt = 903  # Rain
		else:
			if cloud<0.4:
				wt = 0    # Sunny
			elif 0.4<=cloud<0.8:
				wt = 1    # Cloudy
			else:
				wt = 2    # Overcast
			if visiability<1:
				wt = 18   # Foggy
	except:
		wt = 99           # Unknown
	return wt

