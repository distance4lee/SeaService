def wd2category(wd):

	if( (wd > 0 and wd <=22.5) or ( wd > 337.5 and wd <= 360) ):
		wd = 0    #--North
	elif( wd > 22.5 and wd <= 67.5 ):
		wd = 1    #--Northeast
	elif( wd > 67.5 and wd <= 112.5 ):
		wd = 2    #--East
	elif( wd > 112.5 and wd <= 157.5 ):
		wd = 3    #--Southeast
	elif( wd > 157.5 and wd <= 202.5 ):
		wd = 4    #--South
	elif( wd > 202.5 and wd <= 247.5 ):
		wd = 5    #--Southwest
	elif( wd > 247.5 and wd <= 292.5 ):
		wd = 6    #--West
	elif( wd > 292.5 and wd <= 337.5 ):
		wd = 7    #--Northwest

	return wd

def code2char(ww,wd):

	WWDICT = {0:"晴",1:"多云",2:"阴",903:"雨",913:"雪"}
	WDDICT = {0:"北风",1:"东北风",2:"东风",3:"东南风",4:"南风",5:"西南风",6:"西风",7:"西北风"}
	try:
		wwchar = WWDICT.get(ww)
		wdchar = WDDICT.get(wd)
	except:
		wwchar = "缺省"
		wdchar = "缺省"

	return wwchar,wdchar

def uv2speed_direction(uu,vv):

	try:

		ws = round(math.sqrt( uu*uu + vv*vv ),1)    # Calculating wind speed
	
		if ( vv > 0 ):    # Calculating wind direction
			wd = round((math.asin(uu/ws)/math.pi * 180),1)
		else:
			wd = round((180 - math.asin(uu/ws)/math.pi * 180),1)

		if ( wd < 0 ):
			wd += 360
		if ( wd > 360 ):
			wd -= 360

		wd = wd2category(wd)
	except:
		ws = wd = -999

	return ws,wd

def IDWW(cloud, pr, sf):

	try:
		if ( pr == 0 ):
			if ( cloud < 0.4 ):
				ww = 0    #--Sunny
			elif ( cloud >= 0.4 and cloud < 0.8 ):
				ww = 1    #--Partly Cloudy
			else:
				ww = 2    #--Cloudy
		elif ( pr > 0.1 ):
			if ( sf >= 0.5*pr ):
				ww = 913    #--Snow
			else:
				ww = 903    #--Rain
	except:
		ww = -999

	return ww