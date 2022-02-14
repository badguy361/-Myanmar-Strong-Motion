from obspy.geodetics.base import gps2dist_azimuth, kilometer2degrees
from obspy.taup import TauPyModel
import pandas as pd
from tqdm import tqdm

catlog = pd.read_csv("/home/joey/緬甸BH_ubuntu/merge_event_eq.csv")

iasp91_P_arrival = []
iasp91_S_arrival = []
for i in tqdm(range(catlog.shape[0])):
    try:
        model = TauPyModel(model='iasp91') #jb pwdk can run 
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
catlog.to_csv("merge_event_eq.csv",index=False,mode='w')