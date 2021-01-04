import os


from read_file.file_parser import read_file

# 获取所有时期-目录
def generate_catalog(file_path):
    result = []
    for dir in os.listdir(file_path):
        if os.path.isdir(file_path+"/"+dir):
            result.append(dir)
    return result


# 获取每年的文章
def generate_year_article(file_path):
    result = {}
    periods = generate_catalog(file_path)
    articles = []
    for period in periods:
        articles.extend(read_file(file_path + "/" + period))
    for article in articles:
        if article.write_time.year not in result.keys():
            result[article.write_time.year] = []
            result[article.write_time.year].append(article.content)
        else:
            result[article.write_time.year].append(article.content)

