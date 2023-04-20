#算所有的events中有幾個非mb類型的地震
#定義地震範圍等變數
import glob 
from obspy import read
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import pandas as pd
import backoff
import requests

tt1 = UTCDateTime("2021-01-01T00:00:00")
tt2 = UTCDateTime("2021-12-31T00:00:00")
minlat = 10
maxlat = 30
minlng = 90
maxlng = 102
counts = 0
client = Client("IRIS")

#抓地震事件
cats = client.get_events(starttime=tt1, endtime=tt2, minmagnitude=5.5, minlatitude=minlat, maxlatitude=maxlat, minlongitude=minlng, maxlongitude=maxlng)

#跑迴圈列出每個event的屬性
for cat in cats:
    if cat.magnitudes[0].magnitude_type != 'mb':
        counts +=1
        print('cat.origins[0].depth', cat.origins[0].depth) #unit: meter
        print('cat.origins[0].depth_type', cat.origins[0].depth_type)
        print('cat.origins[0].arrivals', cat.origins[0].arrivals)
        print('cat.magnitudes[0].magnitude_type', cat.magnitudes[0].magnitude_type)
        print(cat.focal_mechanisms)
print(counts)

#抓2016-2021資料儲存為mseed，90-102E / 10-30N

import glob 
from obspy import read
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import pandas as pd
import backoff
import requests

#抓取events的初始設定
t1 = UTCDateTime("2021-01-01T00:00:00")
t2 = UTCDateTime("2021-12-31T00:00:00")
minlat = 10
maxlat = 30
minlng = 90
maxlng = 102
df = pd.DataFrame(columns=['longitude','latitude','depth','Otime','magnitude','magnitude_type','event_id','filName'])
row_dict = {}
client = Client("IRIS")

#用@backoff抓執行過程中遇到的錯誤，避免遇到exception直接跳掉
#以originTime下載波形
@backoff.on_exception(backoff.expo,
                    (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError))
def donwloadWaveform(t1):
    return client.get_waveforms("MM", "*","*", "HN*", t1, t1+360,attach_response=True)
# p_arrival-20 s_arrival+120

#用@backoff抓執行過程中遇到的錯誤，避免遇到exception直接跳掉
#下載列表
@backoff.on_exception(backoff.expo,
                    requests.exceptions.ConnectionError)
def donwloadEventList(t1, t2, minlat, maxlat, minlng, maxlng):
    return client.get_events(starttime=t1, endtime=t2, minmagnitude=5.5, minlatitude=minlat, maxlatitude=maxlat, minlongitude=minlng, maxlongitude=maxlng)

#抓事件列表
cats = donwloadEventList(t1, t2, minlat, maxlat, minlng, maxlng)


#印出每個event的屬性，並分別儲存到mseed檔案、檔案列表
for i,cat in enumerate(cats):
    #印出每個event需要的屬性
    print('processing event: ', str(cat.resource_id).split('=')[-1])
    print('cat.origins[0].longitude', cat.origins[0].longitude)
    print('cat.origins[0].latitude', cat.origins[0].latitude)
    print('cat.origins[0].depth', cat.origins[0].depth) #unit: meter
    print('cat.origins[0].time', cat.origins[0].time)
    print('cat.magnitudes[0]', cat.magnitudes[0].mag)
    print('cat.magnitudes[0].magnitude_type', cat.magnitudes[0].magnitude_type)
    print('cat.resource_id', cat.resource_id)
    print('cat.resource_id', str(cat.resource_id).split('=')[-1])
    
    #另存屬性為變數方便使用
    event_id = str(cat.resource_id).split('=')[-1]
    t1 = cat.origins[0].time
    newfile = f'MM_{str(t1)}_{event_id}_RespRemoved.mseed'
    
    #另存屬性到dataframe
    df['longitude'].loc[i] = cat.origins[0].longitude
    df['latitude'].loc[i] = cat.origins[0].latitude
    df['depth'].loc[i] = cat.origins[0].depth
    df['Otime'].loc[i] = cat.origins[0].time
    df['magnitude'].loc[i] = cat.origins[0].time
    df['magnitude_type'].loc[i] = cat.magnitudes[0].magnitude_type
    df['event_id'].loc[i] = event_id
    df['filName'].loc[i] = newfile
    
    #用originTime抓waveform
    st = donwloadWaveform(t1) 
    
    #印出Log來看
    print(f'writing traces to file: {newfile}')
    print(st)
    
    #寫入mseed檔案
    st.write('MM_events_20160101-20211026/'+newfile)  
    print('===')
#儲存整筆事件列表
df.to_csv('./MM_events_20160101-20211026/MM_events_20160101-20211026.csv')

#把mseed另存為sac檔案格式
#已有固定.mseed檔案
#再包一層loop就可以針對每一個mseed檔案另存
import glob 
from obspy import read
for mfile in glob.glob("MM_11484753_response_removed.mseed"):
    for (i, tr) in enumerate(read(mfile)):
        #print(tr,'.mseed', "{}.sac".format(i))
        newfile = mfile.replace('MM',st.traces[i].id)
        tr.write(newfile.replace('.mseed', ".sac"))