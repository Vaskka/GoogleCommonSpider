import os
import re
import time
import requests
import urllib.parse

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


requests_proxies = {
  "http": "http://127.0.0.1:1080",
  "https": "http://127.0.0.1:1080",
}


PROXY = "127.0.0.1:1080"

webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False
}


driver = webdriver.Chrome(executable_path="chromedriver.exe", desired_capabilities=webdriver.DesiredCapabilities.CHROME)


url_list = [
    {
        "url": "https://www.google.com.hk/search?q=%E8%94%AC%E8%8F%9C&newwindow=1&safe=strict&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjC7KDR0IvjAhVOzRoKHX-LBR0Q_AUIECgB&biw=1920&bih=969#imgrc=G2KeiGwmZFaMmM:",
        "dir": "flesh"
    },
    {
        "url": "https://www.google.com/search?q=%E4%B8%8D%E6%96%B0%E9%B2%9C%E7%9A%84%E8%94%AC%E8%8F%9C&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj75fup5IvjAhWSsnEKHfc_Da0Q_AUIECgB",
        "dir": "unflesh"
    }
]


# 爬虫结果根目录
result_root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result")


# 自增id
i = 0


def get_real_url(u):
    res = re.match(".*?imgurl=(.*)&imgrefurl=.*", u)

    if res:
        return res.group(1)
    else:
        return None
    pass


def get_type(u):
    res = re.match(".*\.(.*)", u)

    if res:
        result = res.group(1)
        if "&" in str(result):
            return result.split("&")[0]

        return res.group(1)
    else:
        return None
    pass


def download(result_dir):
    """
    下载本次get的图片
    :param result_dir: 图片存储的路径
    :return: None
    """
    global i

    # 记录每次开始的index
    count = 0

    click_flag = False

    while True:

        # 检查是否需要点击获取更多
        if not click_flag:
            # 正常加载
            for _i in range(300):
                ActionChains(driver).key_down(Keys.DOWN).perform()

        else:
            more_input = driver.find_element_by_id("smb")
            try:
                more_input.click()
            except ElementNotInteractableException:
                # 全部图片下载完成
                break
            click_flag = False

        time.sleep(5)

        root = driver.find_elements_by_xpath("//div[@id='rg_s']/div/a[1]")

        for url in root[count:]:
            # 下载图片

            u = url.get_attribute("href")
            u = get_real_url(urllib.parse.unquote(u))

            if u is None:
                print("u is None")
                continue

            print(u)
            _type = get_real_url(u)
            if _type is None:
                _type = "jpg"
            try:
                res = requests.get(url=u, headers=header, timeout=3)
            except:
                try:
                    res = requests.get(url=u, proxies=requests_proxies, headers=header)
                except:
                    continue

            with open(os.path.join(result_dir, "%d.%s" % (i, _type)), "wb") as f:
                f.write(res.content)

            print("save img[%d] in [%s]" % (i, result_dir))
            i += 1
            pass

        print("batch end. count:%d, len:%d" % (count, len(root)))
        if count == len(root):
            click_flag = True

        count = len(root)

    pass


def init():
    """
    准备工作
    :return: None
    """
    # 准备结果文件夹
    if not os.path.exists(result_root_dir):
        os.mkdir(result_root_dir)

    pass


def main():

    init()

    for item in url_list:
        url = item["url"]
        _dir = item["dir"]

        # 检查dir是否合理
        should_path = os.path.join(result_root_dir, _dir)
        if not os.path.exists(should_path):
            os.mkdir(should_path)

        # 下载图片
        driver.get(url)
        download(should_path)

    driver.close()
    pass


def debug():
    pass


if __name__ == '__main__':
    main()
    # debug()
    pass
