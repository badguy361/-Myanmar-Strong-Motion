from obspy.io.sac import SACTrace
import os 
import glob
import pandas as pd
import subprocess

year = "2021"
allmon = ["01","02","03","04","05","06","07","08","09","10","11","12"]
for j in allmon:
    mon = j
    num = 1
    sac_path = f"/home/joey/緬甸/dataset/MM_events_20160101-20211026/{year}/{mon}/"
    asc_year_path = f"/home/joey/緬甸/output/{year}"
    asc_path = f"/home/joey/緬甸/output/{year}/{mon}/"
    if not os.path.isdir(asc_year_path):
        os.mkdir(asc_year_path)
    if not os.path.isdir(asc_path):
        os.mkdir(asc_path)

    catlog = pd.read_csv("/home/joey/緬甸/merge_event_eq(add_cut_2021).csv")
    os.putenv("SAC_DISPLAY_COPYRIGHT","0")

    os.chdir(f"{sac_path}")
    file_name = glob.glob("*HNE*.sac")
    def TakeTime(file):
        return int(file.split("_")[3])
    file_name.sort(key=TakeTime)

    result = {}
    index = num
    # 以上註解參考MM_process_data.py

    for id,i in enumerate(file_name[num-1::]):
        str1 = '_'
        read_file_name = i
        # 取得P波S波到時
        P_arrive = 50
        S_arrive = float(catlog[catlog["file_name"].isin([i])]["iasp91_S_arrival"].values[0]-\
                    catlog[catlog["file_name"].isin([i])]["iasp91_P_arrival"].values[0]+50)

        # 取得距離和震矩規模
        Dist = round(catlog[catlog["file_name"].isin([i])]["dist_sor"].values[0],2)
        Mw = catlog[catlog["file_name"].isin([i])]["Mw"].values[0]
        print(f"{i} {index} / {len(file_name)}")
        HNE = i.split("_")[0]+"_"+i.split("_")[1]\
                +"_"+"HNE"+"_"+i.split("_")[3]+"_"+\
                i.split("_")[4]+"_"+i.split("_")[5]
        HNZ = i.split("_")[0]+"_"+i.split("_")[1]\
                +"_"+"HNZ"+"_"+i.split("_")[3]+"_"+\
                i.split("_")[4]+"_"+i.split("_")[5]
        HNN = i.split("_")[0]+"_"+i.split("_")[1]\
                +"_"+"HNN"+"_"+i.split("_")[3]+"_"+\
                i.split("_")[4]+"_"+i.split("_")[5]
        s = f"r {HNZ} \
            {HNE} \
            {HNN} \n"
        # 改變t1(P_arrive)和t2(S_arrive)的資訊
        s += f"ch t1 {P_arrive} t2 {S_arrive} \n"
        s += "qdp of \n"
        # 一定要下 才會出現t1 t2的線
        s += "p1 \n"
        s += f"title DIST={Dist}_Mw={Mw} Location BOTTOM size large \n"
        s += "w over \n"
        s += "q \n"
        subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode()) # show the interactivate window
        index+=1

################################## other sac func. ##################################

# sacfile = glob.glob("*")
# for i in sacfile:
#     if i == 'MM_HKA_HNE_20160519231024_5183203_RespRemoved.sac':
#         P_arrive = catlog[catlog["file_name"].isin([i])]["P_arrive"].values[0]
#         S_arrive = catlog[catlog["file_name"].isin([i])]["S_arrive"].values[0]
#         print("P_arrive:",P_arrive)
#         print("S_arrive:",S_arrive)
#         s = f"r {i} \n"
#         s += f"ch t1 {P_arrive} t2 {S_arrive}\n"
#         s += "qdp of \n"
#         s += "p1 \n"
#         s += "title DIST=200_ML=30 Location BOTTOM size large \n"
#         s += "ppk m \n"
#         s += "w over \n"
#         s += "q \n"
#         subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

# sac1 = SACTrace.read('MM_HKA_HNE_20160519231024_5183203_RespRemoved.sac')
# sac1.t1 = catlog[catlog["file_name"].isin([i])]["P_arrive"].values[0]
# sac1.t2 = catlog[catlog["file_name"].isin([i])]["S_arrive"].values[0]
# sac1.dist = 200 
# sac1.mw = 5 

# # solve autopick: http://geophysics.eas.gatech.edu/classes/SAC/
# sac1 = SACTrace.read("MM_HKA_HNE_20160517170517_5182998_RespRemoved.sac")
# print(sac1.t3)