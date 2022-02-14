import os
import glob
import pandas as pd
import subprocess
import obspy
from obspy import read
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from matplotlib import pyplot as plt
import re
from sac2asc import sac2asc
from obspy.io.sac import SACTrace


################################# get waveforms ####################################################

# client = Client("IRIS")
# t1 = UTCDateTime("2016-10-27T06:30:00.000")
# t2 = t1+5
# st = client.get_waveforms("MM", "HKA", "*", "HN*", t1, t2)
# print(st)
# print(st[0].stats.station)  

# inventory = client.get_stations(network="MM", station=st[0].stats.station,
#                                 starttime=t1,
#                                 endtime=t2)
# print(inventory[0][0].longitude)  
# print(inventory[0][0].latitude) 

################################## get events #####################################################

# t1 = UTCDateTime("2021-01-02T00:00:00")
# tt2 = UTCDateTime("2021-03-10T00:00:00")
# minlat = 10
# maxlat = 30
# minlng = 90
# maxlng = 102
# counts = 0
# client = Client("IRIS")

# #抓地震事件
# cats = client.get_events(starttime=t1, endtime=tt2, minmagnitude=4, minlatitude=minlat, maxlatitude=maxlat, minlongitude=minlng, maxlongitude=maxlng)

# for i in cats[0]:
#     print(i)

################################# read mseed ######################################################

# import glob
# from obspy.core import read
# for file in glob.glob('*.mseed'):
#     st = read(file)
#     for i in range(len(st)):
#         tr = st[i]
#         msg = "%s converted to %s.%s.%s.sac" % (str(file), tr.stats.station, tr.stats.channel, str(file)[9:18])
#         fname = "%s.%s.%s.sac" % (tr.stats.station, tr.stats.channel, str(file)[9:18])
#         tr.write(fname, format="SAC")
#         print(msg)