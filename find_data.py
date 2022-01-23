from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy.geodetics.base import gps2dist_azimuth, kilometer2degrees
from obspy.taup import TauPyModel
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import glob 
from obspy import read
from obspy import UTCDateTime
import backoff
import requests
import re

catlog = pd.read_csv("/home/joey/緬甸BH_ubuntu/merge_event_eq.csv")

################################# save iasp91 #################################
# iasp91_P_arrival = []
# iasp91_S_arrival = []
# for i in tqdm(range(catlog.shape[0])):
#     try:
#         model = TauPyModel(model='iasp91') #jb pwdk can run 
#         dist = kilometer2degrees(catlog["dist_surface"][i]) #55 #675 #special:543 
#         depth = catlog["origins.depth"][i]/1000 #83 #55.15 #special:20 
#         arrivals = model.get_travel_times\
#             (source_depth_in_km=depth, distance_in_degree=dist,\
#             phase_list=["P","S",'p','s'])
#         iasp91_P_arrival.append(arrivals[0].time)
#         iasp91_S_arrival.append(arrivals[-1].time)
#     except:
#         iasp91_P_arrival.append("NA")
#         iasp91_S_arrival.append("NA")
        
# catlog["iasp91_P_arrival"] = iasp91_P_arrival
# catlog["iasp91_S_arrival"] = iasp91_S_arrival
# catlog.to_csv("merge_event_eq.csv",index=False,mode='w')

################################# save iasp91 #################################

#抓取events的初始設定
t1 = UTCDateTime("2016-05-01T00:00:00")
t2 = UTCDateTime("2016-06-01T00:00:00")
minlat = 10
maxlat = 30
minlng = 90
maxlng = 102
client = Client("IRIS")

#用@backoff抓執行過程中遇到的錯誤，避免遇到exception直接跳掉
#以originTime下載波形
@backoff.on_exception(backoff.expo,
                    (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError))
def donwloadWaveform(p_arrival,s_arrival,sta):
    return client.get_waveforms("MM", f"{sta}","*", "HN*", p_arrival-20, s_arrival+120,attach_response=True)
# p_arrival-20 s_arrival+120


for i in tqdm(range(44)):
    p_arrival = catlog["iasp91_P_arrival"][i] 
    s_arrival = catlog["iasp91_S_arrival"][i] 
    newfile_E = catlog["file_name"][i]
    newfile_N = newfile_E.replace("HNE","HNN")
    newfile_Z = newfile_E.replace("HNE","HNZ")
    sta = catlog["file_name"][i].split("_")[1]
    sta_get_time = UTCDateTime(catlog["sta_get_time"][i])
    # print(p_arrival,s_arrnnival,newfile)
    st = donwloadWaveform(sta_get_time+p_arrival,sta_get_time+s_arrival,sta)
    # st.plot()
    st[0].write('dataset/MM_mseed/MM_new_events_20160101-20211026/2016/05_new/'+newfile_E)
    st[1].write('dataset/MM_mseed/MM_new_events_20160101-20211026/2016/05_new/'+newfile_N)
    st[2].write('dataset/MM_mseed/MM_new_events_20160101-20211026/2016/05_new/'+newfile_Z)
  

############################ test ################################
# # first
# model = TauPyModel(model='iasp91') #jb pwdk can run 
# dist = kilometer2degrees(55) #55 #675 #special:543 
# depth = 83 #83 #55.15 #special:20 
# arrivals = model.get_travel_times\
#     (source_depth_in_km=depth, distance_in_degree=dist,\
#     phase_list=["P","S",'p','s'])
# print(arrivals[0].time)
# print(arrivals[-1].time)
# print(arrivals)

# client = Client("IRIS")
# t1 = UTCDateTime("2020-05-05T22:15:04.088000") # 2020-05-05T22:15:04.088000 # 2020-05-25T14:42:17.178000
# t2 = t1 +360
# st = client.get_waveforms("MM", "NGU", "*", "HNE", t1, t2,attach_response=True)
#     #NGU # KTN
# st.plot()
# plt.plot(st[0].times(),st[0].data)
# plt.plot([arrivals[0].time, arrivals[0].time], \
#     [-23100, -22350],color="red",linestyle= '--',\
#     label="iasp91") #23100,22350
# plt.plot([arrivals[-1].time, arrivals[-1].time], \
#     [-23100, -22350],color="red",linestyle= '--')
# plt.plot([22.25, 22.25], \
#     [-23100, -22350],color="black",linestyle= '--',\
#     label="ori") #22.25 #150.6
# plt.plot([33.3, 33.3],\
#     [-23100, -22350],color="black",linestyle= '--')
#     #33.3 #226
# plt.legend()


# # second
# model = TauPyModel(model='iasp91') #jb pwdk can run 
# dist = kilometer2degrees(675) #55 #675 #special:543 
# depth = 55.15 #83 #55.15 #special:20 
# arrivals = model.get_travel_times\
#     (source_depth_in_km=depth, distance_in_degree=dist,\
#     phase_list=["P","S",'p','s'])
# print(arrivals[0].time)
# print(arrivals[-1].time)
# print(arrivals)

# client = Client("IRIS")
# t1 = UTCDateTime("2020-05-25T14:42:17.178000") # 2020-05-05T22:15:04.088000 # 2020-05-25T14:42:17.178000
# t2 = t1 +360
# st = client.get_waveforms("MM", "KTN", "*", "HNE", t1, t2,attach_response=True)
#     #NGU # KTN
# st.plot()
# plt.plot(st[0].times(),st[0].data)
# plt.plot([arrivals[0].time, arrivals[0].time], \
#     [-49000, -53000],color="red",linestyle= '--',\
#     label="iasp91") #23100,22350
# plt.plot([arrivals[-1].time, arrivals[-1].time], \
#     [-49000, -53000],color="red",linestyle= '--')
# plt.plot([150.6, 150.6], \
#     [-49000, -53000],color="black",linestyle= '--',\
#     label="ori") #22.25 #150.6 
# plt.plot([226, 226],\
#     [-49000, -53000],color="black",linestyle= '--')
#     #33.3 #226
# plt.legend()

############################ test ################################