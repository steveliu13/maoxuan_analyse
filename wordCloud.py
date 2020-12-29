import os

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from read_file.file_parser import read_file
from word_process.cut_util import cut_word_4_cloud

# 获取所有时期-目录
def generate_catalog(file_path):
    result = []
    for dir in os.listdir(file_path):
        if os.path.isdir(file_path+"/"+dir):
            result.append(dir)
    return result


# 每个时间段的词云
def period_word_cloud():
    file_path = os.path.abspath(".") +"/文本"
    periods = generate_catalog(file_path)
    for period in periods:
        articles = read_file(file_path + "/" +period)
        sentences = []
        for art in articles:
            sentences.append(art.content)
        cut_text= cut_word_4_cloud(sentences)
        result = " ".join(cut_text)
        print(result)
        wc = WordCloud(
            # 设置字体，不指定就会出现乱码
            font_path='/System/Library/Fonts/Hiragino Sans GB.ttc',
            # 设置背景色
            background_color='white',
            # 设置背景宽
            width=500,
            # 设置背景高
            height=350,
            # 最大字体
            max_font_size=50,
            # 最小字体
            min_font_size=10,
            mode='RGBA'
            # colormap='pink'
        )
        # 产生词云
        wc.generate(result)
        # 保存图片
        wc.to_file(period + ".png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
        # 4.显示图片
        # 指定所绘图名称
        # plt.figure("0-1")
        # 以图片的形式显示词云
        # plt.imshow(wc)
        # 关闭图像坐标系
        # plt.axis("off")
        # plt.show()
