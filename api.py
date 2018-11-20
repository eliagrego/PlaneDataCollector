import urllib2, cookielib, json

lat = 46.066207
lon = 11.155460
ray = 100

try:
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

	y = []
	for [a, b] in x:
		y.append((a, b))

	print y

except urllib2.HTTPError, e:
    print e.fp.read()