import mysql.connector
from mysql.connector import errorcode
import urllib2, cookielib, json
import time
import datetime
import string
import random
import math
import os as sys
lat = 46.066326
lon = 11.155522
ray = 30
delay = 10
config = {
  'user': 'flight',
  'password': 'hof5gisAbuqE',
  'host': 'localhost',
  'database': 'flight',
  'raise_on_warnings': True
}
def password_generator(size=12, chars=string.ascii_letters + string.digits):
    return (''.join(random.choice(chars) for i in range(size))).upper()
batch = password_generator()
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
def measure(lat1, lon1, lat2, lon2):
	R = 6378.137
	dLat = lat2 * math.pi / 180.0 - lat1 * math.pi / 180.0
	dLon = lon2 * math.pi / 180.0 - lon1 * math.pi / 180.0
	a = math.sin(dLat/2.0) * math.sin(dLat/2.0) + math.cos(lat1 * math.pi / 180.0) * math.cos(lat2 * math.pi / 180.0) * math.sin(dLon/2.0) * math.sin(dLon/2.0);
	c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c;
	return d;
counter = 1
go = True
while(go):
	try:
		ts = time.time()
		dddd = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		site = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=" + str(lat) + "&lng=" + str(lon) + "&fDstL=0&fDstU=" + str(ray)
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		       'Accept-Encoding': 'none',
		       'Accept-Language': 'en-US,en;q=0.8',
		       'Connection': 'keep-alive'}
		req = urllib2.Request(site, headers=hdr)
		page = urllib2.urlopen(req)
		content = page.read()
		content = content.replace("true", "True")
		content = content.replace("false", "False")
		tmp = eval(content)
		if("acList" in tmp):
			nplane = len(tmp["acList"])
			if(len(tmp["acList"]) > 0):
				toInsert = []
				for plane in tmp["acList"]:
					if("Alt" in plane):
						f_Alt = plane["Alt"]
					else:
						f_Alt = None
					if("AltT" in plane):
						f_AltT = plane["AltT"]
					else:
						f_AltT = None
					if("Bad" in plane):
						if(plane["Bad"]):
							f_Bad = 1
						else:
							f_Bad = 0
					else:
						f_Bad = None
					if("Brng" in plane):
						f_Brng = plane["Brng"]
					else:
						f_Brng = None
					if("CallSus" in plane):
						if(plane["CallSus"]):
							f_CallSus = 1
						else:
							f_CallSus = 0
					else:
						f_CallSus = None
					if("CMsgs" in plane):
						f_CMsgs = plane["CMsgs"]
					else:
						f_CMsgs = None
					if("Cou" in plane):
						f_Cou = plane["Cou"]
					else:
						f_Cou = None
					if("Dst" in plane):
						f_Dst = plane["Dst"]
					else:
						f_Dst = None
					if("EngMount" in plane):
						f_EngMount = plane["EngMount"]
					else:
						f_EngMount = None
					if("EngType" in plane):
						f_EngType = plane["EngType"]
					else:
						f_EngType = None
					if("FlightsCount" in plane):
						f_FlightsCount = plane["FlightsCount"]
					else:
						f_FlightsCount = None
					if("FSeen" in plane):
						ts = str(plane["FSeen"])
						ts = ts.replace("\/Date(", "")
						ts = ts.replace(")\/", "")
						timestamp = datetime.datetime.fromtimestamp(float(ts)/1000.0).strftime('%Y-%m-%d %H:%M:%S')
						f_FSeen = timestamp
					else:
						f_FSeen = None
					if("GAlt" in plane):
						f_GAlt = plane["GAlt"]
					else:
						f_GAlt = None
					if("HasPic" in plane):
						if(plane["HasPic"]):
							f_HasPic = 1
						else:
							f_HasPic = 0
					else:
						f_HasPic = None
					if("HasSig" in plane):			
						if(plane["HasSig"]):
							f_HasSig = 1
						else:
							f_HasSig = 0
					else:
						f_HasSig = None
					if("Icao" in plane):
						f_Icao = plane["Icao"]
					else:
						f_Icao = None
					if("Id" in plane):
						f_id = plane["Id"]
					else:
						f_id = None
					if("InHg" in plane):
						f_InHg = plane["InHg"]
					else:
						f_InHg = None
					if("Interested" in plane):	
						if(plane["Interested"]):
							f_Interested = 1
						else:
							f_Interested = 0
					else:
						f_Interested = "Interested"
					if("Lat" in plane):
						f_Lat = plane["Lat"]
					else:
						f_Lat = None
					if("Long" in plane):
						f_Long = plane["Long"]
					else:
						f_Long = None
					if("Mil" in plane):
						if(plane["Mil"]):
							f_Mil = 1
						else:
							f_Mil = 0
					else:
						f_Mil = None
					if("Mlat" in plane):
						if(plane["Mlat"]):
							f_Mlat = 1
						else:
							f_Mlat = 0
					else:
						f_Mlat = None
					if("PosTime" in plane):
						ts = str(plane["PosTime"])
						ts = ts.replace("\/Date(", "")
						ts = ts.replace(")\/", "")
						timestamp = datetime.datetime.fromtimestamp(float(ts)/1000.0).strftime('%Y-%m-%d %H:%M:%S')
						f_PosTime = timestamp
					else:
						f_PosTime = None
					if("Rcvr" in plane):
						f_Rcvr = plane["Rcvr"]
					else:
						f_Rcvr = None
					if("Spd" in plane):
						f_Spd = plane["Spd"]
					else:
						f_Spd = None
					if("SpdTyp" in plane):
						f_SpdTyp = plane["SpdTyp"]
					else:
						f_SpdTyp = None
					if("Species" in plane):
						f_Species = plane["Species"]
					else:
						f_Species = None
					if("Sqk" in plane):
						if(len(plane["Sqk"]) == 0):
							f_Sqk = None
						else:
							f_Sqk = plane["Sqk"]
					else:
						f_Sqk = None
					if("Tisb" in plane):
						if(plane["Tisb"]):
							f_Tisb = 1
						else:
							f_Tisb = 0
					else:
						f_Tisb = None
					if("Trak" in plane):
						f_Trak = plane["Trak"]
					else:
						f_Trak = None
					if("TrkH" in plane):
						if(plane["TrkH"]):
							f_TrkH = 1
						else:
							f_TrkH = 0
					else:
						f_TrkH = None
					if("Trt" in plane):
						f_Trt = plane["Trt"]
					else:
						f_Trt = None
					if("TSecs" in plane):
						f_TSecs = plane["TSecs"]
					else:
						f_TSecs = None
					if("Vsi" in plane):
						f_Vsi = plane["Vsi"]
					else:
						f_Vsi = None
					if("VsiT" in plane):
						f_VsiT = plane["VsiT"]
					else:
						f_VsiT = None
					if("WTC" in plane):
						f_WTC = plane["WTC"]
					else:
						f_WTC = None					
					toInsert.append((lat, lon, ray, batch, nplane, dddd, f_id, f_Alt, f_AltT, f_Bad, f_Brng, f_CallSus, f_CMsgs, f_Cou, f_Dst, f_EngMount, f_EngType, f_FlightsCount, f_FSeen, f_GAlt, f_HasPic, f_HasSig, f_Icao, f_InHg, f_Interested, f_Lat, f_Long, f_Mil, f_Mlat, f_PosTime, f_Rcvr, f_Spd, f_SpdTyp, f_Species, f_Sqk, f_Tisb, f_Trak, f_TrkH, f_Trt, f_TSecs, f_Vsi, f_VsiT, f_WTC))					
				sql = "INSERT INTO flightdata (Latitude, Longitude, Ray, Batch, NPlane, Time, ID, Alt, AltT, Bad, Brng, CallSus, CMsgs, Cou, Dst, EngMount, EngType, FlightsCount, FSeen, GAlt, HasPic, HasSig, Icao, InHg, Interested, Lat, Longt, Mil, Mlat, PosTime, Rcvr, Spd, SpdTyp, Species, Sqk, Tisb, Trak, TrkH, Trt, TSecs, Vsi, VsiT, WTC) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				for x in toInsert:
					cursor.execute(sql, x)
				cnx.commit()
			else:
				x = ((lat, lon, ray, batch, 0, dddd, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
				sql = "INSERT INTO flightdata (Latitude, Longitude, Ray, Batch, NPlane, Time, ID, Alt, AltT, Bad, Brng, CallSus, CMsgs, Cou, Dst, EngMount, EngType, FlightsCount, FSeen, GAlt, HasPic, HasSig, Icao, InHg, Interested, Lat, Longt, Mil, Mlat, PosTime, Rcvr, Spd, SpdTyp, Species, Sqk, Tisb, Trak, TrkH, Trt, TSecs, Vsi, VsiT, WTC) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, x)
				cnx.commit()
		else:
			x = ((lat, lon, ray, batch, 0, dddd, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
			sql = "INSERT INTO flightdata (Latitude, Longitude, Ray, Batch, NPlane, Time, ID, Alt, AltT, Bad, Brng, CallSus, CMsgs, Cou, Dst, EngMount, EngType, FlightsCount, FSeen, GAlt, HasPic, HasSig, Icao, InHg, Interested, Lat, Longt, Mil, Mlat, PosTime, Rcvr, Spd, SpdTyp, Species, Sqk, Tisb, Trak, TrkH, Trt, TSecs, Vsi, VsiT, WTC) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, x)
			cnx.commit()
		print(str(counter) + " - Fatto")
		counter = counter + 1
		time.sleep(delay)
	except KeyboardInterrupt:
		print("Ending...")
		go = False