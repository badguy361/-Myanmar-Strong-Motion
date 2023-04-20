import pandas as pd
df = pd.read_csv("merge_event_eq(add_cut_2021).csv")
# df.head()
def triangle(Mw,dist):
    index=[]
    a = 1/350
    b = 3.143
    for i in range(len(Mw)):
        if a*dist[i]+b>Mw[i]:
            index.append("False")
        else:
            index.append("True")
    return index
index = triangle(df["Mw"],df["dist_sor"])
df["index"]=index
df = df[df['index']=="True"]
print("Mw",df["Mw"].iloc[1],"dist",df["dist_sor"].iloc[1])
