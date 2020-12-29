import os
import re

from model.article import Article
from read_file.word_util import ChineseToDate


# 把所有文章读取分配到模型中
def read_file(file_dir_path):
    # 读取全部文章
    articles = []
    files = os.listdir(file_dir_path)
    write_time = None
    background = ""
    content = ""
    annotation = ""
    for file in files:
        title = get_article_title(file.title())
        content_flag = False
        anno_flag = False
        with open(file_dir_path + "/" + file, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                # 空串跳过
                if line.isspace():
                    continue
                # 日期
                if match_chinese_data(line):
                    write_time = ChineseToDate(line.strip().replace("（", "").replace("）", ""))
                    continue
                # 背景
                if line.startswith("> "):
                    background = line.replace("> ", "")
                    content_flag = True
                    continue
                # 背景之后是正文
                if content_flag:
                    content += line.strip().replace("#","")
                # 正文之后是注释, 跳过分割线
                if match_division(line):
                    content_flag = False
                    continue
                if match_annotation(line):
                    anno_flag = True
                    continue
                if anno_flag:
                    annotation += line.strip()
            anno_flag = False
        article = Article(title, write_time, background, content, annotation)
        articles.append(article)

    return articles


# 从md标题获取文章标题
def get_article_title(file_title):
    pattern = "[0-9]{3}-(.*)\.Md"
    return re.findall(pattern, file_title)[0]


# 正则判断是否是分割线
def match_division(line):
    pattern = "\-{1,50}"
    result = re.match(pattern, line.strip())
    return result is not None


# 判断是否是注释开始
def match_annotation(line):
    pattern = "注　　释"
    return line.strip() == pattern


# 正则判断是否是中文的时间
def match_chinese_data(line):
    pattern = "（一九[一二三四五六七八九○]{2}年[一二三四五六七八九十]{1,2}月[一二三四五六七八九十]{1,3}日）"
    return re.match(pattern, line.strip().replace(" ", "")) is not None


if __name__ == "__main__":
    arts = read_file(os.path.abspath("..") + "/test")
    for ar in arts:
        print(ar.title)
        print(ar.write_time)
        print(ar.background)
        print(ar.content)
        print(ar.annotation)
    # print(arts.__len__())
    # print(ChineseToDate("一九四六年十月一日"))
