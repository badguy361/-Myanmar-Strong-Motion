# -Myanmar-Strong-Motion
在使用obspy下載緬甸2016-2021的資料後可以用python調用SAC(地球物理處理資料的套件)對這些地震波進行處理，並透過後續的濾波、基線校正等流程計算出工程反映譜，後再經過RCTC可回歸出該區域的強地動衰減式(GMPE)。

# Datasets
* event catalog.csv : obspy下載地震事件資料，但進行很多資料前處理，包括合併GCMT、吳老師地震資料，以及地震矩規模轉換，合併接收測站等等..如果需要這份catalog(2016-2021)，可以email: **t1616joy@yahoo.com.tw**
!(https://drive.google.com/file/d/1sS_5yyq0X0NAWJjQhuaV5fZA6VOYvNiH/view?usp=sharing)

* SAC檔 : obspy下載的地震資料，訂好年份、經緯(minlat = 10 maxlat = 30 minlng = 90maxlng = 102)，並用 **iasp91速度構造** 模型預測P、S波到時，再以P波到時前50秒S波到時後300秒作為地震事件window的大小。(詳見 **find_data.py**)


# Process (main code)
設置好**SAC**及**catalog.csv**檔案位置，終端機執行 `python MM_process_data.py` 即可開始進行濾波，濾波方式就跟一般操作SAC下的ppk mode一模一樣。

# Important code


* `sac2asc.py` : 將picking完的SAC檔案轉換成asc檔案(原本是fortran檔`sac2asc.f`，但由於還要編譯才能執行有夠麻煩，所以將其重構成python檔)。


* `revise_sac.py` : 下載後的SAC檔案是沒有理論到時的，因此需要透過iasp91進行預測，而iasp91預測的到時資訊包含在event catalog.csv檔案中，因此設定好資料夾位置後可在終端機執行 `python revise_sac.py` 即可獲得 **已預測** 過後的SAC檔案。


* `get_iasp91.py` : 使用iasp91速度構造模型預測發震後的P波S波到時，並將此預測時間存到catalog.csv中方便後續調用。其中也包含使用不同的速度構造模型所試出的不同成果比較。


* `find_data.py` : 取得地震波資料，取得標準為P波預測到時前50秒S波預測到時候300秒，做為一筆地震的資料(此標準是經過測試所選定，*避免因為地震距離過遠而使得地震波被切掉*)。


# Other code


* `sac_info_csv.py` : 取得地震測站的資訊(依照SAC檔案中的測站名而去抓)。


* `find_data_WU.py` : 前人下載資料的檔案，已用 `find_data.py` 取代。


* `CWB_process_data.py` : 氣象局的地震波行處理，之前用來確認由shell轉python沒問題的過度程式，但若後人有需求要用本檔案處理氣象局資料亦可參考此檔案。

* `MM_BH_pick.sh` : 原本計畫使用shell操作picking程式，但後改用python，此檔案為改寫到一半的shell檔案。

* `split_data.py` : 將資料分門別類的檔案(已用 `find_data.py` 裡的功能取代)

