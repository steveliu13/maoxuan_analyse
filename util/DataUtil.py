import re
import os


#从当前文件夹中读取数据到List中
def readData(fileName):
    test_data = []
    for line in open(fileName, 'r', encoding='utf-8'):
        test_data.append(line.strip())
    return test_data

#吧list中的数据存储到本地
def writeList(list_data, fileName):
    with open(fileName, 'w', encoding='utf-8')as fp:
        for l in list_data:
            fp.write(l+'\n')

#把list中内容加到文本后面
def appendFile(list_data, fileName):
    with open(fileName, 'a', encoding='utf-8')as fp:
        for l in list_data:
            fp.write(l+'\n')

# 移除字符串中的大部分标点符号
def removeSymbol(string):
    string = re.sub("[\s+\!_,$%^*(+\"\')\[\]|[+()?【】／‘’“”！，。？、~@#￥%……&*·•°～\-：—一（）《》"
                    "⑴⑵⑶]+", "", string)
    #string = re.sub('[‘’“”!"#$%&\'()*+,./:;<=>?@[\\]￥^_`{|}（）《》-]+、','',string)
    return string

#移除所有数字字母
def removeNumberAlpha(string):
    string = re.sub("[a-zA-Z0-9⑴-⒃]+", "", string)
    return string

#去掉中文
def removeChn(input):
    regex = re.compile('[\u3400-\u9FFF]+')
    matchArray = regex.sub('', input)
    return matchArray
    #return re.sub('(\s[\u4E00-\u9FA5]+)|([\u4E00-\u9FA5]+\s)', '', input)

#是否纯中文
def isAllChn(text):
    result = re.match('^[\u3400-\u9FFF]+$', text)
    return result is not None

#去掉括号里的内容
def removeBrackets(sentence):
    regex = re.compile('\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】|\\(.*?\)')
    matchArray = regex.sub('', sentence)
    return matchArray

#根据标点符号断句
def spiltString(sentence):
    pattern = '\。|\；|\;|\!|\！|\?|\？|:'
    return re.split(pattern, sentence)

#读取多个文件的内容到一个Set中
def readManyFiles(file_list):
    output = set()
    for file in file_list:
        for temp in readData(file):
            output.add(temp)
    return output

#判断是否是全英文字母+数字
def isAllEnNum(word):
    result = re.match('^[a-zA-Z0-9]+$', word)
    return result is not None

#判断是否是全数字
# def isAllNum(word):
#     result = re.match('^[0-9]+$', word)
#     return result is not None

if __name__=='__main__':
    # text = '0126aa545'
    # print(isAllNum(text))
    # search = 'abc'
    # start = 0
    # while True:
    #     index = text.find(search, start)
    #     if index == -1:
    #         break
    #     print("%s found at index %d" % (search, index))
    #     start = index + 1
    #print(palces)
    #print(isAllEn('abc'))
    #print(isAllEn('啊啊aa'))
    #print(spiltString('飞机，航空器，；'))
    #print(removeChn('海燕A-78导弹'))
    #print(difflib.SequenceMatcher(None, '埃塞克斯', '埃塞克斯号CV-9航空母舰').ratio())
    print(removeSymbol('“埃塞克斯”号(CV-9)航空母舰'))
    #print(removeBrackets('入围者需要考虑(aaa)从（蹦蹦蹦）摩天大楼的节能'))
    #print('\t'.join(spiltString('入:围;者"需\'要：考；虑,从“蹦”蹦‘蹦.摩’天，大!楼?的。节！能？啊啊')))
