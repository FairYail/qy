import threading
from typing import List


# 定义问题结构体
class QuestionModel:
    def __init__(self, answer: str, relation_question_list: List[str]):
        self.answer = answer
        self.relation_question_list = relation_question_list

    def get_answer(self):
        return self.answer

    def set_answer(self, answer):
        self.answer = answer

    def get_relation_question_list(self):
        return self.relation_question_list

    def set_relation_question_list(self, relation_question_list):
        self.relation_question_list = relation_question_list

    def __hash__(self):
        return hash((self.answer, tuple(self.relationQuestionList)))

    def __eq__(self, other):
        return self.answer == other.answer and set(self.relationQuestionList) == set(other.relationQuestionList)


# 每个游戏对应一个该集合定义问题映射表
class QuestionMap:
    def __init__(self):
        self.lock = threading.Lock()
        self.questions = {}

    def update(self, question: str, answer: str, relation_question_list: List[str]):
        with self.lock:
            self.questions[question] = QuestionModel(answer, relation_question_list)

    def get(self, question: str):
        with self.lock:
            return self.questions.get(question)
