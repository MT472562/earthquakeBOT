"""以下のプログラムはWindows10でのみ動作確認をしています。"""
import time
import json
import requests
import datetime
import ast
import tweepy
import webbrowser
import wave
from requests_oauthlib import OAuth1Session
from re import A
COSUMER_KEY = 'L'
COSUMER_SECRET = 'JvA'
ACCESS_TOKEN = '1'
ACCESS_TOKEN_SECRET ='4'

jsonurl551std=("https://api.p2pquake.net/v2/history?codes=551&limit=1")
jsonurls551std = requests.get(jsonurl551std)
text551std = jsonurls551std.text
data551std = json.loads(text551std)
data551std = data551std[0]
data551std_id = data551std['id']

jsonurl552old=("https://api.p2pquake.net/v2/history?codes=552&limit=1")
jsonurls552old = requests.get(jsonurl552old)
text552old = jsonurls552old.text
data552old = json.loads(text552old)

maxScale = 0

if data552old == []:
    pass
else:
    data552old = data552old[0]
    data552old_id = data552old['id']    
while True:
    start_time = time.time()
    start = datetime.datetime.now()
    jsonurl551=("https://api.p2pquake.net/v2/history?codes=551&limit=1")
    jsonurls551 = requests.get(jsonurl551)
    text551 = jsonurls551.text
    data551 = json.loads(text551)
    data551 = data551[0]
    data551_id = data551['id']
    if data551std_id == data551_id:
        pass
    else:
        #震度に関する情報
        time.sleep(2)
        cunt = 0
        maxScale = data551['earthquake']['maxScale']
        maxScale_list = [0,10,20,30,40,45,50,55,60,70]
        maxScalemsg_list = ["震度0","震度1","震度2","震度3","震度4","震度5弱","震度5強","震度6弱","震度6強","震度7"]
        for n in maxScale_list:
            if maxScale == n:
                maxScalemsg = maxScalemsg_list[cunt]
            cunt+=1
        #津波に関する情報
        cunt = 0
        domesticTsunami = data551['earthquake']['domesticTsunami']
        domesticTsunami_list = ["None","Unknown","Checking","NonEffective","Watch","Warning"]
        domesticTsunamimsg_list = ["この地震による津波の心配はありません。","この地震による津波の可能性は不明です。",\
                                   "この地震による津波の可能性については調査中です。","この地震によって若干の海面変動がありますが、被害の心配はありません。",\
                                   "この地震により、津波注意報が発令されています。","津波予報[種類不明]"]
        for n in domesticTsunami_list:
            if domesticTsunami == n:
                domesticTsunamimsg = domesticTsunamimsg_list[cunt]  
            cunt+=1 
        #地震の情報の種類取得
        cunt = 0
        earthquake_type_list = ["ScalePrompt","Destination","ScaleAndDestination",\
                                "DetailScale","Foreign","Other"]
        earthquake_typemsg_list = ["震度速報","震源に関する情報","震度・震源に関する情報",\
                                   "各地の震度に関する情報","遠地地震に関する情報","その他の情報"]
        earthquake_type = data551['issue']['type']
        for n in earthquake_type_list:
            if earthquake_type == n:
                earthquake_typemsg = earthquake_typemsg_list[cunt]  
            cunt+=1 
        #津波発生時の処理
        if domesticTsunami == "None":
            pass
        else:
            jsonurl552=("https://api.p2pquake.net/v2/history?codes=552&limit=1")
            jsonurls552 = requests.get(jsonurl552)
            text552 = jsonurls552.text
            data552 = json.loads(text552)
            if data552old == []:
                pass
            else:
                data552 = data552[0]
                data552_id = data552['id']
                if data552old_id == data552_id:
                    data552old_id = data552_id
                else:
                    data552_id = data552['id']#ID
                    data552_type = data552['issue']['type']#タイプ
                    data552_source = data552['issue']['source']#発表元
                    if data552_type == "focus" or "Focus":
                        data552_type_msg = "津波予報"
                        data552old_id = data552_id
                    else:
                        print("取得失敗")
                        data552old_id = data552_id
        #時間取得
        hour = data551['earthquake']['time']
        #マグニチュード取得
        magnitude = data551['earthquake']['hypocenter']['magnitude']
        if magnitude == -1.0:
            magnitudemsg = "取得失敗"
        else:
            magnitudemsg = magnitude
        #震源の深さ取得
        depth = data551['earthquake']['hypocenter']['depth']
        if depth == "ごく浅い":
            depthmsg ="ごく浅い"
        else:
            depthmsg = ("約{0}km".format(depth))
        #震源地取得
        name = data551['earthquake']['hypocenter']['name']  
        #data551のid取得
        data551_source = data551['issue']['source']
        #変更
        error_msg = "取得失敗"
        #point
        points = data551['points']
        points_count =str(points)
        counter = points_count.count('addr')
        maxScale = data551['earthquake']['maxScale']
        i = 0
        addr_list = []
        pref_list = []
        scale_list = []
        for i in range(counter):
            if points[i]['scale'] == maxScale:
                addr = points[i]['addr']
                addr_list.append(addr)
                pref = points[i]['pref']
                pref_list.append(pref)
                scale = points[i]['scale']
                scale_list.append(scale) 
            i+=1
        pref_point = (sorted(list(set(pref_list))))
        scale_point = (str(addr_list))
        pref_list_str =(str(pref_point))
        scale_point_name = scale_point.replace('[', '').replace(']', '').replace("'", '')
        pref_point_name = pref_list_str.replace('[', '').replace(']', '').replace("'", '')
        #日付
        year,month,day,hour_,minutes = hour[0:4],hour[5:7],hour[8:10],hour[11:13],hour[14:16]
        if hour_ == "12":
            hour_ = ("お昼の12")
        elif hour_ == "0":
            hour_ = ("深夜の0")
        else:
            if hour_ >= "1" and hour_ <= "11":
                hour_ = ("午前{0}".format(hour_))
            elif hour_ >= "13" and hour_ <= "23":
                hour_ = (int(hour_))
                hour_ = hour_ - 12
                hour_ = ("午後{0}".format(hour_))
        Tweet_msg_time = ("{0}時{1}分ごろ".format(hour_,minutes))
        Tweet_msg = ("【地震情報】\n{0}{1}を震源とする地震がありました。\n震源の深さは{3} 地震の規模はM{2}\n最大{4}を{6}で観測しています。\n{5}\n揺れを観測した地域は以下の通りです。".format(Tweet_msg_time,name,magnitudemsg,depthmsg,maxScalemsg,domesticTsunamimsg,pref_point_name))
        Tweet_msg_no2 = ("最大{0}を観測した地域\n{1}".format(maxScalemsg,scale_point_name))
        print("-"*80)
        print(Tweet_msg)
        print("\n")
        print(Tweet_msg_no2)
        data551std_id = data551_id
        if maxScale >= 30:    
            url ='https://api.twitter.com/1.1/statuses/update.json'
            if depth == -1 or maxScale == error_msg:
                pass
            else:
                def tweet(status, batch_mode, in_reply_to_status_id=None):
                    global tweet_id
                    if batch_mode:
                        params = {"status": status, "batch_mode": "first", "weighted_character_count": True}
                    else:
                        params = {"status": status, "in_reply_to_status_id": in_reply_to_status_id, "batch_mode": "subsequent", "weighted_character_count": True}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params=params)
                    tweet_id = req.json()["id_str"]
                def thread_tweet(statuses=[]):
                    if statuses != []:
                        for i in range(len(statuses)):
                            if i == 0:
                                tweet(statuses[i], True)
                            else:
                                tweet(statuses[i], False, tweet_id)
                if __name__ == '__main__':
                    twitter = OAuth1Session(COSUMER_KEY,COSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
                    thread_tweet([Tweet_msg,Tweet_msg_no2]) 
                webbrowser.open("https://twitter.com/bot77552486")
                print("\n")
                print("I posted this on Twitter because of the intensity 3 and above.")
        else:
            print("\n")
            print("I have not posted on Twitter because the seismic intensity is below 3.")
    end_time = time.time()
    total_time = end_time-start_time
    if total_time >= 3:
        sleep_time = total_time
    else:
        sleep_time = 3-total_time
        
    print("\r"+str(total_time),end="")
    time.sleep(sleep_time)
