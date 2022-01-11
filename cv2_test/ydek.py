
from lxml import etree
import urllib.parse
import requests,time
from threading import Thread
import os


url = 'http://ydek.drugnews.cn/app/index.php?i=2&c=entry&id=44&sectionid=0&uid=15903&do=lesson&m=fy_lessonv2'
# # url = 'http://192.168.0.133:8083/api/yt-pharmacy-user/add-user2'
#
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030073)',
    'Cookie':'PHPSESSID=9906b11961a8ac830b19e54bb19ff53f'
}
session = requests.session()
session.headers=headers
# res = session.get(url)
# print(res.text)

# with open('fy_lessonv2.html',mode='w',encoding='utf-8') as f:
#     f.write(res.text)
# f.close()
# exit()

class web_info(object):
    def __init__(self,url,headers):
        self.url = url
        self.headers = headers

    def get_m3u8_web_url(self,video_file,sectionid):
        try:
            time.sleep(0.5)
            m3u8_list = []

            with open(str(sectionid)+'.m3u8',mode='r',encoding='utf-8') as f:
                m3u8_data = f.read().split('\n')
                # m3u8_data = requests.get(self.url,self.headers).text.split('\n')
                # print(len(m3u8_data),m3u8_data)
                for i in m3u8_data:
                    if '.ts' in i:
                        i = i.split('/')[-1]
                        m3u8_list.append(i)

                for ts in m3u8_list:
                    web_url = self.url.replace(self.url.split('/')[-1],ts)
                    web_info.download(self,web_url,video_file,sectionid)

        except Exception as e:
            print(e)

    def download(self,web_url,video_file,sectionid):
        # print(web_url)
        # print(video_file)
        # print(sectionid)

        ts_file = os.path.basename(web_url).split('?')[0]
        # os.makedirs(sectionid,exist_ok=True)

        # print(os.path.join(sectionid,video_file))
        # open(os.path.join(sectionid, video_file), mode='ab')
        if not os.path.exists(os.path.join(sectionid,ts_file)):
            print(os.path.exists(os.path.join(sectionid,ts_file)))
            print(os.path.join(sectionid, ts_file))
        return True
        try:
            video_data = requests.get(web_url,self.headers,timeout = 120)
            #print('开始下载')
            with open(os.path.join(sectionid,video_file),mode='ab') as f:
                for content in video_data.iter_content(10240):
                    f.write(content)

            with open(os.path.join(sectionid,ts_file),mode='ab') as f:
                for content in video_data.iter_content(10240):
                    f.write(content)
            print('下载 %s 完成' %(web_url))
        except Exception as e:
            print(e)


def app_master(url,headers,ids):
    start_list = []
    i=0
    for u in url:
        web_info_list = web_info(u,headers)
        time.sleep(0.5)
        video_file = str(ids[i]).replace('.', '_') + '.ts'

        # print(video_file)
        t = Thread(target=web_info_list.get_m3u8_web_url, args=(video_file,ids[i]))
        start_list.append(t)
        i = i + 1
    for t in start_list:
        t.start()
    for t in start_list:
        t.join()
urls = []
ids=[]
titles=[]
with open('fy_lessonv2.html',mode='r',encoding='utf-8') as f:
    # print(f.read())
    result = etree.HTML(f.read())
    f.close()

    for e in result.xpath('//li/a[@href]'):
        lession_url = e.get('href')
        # print(e.xpath('div'))
        # for title1 in e.xpath('./div'):
        #     print(title1.xpath('./text()'))

        for title in e.xpath('div/text()'):
            title=title.replace('\n','').replace('\t','').replace('\xa0','').replace('\xca','')
            if  title:
                # print(title)
                titles.append(title)
        # print(len(lession_url.split('./')))

        # urllib3.
        if len(lession_url.split('./'))==1:
            continue
        lession_url = urllib.parse.urljoin('http://ydek.drugnews.cn/app/',e.get('href')+'&uid=15905')
        parsed = urllib.parse.urlparse(lession_url)
        # print(lession_url)
        querys = urllib.parse.parse_qs(parsed.query)
        sectionid = querys.get('sectionid')[0]
        ids.append(str(sectionid))

        # res = session.get(lession_url)
        # with open(str(sectionid)+'.html',mode='w',encoding='utf-8') as f:
        #     f.write(res.text)
        # f.close()
        with open(os.path.join(str(sectionid), str(sectionid)+'.html'), mode='r', encoding='utf-8') as f:
            # print(os.path.join(str(sectionid), str(sectionid)+'.html'))
            read_text = f.read()
            result = etree.HTML(read_text)
            # with open(os.path.join(str(sectionid), str(sectionid)+'.html'), mode='w', encoding='utf-8') as f1:
            #     f1.write(read_text)
            #     print(len(read_text))
            # f1.close()
            f.close()



            for e in result.xpath('//video'):
                # print(e.get('src'))
                urls.append(e.get('src'))


                # res = session.get(e.get('src'))
                with open(os.path.join(str(sectionid), str(sectionid) + '.m3u8'),mode='r',encoding='utf-8') as f:
                    # with open(os.path.join(str(sectionid), str(sectionid) + '.m3u8'), mode='w', encoding='utf-8') as f1:
                    #     f1.write(f.read())
                    # f1.close()
                    pass
                f.close()


# app_master(urls,headers,ids)

print(len(urls))
print(len(ids))
print(len(titles))

def copy():
    # 复制文件到F盘
    i=0
    for u in urls:
        # print(i,u)
        video_file = str(ids[i]).replace('.', '_') + '.ts'
        title_file = str(titles[i]).replace('.', '_') + '.ts'
        if not os.path.exists(os.path.join('f:/', title_file)):

            # exit()
            try:

                with open(os.path.join(str(ids[i]).replace('.', '_'), video_file), mode='rb') as f:
                    # print(str(os.path.join('f:/', title_file)))
                    with open(os.path.join('f:/', title_file), mode='wb') as f1:
                        f1.write(f.read())
                    f1.close()
                f.close()

            except Exception as e:
                print(e)
                print(os.path.join('f:/', title_file))
                pass
            time.sleep(5)
        i = i + 1

print(urls)
print(ids)
print(titles)



# video_file=str(ids[i]).replace('.', '_') + '.ts'
# video_file=str(titles[i]).replace('.', '_') + '.ts'
# with open(os.path.join(sectionid, video_file), mode='ab') as f:
#     for content in video_data.iter_content(10240):
#         f.write(content)