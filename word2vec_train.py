import multiprocessing
import os

import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

from read_file.file_parser import read_file
from util import DataUtil
from wordCloud import generate_catalog
from word_process.cut_util import import_stop_words

#训练word2vec模型
def trainModel():
    #获取训练数据
    total_data =[]
    pds = generate_catalog(os.path.abspath(".") + "/文本")
    for pd in pds:
        articles = read_file(os.path.abspath(".") + "/文本" + "/" + pd)
        for article in articles:
            total_data.append(article.content)
            total_data.append(article.background)
            total_data.append(article.annotation)
    #加载停用词表
    stop_words = import_stop_words()
    #分词
    write_data = []
    i = 0
    for line in total_data:
        i += 1
        if i % 100 == 0:
            print('当前进度：第' + str(i) + '行')
        temp = ''
        # 断句
        sentences = DataUtil.spiltString(line)
        for sentence in sentences:
            sentence = DataUtil.removeSymbol(sentence)
            sentence = DataUtil.removeBrackets(sentence)
            # 每行单独分词，实体加在后面
            words = jieba.cut(sentence)
            for word in words:
                if word not in stop_words :
                    temp += ' ' + word + ' '
        write_data.append(temp)

    DataUtil.writeList(write_data, 'after_cut.txt')
    print('分词写入完毕')
    model = Word2Vec(LineSentence('after_cut.txt'), size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())
    model.save( 'maoxuan.model')
    model.wv.save_word2vec_format('maoxuan.vector', binary=False)
    print('训练完毕')


#寻找关联度最高的词
def find_related_word():
    maoxuan_model = Word2Vec.load(os.path.abspath(".")+"/maoxuan.model")
    wd_path = os.path.abspath(".")+"/resource/"
    words_read = open(wd_path+"比较词汇.txt", 'r', encoding='utf-8')
    words = [line.strip() for line in words_read]
    write_w2v_result(words, maoxuan_model)



def write_w2v_result(words, maoxuan_model):
    word_sims = []
    for word in words:
        if word not in maoxuan_model:
            continue
        word_sims.append((word, maoxuan_model.most_similar(word)[0][0], maoxuan_model.most_similar(word)[0][1]))
    with open("分析结果/word2vec分析结果.txt", 'w', encoding='utf-8')as fp:
        for ws in word_sims:
            fp.write(ws[0]+ " " + ws[1] + " "+ str(ws[2])+'\n')


if __name__=="__main__":
    #print(os.path.abspath("."))
    #trainModel()
    find_related_word()