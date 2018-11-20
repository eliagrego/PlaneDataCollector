import mysql.connector
from mysql.connector import errorcode
import urllib2, cookielib, json
import time
import datetime

lat = 46.066974
lon = 11.150047
ray = 30

delay = 60

config = {
  'user': 'flight',
  'password': 'hof5gisAbuqE',
  'host': 'localhost',
  'database': 'flight',
  'raise_on_warnings': True
}

try:

	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()

	#query = "SELECT * FROM test"
	#cursor.execute(query)

	try:

		counter = 1

		while(True):

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

			x = []

			ts = time.time()
			timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

			nplane = len(tmp["acList"])
			if(nplane > 0):
				for fn in tmp["acList"]:
					keyforflight = fn.keys()
					for mykey in keyforflight:
						valido = True
						for coppia in x:
							if(coppia[0] == mykey):
								valido = False
								coppia[1] = coppia[1] + 1
						if(valido):
							x.append([mykey, 1])
				val = []
				for [a, b] in x:
					val.append((a, b, timestamp, nplane, lat, lon, ray))
				sql = "INSERT INTO fieldstat (Name, Value, TS, NPlane, Lat, Lon, Ray) VALUES (%s, %s, %s, %s, %s, %s, %s)"
				for x in val:
					cursor.execute(sql, x)
				cnx.commit()

			else:
				sql = "INSERT INTO fieldstat (Name, Value, TS, NPlane, Lat, Lon, Ray) VALUES (%s, %s, %s, %s, %s, %s, %s)"	
				cursor.execute(sql, ("Zero", 0, timestamp, 0, lat, lon, ray))
				cnx.commit()			

			print str(counter) + ") - Fatto"
			counter = counter + 1
			time.sleep(delay)

	except urllib2.HTTPError, e:
	    print e.fp.read()

	#print("Fatto")
	#result = cursor.fetchall()
	#for i in result:
	#	print i

	#cursor.close()
	#cnx.close()

except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cnx.close()
