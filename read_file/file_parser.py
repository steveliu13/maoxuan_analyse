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
        print(file.title())
        if file.title().__contains__("Store"):
            continue
        title = get_article_title(file.title())
        back_line = 0
        anno_line = 0
        lines = open(file_dir_path + "/" + file, "r", encoding="utf-8").readlines()
        for i in range(lines.__len__()):
            lines[i] = lines[i].strip()
            line = lines[i]
            if line.isspace():
                continue
            if match_chinese_data(line):
                write_time = ChineseToDate(line.strip().replace(" ",""))
                continue
            # 背景
            if line.startswith(">"):
                background = line.replace(">", "").strip()
                back_line = i
                continue
            # 正文之后是注释, 跳过分割线
            if match_division(line):
                anno_line = i
                continue
        if anno_line == 0:
            anno_line = len(lines)
        content = "".join(lines[back_line+1: anno_line])
        annotation = "".join(lines[anno_line+1: len(lines)])

        article = Article(title, write_time, background, content, annotation)
        title = ""
        write_time = None
        background = ""
        content = ""
        annotation = ""
        articles.append(article)

    return articles


# 从md标题获取文章标题
def get_article_title(file_title):
    pattern = "[0-9]{3}-(.*)\.[mM]d"
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
    pattern1 = "[（(]一九[一二三四五六七八九○]{2}年[一二三四五六七八九十]{1,2}月([一二三四五六七八九十]{1,3}日)?[）)]"
    #pattern2 = "（一九[一二三四五六七八九○]{2}年[一二三四五六七八九十]{1,2}月）"
    return re.match(pattern1, line.strip().replace(" ", "")) is not None
           #or re.match(pattern2, line.strip().replace(" ", ""))


if __name__ == "__main__":
    print(match_chinese_data("(一九五二年一月一日)"))
    # print(match_chinese_data("（一九四五年八月十一日）"))
    arts = read_file(os.path.abspath("..") + "/test")
    for ar in arts:
        print(ar.title)
        print(ar.write_time)
        print(ar.background)
        print(ar.content)
        print(ar.annotation)
        print("--------------------")
    # print(arts.__len__())
    # print(ChineseToDate("一九四六年十月三日"))
    # print(ChineseToDate("一九四六年十一月"))

