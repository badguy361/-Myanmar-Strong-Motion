from obspy.geodetics.base import gps2dist_azimuth, kilometer2degrees
from obspy.taup import TauPyModel
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np

catlog = pd.read_csv("D:/緬甸BH/merge_event_eq(add_cut_2021).csv")

################################# write iasp91 arrival time to csv #################################
iasp91_P_arrival = []
iasp91_S_arrival = []
for i in tqdm(range(catlog.shape[0])):
    try:
        model = TauPyModel(model='iasp91') #jb pwdk can test 
        dist = kilometer2degrees(catlog["dist_surface"][i]) 
        depth = catlog["origins.depth"][i]/1000 
        arrivals = model.get_travel_times\
            (source_depth_in_km=depth, distance_in_degree=dist,\
            phase_list=["P","S",'p','s'])
        iasp91_P_arrival.append(arrivals[0].time)
        iasp91_S_arrival.append(arrivals[-1].time)
    except:
        iasp91_P_arrival.append("NA")
        iasp91_S_arrival.append("NA")
        
catlog["iasp91_P_arrival"] = iasp91_P_arrival
catlog["iasp91_S_arrival"] = iasp91_S_arrival
catlog.to_csv("D:/緬甸BH/merge_event_eq(add_cut_2021).csv",index=False,mode='w')

################################# write other model to csv #################################
models = ["ak135","iasp91","prem"]

for mod in models:
    P_arrival = []
    S_arrival = []
    for i in tqdm(range(catlog.shape[0])):
        try:
            model = TauPyModel(model=mod) #jb pwdk can run 
            dist = kilometer2degrees(catlog["dist_surface"][i]) 
            depth = catlog["origins.depth"][i]/1000 
            arrivals = model.get_travel_times\
                (source_depth_in_km=depth, distance_in_degree=dist,\
                phase_list=["P","S",'p','s'])
            P_arrival.append(arrivals[0].time)
            S_arrival.append(arrivals[-1].time)
        except:
            P_arrival.append("NA")
            S_arrival.append("NA")
            
    catlog[f"{mod}_P_arrival"] = P_arrival
    catlog[f"{mod}_S_arrival"] = S_arrival
    catlog.to_csv("D:/緬甸BH/merge_event_eq(add_cut_2021).csv",index=False,mode='w')

################################# check other model if they are different #################################

model = TauPyModel(model="ak135") #jb pwdk can run 
dist = kilometer2degrees(catlog["dist_surface"][1]) 
depth = catlog["origins.depth"][1]/1000 
arrivals = model.get_travel_times\
    (source_depth_in_km=depth, distance_in_degree=dist,\
    phase_list=["P","S",'p','s'])
print("ak135",arrivals[0].time)
print("ak135",arrivals[-1].time)

model = TauPyModel(model="iasp91") #jb pwdk can run 
dist = kilometer2degrees(catlog["dist_surface"][1]) 
depth = catlog["origins.depth"][1]/1000 
arrivals = model.get_travel_times\
    (source_depth_in_km=depth, distance_in_degree=dist,\
    phase_list=["P","S",'p','s'])
print("iasp91",arrivals[0].time)
print("iasp91",arrivals[-1].time)

model = TauPyModel(model="prem") #jb pwdk can run 
dist = kilometer2degrees(catlog["dist_surface"][1]) 
depth = catlog["origins.depth"][1]/1000 
arrivals = model.get_travel_times\
    (source_depth_in_km=depth, distance_in_degree=dist,\
    phase_list=["P","S",'p','s'])
print("prem",arrivals[0].time)
print("prem",arrivals[-1].time)

################################# plot scatter #################################
models = ["ak135","iasp91","prem"]
catlog = pd.read_csv("/home/joey/緬甸BH_ubuntu/merge_event_eq.csv")
dif_P_ak = abs(catlog[f"{models[1]}_P_arrival"] - catlog[f"{models[0]}_P_arrival"])
dif_S_ak = abs(catlog[f"{models[1]}_S_arrival"] - catlog[f"{models[0]}_S_arrival"])
plt.scatter(np.arange(0,len(catlog[f"{models[1]}_P_arrival"])),dif_P_ak,label="P_residual",s=2)
plt.scatter(np.arange(0,len(catlog[f"{models[1]}_S_arrival"])),dif_S_ak,label="S_residual",s=2)
plt.legend()
plt.savefig("/home/joey/Desktop/output.jpg",dpi=300)
# dif_P_prem = abs(catlog[f"{models[1]}_P_arrival"] - catlog[f"{models[2]}_P_arrival"])
# dif_S_prem = abs(catlog[f"{models[1]}_S_arrival"] - catlog[f"{models[2]}_S_arrival"])
# plt.scatter(np.arange(0,len(catlog[f"{models[1]}_P_arrival"])),dif_P_prem,label="prem_P",s=2)
# plt.scatter(np.arange(0,len(catlog[f"{models[1]}_S_arrival"])),dif_S_prem,label="prem_S",s=2)
# plt.legend()
# reference: https://seismo.berkeley.edu/wiki_cider/REFERENCE_MODELS