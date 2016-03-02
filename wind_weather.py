# coding:utf8

from config import *


WIND_DIRECT = {
	'NE':[22.5,67.5],
	'E':[67.5,112.5],
	'SE':[112.5,157.5],
	'S':[157.5,202.5],
	'SW':[202.5,247.5],
	'W':[247.5,292.5],
	'NW':[292.5,337.5],
	'N':[337.5,22.5]
}

WIND_DIRECT_CODE = {
	1:"NE",
	2:"E",
	3:"SE",
	4:"S",
	5:"SW",
	6:"W",
	7:"NW",
	8:"N",
	9:"Whirl",
	0:"C",
	-1:"Unknown"
}

WEATHER_TYPE_CODE = {
	0:'Sunny',
	1:'Cloudy',
	2:'Overcast',
	3:'Shower',
	4:'Thundershower',
	5:'Thundershower with hail',
	6:'Sleet',
	7:'Light rain',
	8:'Moderate rain',
	9:'Heavy rain',
	10:'Storm',
	11:'Heavy storm',
	12:'Severe storm',
	13:'Snow flurry',
	14:'Light snow',
	15:'Moderate snow',
	16:'Heavy snow',
	17:'Snowstorm',
	18:'Foggy',
	19:'Ice rain',
	20:'Duststorm',
	21:'Light to moderate rain',
	22:'Moderate to heavy rain',
	23:'Heavy rain to storm',
	24:'Storm to heavy storm',
	25:'Heavy to severe storm',
	26:'Light to moderate snow',
	27:'Moderate to heavy snow',
	28:'Heavy snow to snowstorm',
	29:'Dust',
	30:'Sand',
	31:'Sandstorm',
	53:'Haze',
	99:'Unknown',
	903:'Rain',
	913:'Snow',
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
				wd = round(180 + np.arcsin(u/ws)/np.pi*180, 1)
			else:
				wd = round(360 - np.arcsin(u/ws)/np.pi*180, 1)
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


def weather_type(rainfall, snowfall, cloud, visibility):
	'''
		INPUTS:
			raingfall and snowfall units in mm
			cloud means cloud fraction
			visibility units in m
		OUTPUTS:
			wt in priority of Snow,Rain,Frog,Sunny/Cloudy/Overcast, in int code
	'''
	try:
		if rainfall < 0.1:
			if visibility < 1000:
				wt = 18
			else:
				if cloud < 0.4:
					wt = 0
				elif 0.4 <= cloud < 0.8:
					wt = 1
				else:
					wt = 2

		elif 0.1 <= rainfall <= 2.9:
			wt = 7
			if 0 < snowfall <= 0.4 and snowfall < 0.5*rain:
				wt = 6
			elif 0 < snowfall <= 0.4 and snowfall >= 0.5*rain:
				wt = 14
			elif 0.4 < snowfall <= 1.4:
				wt = 15
			elif 1.4 < snowfall <= 2.9:
				wt = 16

		elif 2.9 < rainfall <= 9.9:
			wt = 8
			if 0.4 < snowfall <= 1.4:
				wt = 15
			elif 1.4 < snowfall <= 2.9:
				wt = 16
			elif 2.9 < snowfall <= 5.9:
				wt = 17

		elif 9.9 < rainfall <= 19.9:
			wt = 9
			if 1.4 < snowfall <= 2.9:
				wt = 16
			elif 2.9 < snowfall <= 5.9:
				wt = 17

		elif 19.9 < rainfall <= 49.9:
			wt = 10
			if 2.9 < snowfall <= 5.9:
				wt = 17

		elif 49.9 < rainfall <= 69.9:
			wt = 11

		elif rainfall > 69.9:
			wt = 12

	except:
		wt = 99           # Unknown
	return wt


if __name__ == '__main__':
	print uv2wswd(-0.0,1)
