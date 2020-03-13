#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import hashlib, urllib
from datetime import datetime
from workflow import Workflow3, web, ICON_ERROR
from configuration import Configuration
from config import KEY

reload(sys)
sys.setdefaultencoding('utf-8')

search = None

def get_week(index):
    return ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][index]

def get_local_ip():
    return os.popen("ipconfig getifaddr en0").read().strip()

def get_public_ip():
    url = r"http://%s.ip138.com/ic.asp" % datetime.now().strftime("%Y")
    request = web.get(url)
    request.raise_for_status()
    content = request.text
    return content[content.find("[") + 1:content.find("]")]

def get_cache_public_ip(workflow):
    """
    获取公网IP需要依赖一次网络请求
    根据本地的网络变化情况，来判断网络是否有变化，决定是否需要获取公网IP
    以此使用本地缓存，减少网络请求，提高效率
    """
    cache_key = hashlib.md5(get_local_ip()).hexdigest()
    return workflow.cached_data(cache_key, get_public_ip, max_age=3600)

def get_weather():
    global search
    url = r"https://free-api.heweather.com/s6/weather?%s" % urllib.urlencode({"location":search, "key":KEY})
    request = web.get(url)
    request.raise_for_status()
    return request.json()["HeWeather6"][0]

def get_cache_weather(workflow):
    global search
    args = workflow.args
    search = args[0].strip() if 0 < len(args) else get_cache_public_ip(workflow)
    print(search)
    exit
    # 触发配置信息操作
    if "config" == search:
        if 1 < len(args) and "set" == args[1].strip():
            Configuration().set()
        else:
            Configuration().get()
        return
    return workflow.cached_data(r"weather-data-%s" %search, get_weather, max_age=300)

def main(workflow):
    # 检查配置信息
    if KEY is None or 32 > len(KEY):
        Configuration().set()
        return

	print("1111111")
    return
    data = get_cache_weather(workflow)
    if data is not None:
        if "ok" == data["status"]:
            # 显示地址，减少重复显示
            location = ""
            for index in ["admin_area", "parent_city", "location"]:
                if data["basic"][index] not in location:
                    location = "%s-%s" % (location, data["basic"][index])
            location = location.lstrip("-")
            # 当前天气
            today = data["now"]
            title = r"%s 现在 %s" % (location, today["cond_txt"])
            subtitle = r"温度 %s℃ | 湿度 %s%% | 能见度 %sKm | %s %s" % (today["tmp"], today["hum"], today["vis"], today["wind_dir"], today["wind_sc"])
            icon = r"icons/%s.png" % today["cond_code"]
            workflow.add_item(title=title, subtitle=subtitle, valid=False, icon=icon)
            # 未来天气
            for item in data["daily_forecast"]:
                week = get_week(datetime.weekday(datetime.strptime(item["date"], "%Y-%m-%d")))
                title = r"%s %s 白天-%s 夜间-%s" % (location, week, item["cond_txt_d"], item["cond_txt_n"])
                subtitle = r"温度 %s℃~%s℃ | 湿度 %s%% | 能见度 %sKm | %s %s" % (item["tmp_max"], item["tmp_min"], item["hum"], item["vis"], item["wind_dir"], item["wind_sc"])
                icon = r"icons/%s.png" % item["cond_code_d"]
                workflow.add_item(title=title, subtitle=subtitle, valid=False, icon=icon)
        else:
            workflow.add_item(r"暂没有 '%s' 的信息" % search, icon=ICON_ERROR)
    workflow.send_feedback()

if __name__ == "__main__":
    workflow = Workflow3()
    sys.exit(workflow.run(main))
