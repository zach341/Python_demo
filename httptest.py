import requests
from fake_useragent import UserAgent

url = "https://mirrors.dgut.edu.cn/ubuntu-releases/18.04.3/ubuntu-18.04.3-live-server-amd64.iso"
get_data = requests.get(url,headers={'UserAgent':UserAgent().random},stream=True)
with open("C:/Users/zach.zhang/Desktop/ubuntu-18.04.3-live-server-amd64.iso","wb") as f:
    for chunk in get_data.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
