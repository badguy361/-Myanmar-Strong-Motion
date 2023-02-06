# 專案目的
為取得緬甸區域強地動資料，該專案透過地震學處理套件 obspy 下載緬甸 2016-2021 的資料，為統一操作語言，亦使用 python 調用地震學資料處理工具 SAC 對該些地震波資料進行處理，最後藉由濾波、基線校正等流程計算出工程反映譜，後再經過RCTC可回歸出該區域的強地動衰減式(GMPE)。
**然本專案著重在資料下載到資料處理結束。**

# Datasets
* event catalog.csv : obspy下載地震事件紀錄，加上比對GCMT、吳老師地震資料後決定的focal type，及地震矩規模轉換，合併接收測站等等..若需要這份catalog(2016-2021)。email: **t1616joy@yahoo.com.tw**

* SAC檔 : obspy下載之地震資料，訂好年份、經緯(minlat = 10 maxlat = 30 minlng = 90maxlng = 102)，並用 **iasp91速度構造** 模型預測P、S波到時，再以P波到時前50秒S波到時後300秒作為地震事件window的大小。(詳見 **find_data.py**)

![Imgur](https://i.imgur.com/vscBTzM.png)

# 操作流程
1. 環境問題，若已經是linux OS且 python 及 SAC 安裝完畢，可直接跳到步驟2即可。若是尚未設置好環境可參考本專案之dockerfile
，於本地安裝docker完畢後(此處部贅述網上很多教學)，建置image後，即可依照指令將專案run起來，進到容器中即可開始操作。
```
docker build -t mm_seismic .
docker run -it -v 本機路徑:/app -d -p 80:5000 --name seis mm_seismic
docker exec -it mm_seismic bash
```

2. 設置好**SAC**及**catalog.csv**檔案位置，終端機執行 `python MM_process_data.py` 即可開始進行濾波，濾波方式就跟一般操作SAC下的ppk mode一樣。
![Imgur](https://i.imgur.com/noT7zu7.png)
# Important code


* `sac2asc.py` : 將picking完的SAC檔案轉換成asc檔案(原本是fortran檔`sac2asc.f`，但由於還要編譯才能執行有夠麻煩，所以將其重構成python檔)。


* `revise_sac.py` : 下載後的SAC檔案是沒有理論到時的，因此需要透過iasp91進行預測，而iasp91預測的到時資訊包含在event catalog.csv檔案中，因此設定好資料夾位置後可在終端機執行 `python revise_sac.py` 即可獲得 **已預測** 過後的SAC檔案。


* `get_iasp91.py` : 使用iasp91速度構造模型預測發震後的P波S波到時，並將此預測時間存到catalog.csv中方便後續調用。其中也包含使用不同的速度構造模型所試出的不同成果比較。
![Imgur](https://i.imgur.com/M74afpj.png)

* `find_data.py` : 取得地震波資料，取得標準為P波預測到時前50秒S波預測到時候300秒，做為一筆地震的資料(此標準是經過測試所選定，*避免因為地震距離過遠而使得地震波被切掉*)。


# Reference code


* `sac_info_csv.py` : 取得地震測站的資訊(依照SAC檔案中的測站名而去抓)。


* `find_data_WU.py` : 前人下載資料的檔案，已用 `find_data.py` 取代。


* `CWB_process_data.py` : 氣象局的地震波行處理，之前用來確認由shell轉python沒問題的過度程式，但若後人有需求要用本檔案處理氣象局資料亦可參考此檔案。

* `MM_BH_pick.sh` : 原本計畫使用shell操作picking程式，但後改用python，此檔案為改寫到一半的shell檔案。

* `split_data.py` : 將資料分門別類的檔案(已用 `find_data.py` 裡的功能取代)

