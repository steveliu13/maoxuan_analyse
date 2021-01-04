# 情感分析的结果
class EmotionResult:
    def __init__(self, title, write_time, score, best):
        # 标题
        self.time = title
        # 年份/阶段
        self.write_time = write_time
        # 分值
        self.score = score
        # 最低、最高
        self.best = best