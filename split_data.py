import numpy as np
import shutil
import os 
import glob
os.chdir("/home/joey/緬甸BH_ubuntu/dataset/MM_2016-2021/2017")
file = glob.glob("*.sac")
for i in file:
    shutil.move(i,i.split("_")[3][4:6])
