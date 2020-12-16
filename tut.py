import pandas as pd
import requests
from bs4 import BeautifulSoup



ref_str = "https://spotifycharts.com/regional/global/daily/"
ref_arr = []
for x in range (1,13):
    date = "2020-"
    if x<10:
        date = date+ "0" + str(x) + "-01/download"
    else:
        date = date + str(x) + "-01/download"
    date = ref_str + date
    ref_arr.append(date)


for i in ref_arr:
    r = requests.get(i, allow_redirects = True)
    date = i[48:58]
    print(date)
    fileName = "regional-global-daily-" + date + ".csv"
    print(fileName)
    open(fileName, "wb").write(r.content)
    df = pd.read_csv(fileName)

