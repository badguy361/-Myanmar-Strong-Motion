from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy.geodetics.base import gps2dist_azimuth, kilometer2degrees
import pandas as pd
from tqdm import tqdm
from obspy import read
from obspy import UTCDateTime
import backoff
import requests
import os
from http.client import IncompleteRead

catlog = pd.read_csv("/home/joey/緬甸BH_ubuntu/merge_event_eq.csv")

# TODO
# 抓取events的初始設定
year=2017
start_mon="01"
end_mon="12"
for mon in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
    sac_path = f"/home/joey/緬甸BH_ubuntu/dataset/MM_new_events_20160101-20211026/{year}/{mon}/"
    if not os.path.isdir(sac_path):
        os.mkdir(sac_path)
t1 = UTCDateTime(f"2016-{start_mon}-01T00:00:00")
t2 = UTCDateTime(f"2016-{end_mon}-01T00:00:00")
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
    return client.get_waveforms("MM", f"{sta}","*", "HN*", p_arrival-50, s_arrival+300,attach_response=True)
# p_arrival-20 s_arrival+120



for i in tqdm([981,996,1011,1044]):# merge_event_eq.csv -> event_id
    try:
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
        st[0].write(f'dataset/MM_new_events_20160101-20211026/{year}/12/'+newfile_E)
        st[1].write(f'dataset/MM_new_events_20160101-20211026/{year}/12/'+newfile_N)
        st[2].write(f'dataset/MM_new_events_20160101-20211026/{year}/12/'+newfile_Z)  
    except IncompleteRead:
        # Oh well, reconnect and keep trucking
        continue

# import shutil
# import glob
# target_mon="12"
# original = glob.glob(f'dataset/MM_new_events_20160101-20211026/{year}/{start_mon}/*2017{target_mon}*')
# target = f'dataset/MM_new_events_20160101-20211026/{year}/{target_mon}/'

# for i in original:
#     shutil.move(i,target)

# import os 
# a = os.listdir("dataset/MM_new_events_20160101-20211026/2017/10")
# b = os.listdir("dataset/MM_2016-2021/2017/10")