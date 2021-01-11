import datetime
import os

from snownlp import SnowNLP
from read_file.file_parser import read_file
from read_file.file_util import generate_catalog
from util.DataUtil import spiltString


def generate_article_emotion(content):
    lines = spiltString(content)
    count = 1
    score = 0
    for line in lines:
        if line.__len__()>1:
            line_score = SnowNLP(line).sentiments
            score += line_score
            count += 1
    return score/count

def analyse():
    write_data = []
    period_articles = {}
    failed = []
    #1. 获取不同时间段的所有文章
    pds = generate_catalog(os.path.abspath(".") + "/文本")
    for pd in pds:
        articles = read_file(os.path.abspath(".") + "/文本" + "/" + pd)
        period_articles[pd] = articles
    #1.1 排序选出该时间段最高和最低情绪的文章
    for pd in period_articles.keys():
        es_worst = ("", "", 100, "", "")
        es_best = ("", "", -100, "", "")
        for art in period_articles[pd]:
            text = art.content
            if len(str(text).strip()) == 0:
                failed.append(art.title)
                continue
            emotion_score = generate_article_emotion(text)
            print(art.title + " " + str(emotion_score))
            if emotion_score > es_best[2]:
                es_best=(art.title, art.write_time, emotion_score, pd, True)
            if emotion_score < es_worst[2]:
                es_worst = (art.title, art.write_time, emotion_score, pd, False)
        write_data.append(es_best)
        write_data.append(es_worst)

    #2. 获取不同年份的所有文章
    year_articles = {}
    periods = generate_catalog(os.path.abspath(".") + "/文本")
    articles = []
    for period in periods:
        articles.extend(read_file(os.path.abspath(".") + "/文本" + "/" + period))
    for article in articles:
        if article.write_time is not None:
            if article.write_time.year not in year_articles.keys():
                year_articles[article.write_time.year] = []
                year_articles[article.write_time.year].append(article)
            else:
                year_articles[article.write_time.year].append(article)

    #2.1 排序选出该年最高和最低情绪的文章
    for year in year_articles.keys():
        es_worst = ("", "", 100, "", "")
        es_best = ("", "", -100, "", "")
        for art in year_articles[year]:
            text = art.content
            if len(str(text).strip()) == 0:
                failed.append(art.title)
                continue
            emotion_score = generate_article_emotion(text)
            print(art.title + " " + str(emotion_score))
            if emotion_score > es_best[2]:
                es_best = (art.title, art.write_time, emotion_score, year, True)
            if emotion_score < es_worst[2]:
                es_worst = (art.title, art.write_time, emotion_score, year, False)
        write_data.append(es_best)
        write_data.append(es_worst)

    #3 整理到txt中

    with open("分析结果/情感分析结果.txt", "a", encoding='utf-8') as fp:
        for es in write_data:
            emotion = ""
            if es[4] :
                emotion = "最好"
            else:
                emotion = "最坏"
            fp.write(str(es[0]) + " " + str(es[1]) + " " +
                     str(es[2]) + " " + str(es[3]) + " " + emotion+"\n")
    with open("情感分析结果失败.txt", "a", encoding='utf-8') as fp:
        for fa in failed:
            fp.write(fa+"\n")

if __name__ == "__main__":
    analyse()
    # snow_result = SnowNLP("今天天气不错")
    # print(emotion_score)