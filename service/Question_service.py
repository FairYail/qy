import threading

from dto.question_dto import QuestionDto
from model.question_model import QuestionMap
from text2vec import SentenceModel, semantic_search

from util.csvUtil import read_csv_file

embedder = SentenceModel("GanymedeNil/text2vec-large-chinese")


# 定义问题服务
class QuestionService:
    def __init__(self):
        self.question_map = {}  # 问题映射表
        self.gameId_embeddings = {}  # gameId对应的embeddings
        self.question_lock = threading.Lock()
        self.game_lock = threading.Lock()

    # 初始化问题映射表
    def initialize_question_map(self):
        # 加载问题数据，初始化question_map
        with self.question_lock:
            # TODO 此处需要根据游戏分类哦
            # 读取数据到question_map
            dtlList = read_csv_file()
            infoQM = {}
            infoRM = {}
            question_list = []

            for val in dtlList:
                qInfo = val[0]  # 问题
                aInfo = val[1]  # 答案
                rInfo = val[2]  # 相关问题
                if qInfo not in question_list:
                    question_list.append(qInfo)

                if aInfo != "" and qInfo not in infoQM:
                    infoQM[qInfo] = aInfo

                if infoRM[qInfo] is None:
                    infoRM[qInfo] = []

                if rInfo != "" and rInfo not in infoRM[qInfo]:
                    infoRM[qInfo].append(rInfo)

            # 保存问题集合
            question_map = QuestionMap()
            for val in infoQM:
                question_map.update(val, infoQM[val], infoRM[val])
            self.question_map["dtl"] = question_map

            # 向量初始化
            self.initialize_gameId_embeddings(question_list)
            pass

    # 向量初始化
    def initialize_gameId_embeddings(self, question_list):
        # 加载问题数据，初始化gameId_embeddings
        with self.game_lock:
            self.gameId_embeddings = {"dtl": embedder.encode(question_list)}
            pass

    # queryQuestion 问题查询
    def queryQuestion(self, gameId, query_question, num):
        lst = []
        with self.game_lock:
            # gameId对应的embeddings
            corpus_embeddings = self.gameId_embeddings[gameId]
            query_embedding = embedder.encode(query_question)
            # 问题映射表
            hits = semantic_search(query_embedding, corpus_embeddings, top_k=num)
            hits = hits[0]
            for hit in hits:
                questionName = hit['corpus_id']
                score = hit['score']
                dto = QuestionDto(questionName, score)
                lst.append(dto)
        return QuestionDto.sort_list_by_score(lst)

    # doQuestion 问题结果处理
    def doQuestion(self, gameId, query_question, num):
        # 问题查询
        lst = self.queryQuestion(gameId, query_question, num)
        # 结果处理
        if len(lst) == 0:
            return "问题查找不存在，请输入重新提问题"

        answerStr = ""
        # 结果处理，匹配度达到1，直接返回问题信息，其他返回前5个问题
        if lst[0].score == 1:
            answerModelInfo = self.question_map[gameId].get(lst[0].questionId)
            answerStr = answerModelInfo.get_answer() + "\n"
            for question in answerModelInfo.get_relation_question_list():
                answerStr += "1、" + question + "\n"
        return answerStr
