import os

from util import DataUtil


def import_stop_words():
    path = os.path.abspath(".")+"/resource/cn_stopwords.txt"
    stop_words = set()
    stopwords_list = open(path, "r", encoding='utf-8')
    stop_words.update(stopwords_list)

    return stop_words