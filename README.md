# 谷歌图片通用爬虫

## 安装

需要python 3.6

[Download python-3.6 from python.org](https://www.python.org/downloads/release/python-368/)

使用pip安装selenium, requests

``` bash
    pip3 install selenium requests
```

下载chrome驱动

[Download ChromeDriver from chromium.org](http://chromedriver.chromium.org/downloads)

## 使用

### chromedriver的处理

请将下载好的chrome驱动程序放在与main.py的**同级目录下**，对于windows开发者，请保证chrome驱动程序的文件名为**chromedriver.exe**。对于其他系统的开发者，在保证驱动程序和脚本在**同级目录的前提下**，修改main.py第37行，将“chromedriver.exe”修改为您下载好相应的chromedriver的文件名。

### 配置下载网址

本爬虫是基于google图片搜索而构建的爬虫，因此先在google中输入要查找的图片关键字，例如“蔬菜”。点击图片分类，google会跳转到“蔬菜”关键字的图片搜索页面，接着复制当前网址，在main.py第40行的url_list的列表中删除默认的两个dict（这两个是配置demo示范，分别爬取的是“蔬菜”和“不新鲜的蔬菜”，需要删去换成自己需要爬取的网址），将刚复制的网址粘贴上去。下面是具体参数的解释：

```python
{
    "url": "你要爬取的网址，需要粘贴上去的内容。",
    "dir": "爬取结果图片保存的文件夹，例如示例中写的是fresh，则结果就会保存在result/fresh下"
}
```

### 配置代理

由于在国内，又是针对google图片进行爬取，代理必不可少。main.py的第18行是requests库需要的代理，main.py的26行是selenium需要的代理，请根据本机情况自行填写代理地址。

### 运行

以上全部配置完成即可运行，结果会保存在与main.py的同级目录下的 “result/您配置的保存文件夹”中。

运行：

```bash
python main.py
```

## 依赖

[selenium github](https://github.com/SeleniumHQ/selenium)

[requests github](https://github.com/kennethreitz/requests)

## license

[MIT](https://opensource.org/licenses/MIT)
