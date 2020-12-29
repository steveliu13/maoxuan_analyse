# 文章的模型
class Article:
    def __init__(self, title, write_time, background, content, annotation):
        # 标题
        self.title = title
        # 创作时间
        self.write_time = write_time
        # 背景
        self.background = background
        # 内容
        self.content = content
        # 注释
        self.annotation = annotation


