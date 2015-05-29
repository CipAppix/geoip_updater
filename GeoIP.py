#!/usr/bin/env python

import os
import urllib2
import sys
import gzip

# Check if GeoIP is install
if not os.access('/usr/share/GeoIP/', os.F_OK):
    print("*" * 46)
    print("You don't have GeoIP installed on your machine")
    print("Please, first install it")
    print("*" * 46)
    sys.exit()

# Change directory to GeoIP
os.chdir('/usr/share/GeoIP')

# Define URL to files
urls = ["http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz",
        "http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz",
        "http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz",
        "http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz",
        "http://geolite.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz",
        "http://geolite.maxmind.com/download/geoip/database/asnum/GeoIPASNumv6.dat.gz"]

# Download the files from URL
for url in urls:
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()

# Read compressed file
    inF = gzip.GzipFile(file_name, 'rb')
    s = inF.read()
    inF.close()

# Decompress compressed file
    new_file = file_name.split('.')[-3] + "." + file_name.split('.')[-2]
    outF = file(new_file, 'wb')
    outF.write(s)
    outF.close()

# Delete a compressed file
    os.remove(file_name)
