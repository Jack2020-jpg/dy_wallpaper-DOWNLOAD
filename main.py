# coding=utf-8
# author: "myjack"
# data: 2025/1/3 003 0:11
from time import sleep
from DrissionPage import ChromiumPage, ChromiumOptions
import os
import requests
from tqdm import tqdm


def download_images(image_urls, folder_name='image'):
    # 检查文件夹是否存在，不存在则创建
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    print("开始下载图片...")

    # 遍历图片链接集合
    for i, url in enumerate(tqdm(image_urls, desc='下载进度')):
        try:
            # 发起请求获取图片内容
            response = requests.get(url)
            response.raise_for_status()  # 确保请求成功

            # 构造图片文件的完整路径
            image_path = os.path.join(folder_name, f'image_{i + 1}.jpg')

            # 保存图片
            with open(image_path, 'wb') as f:
                f.write(response.content)
            # print(f'图片 {i + 1} 已保存到 {image_path}')
        except requests.RequestException as e:
            print(f'图片 {i + 1} 下载失败: {e}')


co = ChromiumOptions()
# co.auto_port()
# 设置启动时最大化
co.set_argument('--start-maximized')
co.headless(True)
page = ChromiumPage(co)

target_shared_link = input("请输入抖音链接：")
# target_shared_link = """2.05 y@g.bN 11/01 eOx:/ 4k超清电脑横屏壁纸<欢迎白嫖>。# 艺术在抖音 # 电脑桌面 # 好图分享 # 超清 # 绝美  https://v.douyin.com/iyrXqsUq/ 复制此链接，打开Dou音搜索，直接观看视频！"""

target_link = ""

for item in target_shared_link.split():
    if "http" in item:
        target_link = item

print("视频短链接为：  "+ target_link)

# page.get("https://v.douyin.com/iyrQ1WXX/")
page.get(target_link)
sleep(3)

data_set = set()

"""
示例：
https://p3-pc-sign.douyinpic.com/tos-cn-i-0813c000-ce/ocFiSAHnQAfoECQAE9TpC9MEeCFfQN5AAQ0wID~tplv-dy-aweme-images:q75.webp?biz_tag=aweme_images&from=327834062&lk3s=138a59ce&s=PackSourceEnum_AWEME_DETAIL&sc=image&se=false&x-expires=1738425600&x-signature=Zrcivaf2lVvblo%2BejbW5vFuvrP8%3D
"""

image_list = page.ele('@class$focusPanel').eles("tag:img")
for item in image_list:
    link = item.link

    if link[0] == "h" and len(link) > 100:
        data_set.add(link)

# # 打印图片链接
# for item in data_set:
#     print(item)

print("一共有 "+str(len(data_set))+" 张图片")
download_images(data_set)
