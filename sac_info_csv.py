from obspy.io.sac import SACTrace
import os 
import glob
import pandas as pd
import re
pattern = "[a-zA-Z]+" 
time = []
sta = []
name = []
year = ["2016","2017","2018","2019","2020"]
for z in year:
    os.chdir(f"/home/joey/緬甸BH_ubuntu/dataset/MM_new_events_20160101-20211026/2017/01/") # total sac file
    sacfile = glob.glob("*HNE*")
    for i in sacfile:
        tmp = re.findall(pattern,i) # station_name
        print(tmp)
        sac1 = SACTrace.read(i)
        time.append(sac1.reftime)
        sta.append(tmp[1])
        name.append(i)
        
# df = pd.DataFrame(time,columns=["sta_get_time"])
# df["sta_name"] = pd.DataFrame(sta)
# df["file_name"] = pd.DataFrame(name)
# df = df.sort_values(by=["sta_get_time"],ignore_index=True)
# df.to_csv("/home/joey/緬甸BH_ubuntu/MM_sta_info.csv",index=False)