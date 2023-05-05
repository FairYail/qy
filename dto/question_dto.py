# 定义问题结构体
class QuestionDto:
    def __init__(self, questionId: str, score: float):
        self._questionId = questionId
        self._score = score

    @property
    def questionId(self):
        return self._questionId

    @questionId.setter
    def questionId(self, value):
        self._questionId = value

    @property
    def score(self):
        return round(self._score, 4)

    @score.setter
    def score(self, value):
        self._score = round(value, 4)

    @staticmethod
    def sort_list_by_score(lst):
        return sorted(lst, key=lambda x: x.score, reverse=True)
