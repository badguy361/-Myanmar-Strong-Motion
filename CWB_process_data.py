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

year = "2020"
mon = "03"
num = 1
a="apple"

sac_path = f"/home/joey/緬甸BH_ubuntu/dataset/{year}/{mon}/"
asc_path = f"/home/joey/緬甸BH_ubuntu/{year}_output/{mon}/"

os.chdir(f"{sac_path}")
file_name = glob.glob("*H1.sac")
file_name.sort()
result = {}
index = num
try:
    os.putenv("SAC_DISPLAY_COPYRIGHT","0")
    for i in file_name[num-1::]:
        os.chdir(f"{sac_path}")
        str1 = '_'
        read_file_name = str1.join(i.split("_")[:-1])
        print(f"{read_file_name} {index} / {len(file_name)}")

        s = f"r {read_file_name}_Z.sac \
            {read_file_name}_H1.sac \
            {read_file_name}_H2.sac \
            {read_file_name}_ENG.sac \n"
        s += "qdp of \n"
        s += "ppk m \n"
        s += "w over \n"
        s += "q \n"
        subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode()) # show the interactivate window

        print("Accept [Y/y] or Accpet but Z [Z/z] or Reject [Others]?")
        check = input()
        if check=="Y" or check=="y": 
            print(f"Accept!! copy! {check}")
            result[f"{index}"] = [read_file_name,"y"]

            sac1 = SACTrace.read(f"{read_file_name}_H1.sac")
            sac2 = SACTrace.read(f"{read_file_name}_H2.sac")
            sacZ = SACTrace.read(f"{read_file_name}_Z.sac")
            zory = "y"
            # print(type(sac1.data[1]))
            # print(sac1.reftime)

            os.chdir(f"{asc_path}")
            data = sac2asc(sacZ,sac1,sac2,zory)
            data.__call__()
            os.rename(f'{asc_path}data.asc', f'{asc_path}{read_file_name}.asc')

        elif check=="Z" or check=="z":
            print(f"Accept but Z problem!! copy! {check}")
            result[f"{index}"] = [read_file_name,"z"]

            sac1 = SACTrace.read(f"{read_file_name}_H1.sac")
            sac2 = SACTrace.read(f"{read_file_name}_H2.sac")
            sacZ = SACTrace.read(f"{read_file_name}_Z.sac")
            zory = "z"
            # print(type(sac1.data[1]))
            # print(sac1.reftime)
            
            os.chdir(f"{asc_path}")
            data = sac2asc(sacZ,sac1,sac2,zory)
            data.__call__()
            os.rename(f'{asc_path}data.asc', f'{asc_path}{read_file_name}.asc')

        elif check=="1":
            print(f"1 problem!!!")
            result[f"{index}"] = [read_file_name,"1"]
        elif check=="2":
            print(f"2 problem!!!")
            result[f"{index}"] = [read_file_name,"2"]
        elif check=="3":
            print(f"3 problem!!!")
            result[f"{index}"] = [read_file_name,"3"]
        elif check=="4":
            print(f"4 problem!!!")
            result[f"{index}"] = [read_file_name,"4"]
        elif check=="5":
            print(f"5 problem!!!")
            result[f"{index}"] = [read_file_name,"5"]
        else:
            print("NO DEFINE!!!")
            result[f"{index}"] = [read_file_name,"NO DEFINE"]

        index+=1
 
finally:
    os.chdir(asc_path)
    df = pd.DataFrame.from_dict(result,orient='index')
    df.to_csv("result.csv",header=False,index=True,mode='a') 
    df = pd.read_csv("result.csv",header=None)
    df = df.drop_duplicates(subset=[0],keep='last', inplace=False) # 保留最後的定義 
    df = df.sort_values(by=[0],ignore_index = True) # 將資料做排序
    df.to_csv("result.csv",header=False,index=False,mode='w')
    print("finish output!!")

# ############################# 清理用不到的asc #########################################################

# os.chdir(asc_path)
# dir = glob.glob("*.asc")
# y_data = []
# df = pd.read_csv(f"{asc_path}result.csv",header=None)
# for index,i in enumerate(df[2]):
#     if i == "y" or i == 'z':
#         y_data.append(str(df[1][index]+'.asc'))
#         if str(df[1][index]+'.asc') not in dir:
#             print(df[0][index],df[1][index],"hasn't asc. WARNING!!")
# print("\n")
# for index,i in enumerate(dir):
#     if i not in y_data:
#         print(i,"is not y or z. WARNING!!")

# ############################# 最終輸出格式（看有沒有需要） #########################################################

# tmp = []
# df = pd.read_csv(f"{asc_path}result.csv",header=None)
# for index,i in enumerate(df[0]):
#     tmp.append(f"{mon}_{i}")
# df[0] = tmp
# df.to_csv("result_fin.csv",header=False,index=False,mode='w')

# # ################################ 畫asc #######################################################
# t = []
# com_z = []
# com_1 = []
# com_2 = []
# with open("asc_path/202003150152_SNS_15150152.P20.asc","r") as file:
#     for index,line in enumerate(file):
#         if index>0:
#             print(index,line)
#             t.append(float(line.split()[0]))
#             com_z.append(float(line.split()[1]))
#             com_1.append(float(line.split()[2]))
#             com_2.append(float(line.split()[3]))
#     plt.figure(figsize=(8,6))
#     plt.subplot(311)  
#     plt.plot(t,com_z)
#     plt.subplot(312)  
#     plt.plot(t,com_1)
#     plt.subplot(313)  
#     plt.plot(t,com_2)

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
