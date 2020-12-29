import jieba

from read_file.stop_words import import_stop_words
from util import DataUtil

# 为词云分词
def cut_word_4_cloud(lines):
    stop_words = import_stop_words()
    result = []
    #分词
    for line in lines:
        # 断句
        sentences = DataUtil.spiltString(line)
        #sentences = line.split("。")
        for sentence in sentences:
            # 去掉标点符号和数字
            sentence = DataUtil.removeSymbol(sentence)
            sentence = DataUtil.removeNumberAlpha(sentence)
            # 每行单独分词，实体加在后面
            seg_list = jieba.cut(sentence)
            for key in seg_list:
                # 去除停用词，去除单字，去除非字符串类型的词
                if not (key.strip() in stop_words) and len(key) > 1 and type(key) is str:
                    result.append(key)

    return result