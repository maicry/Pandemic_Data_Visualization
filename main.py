# 主程序 位于main.py文件 第23、60行

import zipfile
import pandas as pd
import numpy as np
import glob
from pyecharts.charts import Map
from pyecharts import options as opts


# 定义解压zip文件，将疫情数据文件解压到指定目录
def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


# 读取Data文件的疫情数据
def read():
    # 初始化各种数据
    city_name = []  # 城市名
    amount = []  # 累计确诊
    city_list = []  # 城市-累计确诊
    for i in range(0, 364):
        amount.append(0)  # 将每个城市累计确诊初始化为零

    # 将Data.zip解压到Data文件夹中
    unzip_file(zip_src='./Data.zip', dst_dir='./Data')
    print("数据解压成功！")
    c = 1
    # 遍历每一个csv文件
    for n1 in glob.glob('./Data/*.csv'):
        infor = pd.read_csv(n1)
        # 在第一次遍历的时候载入所有城市名称
        if c == 1:
            name = np.array(infor['城市'])
            for h in name:
                city_name.append(h)
            c += 1
        count = np.array(infor['新增确诊'])
        # 遍历每一个文件的每一个新增确诊信息
        m = 0
        for l1 in count:
            amount[m] += l1
            m += 1
    # print(city_name)
    # print(amount)
    # 将城市数据写入city_list列表中
    for n1 in range(0, 364):
        city_list.append((city_name[n1], int(amount[n1])))
    print("数据写入成功！")
    return city_list


# 绘出可视化图像
def draw_map(city_list):
    china_city = (
        Map(init_opts=opts.InitOpts(width='1100px', height='750px'))  # 设置窗口分辨率大小
        .add("", city_list, "china-cities", label_opts=opts.LabelOpts(is_show=False))  # 采用china-cities模型描绘地级市的疫情模型
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2021年中国新冠累计确诊数据地图"),  # 命名表名
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True, range_text=['高', '低'], pieces=[  # 分段显示
                    {"min": 10000, "color": "#642100"},                 # 分别设置值和颜色
                    {"min": 1000, "max": 9999, "color": "#a23400"},
                    {"min": 500, "max": 999, "color": "#bb5e00"},
                    {"min": 100, "max": 499, "color": "#ff8000"},
                    {"min": 10, "max": 99, "color": "#ffaf60"},
                    {"min": 1, "max": 9, "color": "#ffd1a4"},
                    {"min": 0, "max": 0, "color": "#fffaf4"}
                ]
            ),
        )
    )
    china_city.render("2021年中国新冠累计确诊数据地图.html")  # 存储可视化文件为html格式
    print("地图绘制成功！")


draw_map(read())


