import requests
import datetime
from bs4 import BeautifulSoup
import re
import time



start_date1 = "2020-08-03"
end_date= "2020-08-08"
video_id = '219605972'

file = open("D:/danmu.txt",'w+',encoding='utf-8')

headers ={
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
"cookie": "_uuid=9A12E616-89A1-BEE8-BE5C-6E46A317132275958infoc; buvid3=7B64182A-2741-4A53-A967-EEC8A1A4168A155805infoc; CURRENT_FNVAL=16; LIVE_BUVID=AUTO7615792392727588; rpdid=|(YuJ~m~l|k0J'ul~mkJmk~m; sid=bc2ws5py; DedeUserID=131001249; DedeUserID__ckMd5=0095ae2b0ebce065; SESSDATA=0a42914c%2C1604486701%2C81a67*51; bili_jct=7aeec0263ee68c2b9808ee880986f652; bsource=search_google; CURRENT_QUALITY=64; bp_video_offset_131001249=420393254364246809; bp_t_offset_131001249=420702990226221800; bfe_id=61a513175dc1ae8854a560f6b82b37af; PVID=1",
'origin': 'https://www.bilibili.com',
'referer': 'https://www.bilibili.com/video/BV1Nt4y1D7pW',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}


def get_duration_time(start_date1,end_date,video_id):
    # 日期格式转换
    start_date = datetime.datetime.fromisoformat(start_date1)
    end_date = datetime.datetime.fromisoformat(end_date)
    dateltime = datetime.timedelta(days=1)
    while start_date <= end_date:

        startdate_format =  start_date.strftime("%Y-%m-%d")
        download_date(startdate_format,video_id)
        start_date = start_date +  dateltime



def download_date(timedate,video_id):
    # 传入日期、视频id 进行数据爬取
    shipin_url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid={0}&date={1}'.format(video_id,timedate)
    print("正在抓取弹幕网页", shipin_url)
    response = requests.get(url = shipin_url,headers = headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    for i in soup.find_all('d'):
        locate = re.findall(r'p="(.*?)">(.*?)</d>',str(i))
        file.write(str(locate[0][0]))
        file.write(',')
        file.write(str(str(locate[0][-1])))
        file.write("\n")
    time.sleep(2) # 增加时间间隔，防止爬取太频繁;



if __name__ =='__main__':

    start_date1 = "2020-08-02"
    end_date = "2020-08-08"
    video_id = '219605972'
    get_duration_time(start_date1,end_date,video_id)
    file.close()
