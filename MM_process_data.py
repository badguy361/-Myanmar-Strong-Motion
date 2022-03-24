# 導入模組
import os
import glob
import pandas as pd
import subprocess
import obspy
from obspy import read
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from matplotlib import pyplot as plt
from sac2asc import sac2asc
from obspy.io.sac import SACTrace

# 輸入參數＆資料和輸出位置
year = "2017" 
mon = "08"
num = 1
sac_path = f"/home/joey/緬甸BH_ubuntu/dataset/MM_new_events_20160101-20211026/{year}/{mon}/"
asc_year_path = f"/home/joey/緬甸BH_ubuntu/MM_output/{year}_output"
asc_path = f"/home/joey/緬甸BH_ubuntu/MM_output/{year}_output/{mon}/"

# 創建資料夾
if not os.path.isdir(asc_year_path):
    os.mkdir(asc_year_path)
if not os.path.isdir(asc_path):
    os.mkdir(asc_path)

# 讀入event catalog
catlog = pd.read_csv("/home/joey/緬甸BH_ubuntu/merge_event_eq.csv")

# 改變當前路徑
os.chdir(f"{sac_path}")

# 讀入所有HNE的資料,主要是獲得檔名
file_name = glob.glob("*HNE*.sac")

# 確保檔案排序是依照年份排
def TakeTime(file):
    return int(file.split("_")[3]),file.split("_")[1][0]
file_name.sort(key=TakeTime)
 
result = {}
index = num
try:
    # 調用sac指令
    os.putenv("SAC_DISPLAY_COPYRIGHT","0")
    # 主要迴圈（跑所有的HNE檔案）
    for id,i in enumerate(file_name[num-1::]):
        # 改變當前路徑
        os.chdir(f"{sac_path}")
        str1 = '_'
        read_file_name = i
        # print(id,i)
        # 抓取距離和規模
        Dist = round(catlog[catlog["file_name"].isin([i])]["dist_sor"].values[0],2)
        Mw = catlog[catlog["file_name"].isin([i])]["Mw"].values[0]
        print(f"{i} {index} / {len(file_name)}")
        # 取得HNE HNN HNZ檔名
        HNE = i.split("_")[0]+"_"+i.split("_")[1]\
                +"_"+"HNE"+"_"+i.split("_")[3]+"_"+\
                i.split("_")[4]+"_"+i.split("_")[5]
        HNZ = i.split("_")[0]+"_"+i.split("_")[1]\
                +"_"+"HNZ"+"_"+i.split("_")[3]+"_"+\
                i.split("_")[4]+"_"+i.split("_")[5]
        HNN = i.split("_")[0]+"_"+i.split("_")[1]\
                +"_"+"HNN"+"_"+i.split("_")[3]+"_"+\
                i.split("_")[4]+"_"+i.split("_")[5]
        
        # 讀取sac檔（sac的指令）
        s = f"r {HNZ} \
            {HNE} \
            {HNN} \n"
        # 畫圖 ＆ 顯示資訊 + pick mode
        s += "qdp of \n"
        s += f"title DIST={Dist}_Mw={Mw} Location BOTTOM size large \n"
        s += "ppk m \n"
        s += "w over \n"
        s += "q \n"
        subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode()) # show the interactivate window

        # print("Accept [Y/y] or Accpet but Z [Z/z] or Reject [Others]?")
        # # 吃輸入的資訊(Y Z 1-5)
        # check = input()
        # if check=="Y" or check=="y": 
        #     print(f"Accept!! copy! {check}")
        #     # 存取資訊
        #     result[f"{index}"] = [read_file_name,"y"]
        #     # 讀檔（要丟到sac2asc中）
        #     sac1 = SACTrace.read(f"{HNE}")
        #     sac2 = SACTrace.read(f"{HNN}")
        #     sacZ = SACTrace.read(f"{HNZ}")
        #     zory = "y"
        #     # print(type(sac1.data[1]))
        #     # print(sac1.reftime)

        #     # 改變當前路徑
        #     os.chdir(f"{asc_path}")
        #     # 轉出asc檔案
        #     data = sac2asc(sacZ,sac1,sac2,zory)
        #     data.__call__()
        #     os.rename(f'{asc_path}data.asc', f'{asc_path}{read_file_name}.asc')

        # elif check=="Z" or check=="z":
        #     # 同上
        #     print(f"Accept but Z problem!! copy! {check}")
        #     result[f"{index}"] = [read_file_name,"z"]
        #     sac1 = SACTrace.read(f"{HNE}")
        #     sac2 = SACTrace.read(f"{HNN}")
        #     sacZ = SACTrace.read(f"{HNZ}")
        #     zory = "z"
        #     # print(type(sac1.data[1]))
        #     # print(sac1.reftime)
            
        #     os.chdir(f"{asc_path}")
        #     data = sac2asc(sacZ,sac1,sac2,zory)
        #     data.__call__()
        #     os.rename(f'{asc_path}data.asc', f'{asc_path}{read_file_name}.asc')

        # # 當判定1-5也要存取輸出檔
        # elif check=="1":
        #     print(f"1 problem!!!")
        #     result[f"{index}"] = [read_file_name,"1"]
        # elif check=="2":
        #     print(f"2 problem!!!")
        #     result[f"{index}"] = [read_file_name,"2"]
        # elif check=="3":
        #     print(f"3 problem!!!")
        #     result[f"{index}"] = [read_file_name,"3"]
        # elif check=="4":
        #     print(f"4 problem!!!")
        #     result[f"{index}"] = [read_file_name,"4"]
        # elif check=="5":
        #     print(f"5 problem!!!")
        #     result[f"{index}"] = [read_file_name,"5"]
        # else:
        #     print("NO DEFINE!!!")
        #     result[f"{index}"] = [read_file_name,"NO DEFINE"]

        # 一定要+1
        index+=1
 
finally: # 確保臨時中斷也能輸出
    os.chdir(asc_path)
    # 存取result檔案
    # df = pd.DataFrame.from_dict(result,orient='index')
    # # 轉成csv並加在原有的後面
    # df.to_csv("result.csv",header=False,index=True,mode='a') 
    # df = pd.read_csv("result.csv",header=None)
    # # 保留最後的定義(防呆設計)
    # df = df.drop_duplicates(subset=[0],keep='last', inplace=False)
    # # 將資料做排序(防呆設計)
    # df = df.sort_values(by=[0],ignore_index = True)
    # # 重新存一次csv檔案
    # df.to_csv("result.csv",header=False,index=False,mode='w')
    # print("finish output!!")

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

# ################################ 畫asc #######################################################
# t = []
# com_z = []
# com_1 = []
# com_2 = []
# with open("/home/joey/緬甸BH_ubuntu/MM_output/2017_output/11/MM_MDY_HNE_20171104202936_10558792_RespRemoved.sac.asc","r") \
#         as file:
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

# ############################# 最終輸出格式（看有沒有需要） #########################################################

# tmp = []
# df = pd.read_csv(f"{asc_path}result.csv",header=None)
# for index,i in enumerate(df[0]):
#     tmp.append(f"{mon}_{i}")
# df[0] = tmp
# df.to_csv("result_fin.csv",header=False,index=False,mode='w')
