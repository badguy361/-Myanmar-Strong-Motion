class sac2asc:
    def __init__(self,sacdataz,sacdata1,sacdata2,zory):
        self.npts1 = int(sacdata1.npts)
        self.npts2 = int(sacdata2.npts)
        self.nptsz = int(sacdataz.npts)
        self.dt1 = float(sacdata1.delta)
        self.dt2 = float(sacdata2.delta)
        self.dtz = float(sacdataz.delta)
        try:
            self.t1 = float(sacdata1.t1)
            self.t2 = float(sacdata1.t2)
            self.t3 = float(sacdata1.t3)
            self.t4 = float(sacdata1.t4)
        except:
            print("plz define t1-t4")
        self.b = float(sacdata1.b)
        self.y1 = sacdata1.data
        self.y2 = sacdata2.data
        self.yz = sacdataz.data
        self.Parr = float(sacdata1.t1-sacdata1.b)
        self.Sarr = float(sacdata1.t2-sacdata1.b)
        self.zory = zory

        self.mz=sum(self.yz)/self.npts1 # yz -> mean
        for i in range(self.npts1):
            self.yz[i]=self.yz[i]-self.mz # normalize
        self.m1=sum(self.y1)/self.npts1
        for i in range(self.npts1):
            self.y1[i]=self.y1[i]-self.m1 # normalize
        self.m2=sum(self.y2)/self.npts1
        for i in range(self.npts1):
            self.y2[i]=self.y2[i]-self.m2 # normalize
            
    def __call__(self):
        with open("data.asc","w") as file: # !namex
            file.write(" ")
            file.write(str(round(self.Parr,4)))
            file.write("\t")
            file.write(str(round(self.Sarr,4)))
            file.write("\t")
            if self.zory == "z":
                file.write("9")
            elif self.zory == "y":
                file.write("0")
            file.write("\n") # !type
            for i in range(self.npts1):
                t = (i-1)*self.dt1
                if t<=self.t3-self.b and t>=self.t4-self.b:
                    file.write(" ")
                    file.write(str(round(t,4)))
                    file.write("   ")
                    file.write(str(round(self.yz[i],4)))
                    file.write("   ")
                    file.write(str(round(self.y1[i],4)))
                    file.write("   ")
                    file.write(str(round(self.y2[i],4)))
                    file.write("\n")