import threading

from dto.question_dto import QuestionDto
from model.question_model import QuestionMap
from text2vec import SentenceModel, semantic_search

from util.csvUtil import read_csv_file

embedder = SentenceModel("shibing624/text2vec-base-chinese")


# 定义问题服务
class QuestionService:
    def __init__(self):
        self.question_map = {}  # 问题映射表
        self.question_list = {}  # 问题映射表
        self.gameId_embeddings = {}  # gameId对应的embeddings
        self.question_lock = threading.Lock()
        self.game_lock = threading.Lock()

        # 数字混存问题信息
        self.cacheQuestion = {}

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

                if qInfo not in infoRM:
                    infoRM[qInfo] = []

                if rInfo != "" and rInfo not in infoRM[qInfo]:
                    infoRM[qInfo].append(rInfo)

            # 保存问题集合
            question_map = QuestionMap()
            for val in infoQM:
                question_map.update(val, infoQM[val], infoRM[val])
            self.question_map["dtl"] = question_map
            self.question_list["dtl"] = question_list

            # 向量初始化
            self.initialize_gameId_embeddings(question_list)

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
                questionName = self.question_list['dtl'][hit['corpus_id']]
                score = hit['score']
                dto = QuestionDto(questionName, score)
                lst.append(dto)
        return QuestionDto.sort_list_by_score(lst)

    # doQuestion 问题结果处理
    def doQuestion(self, gameId, query_question, num):
        # 缓存查找，并且清空缓存
        if query_question in self.cacheQuestion:
            query_question = self.cacheQuestion[query_question]
        self.cacheQuestion.clear()

        # 问题查询
        lst = self.queryQuestion(gameId, query_question, num)
        # 结果处理
        if len(lst) == 0:
            return "<div>问题查找不存在，请输入重新提问题</div>\n"

        if lst[0].score < 0.2:
            return "<div" \
                   ">掌门您好，非常抱歉没有听懂您的意思，您可以输入【*】返回主菜单进行提问，如未能解决您的问题，请您输入“联系客服”，转人工咨询，详细描述下您遇到的问题并提供相应截图或视频，以便这边为您核实处理哦。</div>\n"

        answerStr = ""
        # 结果处理，匹配度达到1，直接返回问题信息，其他返回前5个问题
        if lst[0].score == 1:
            answerModelInfo = self.question_map[gameId].get(lst[0].questionId)
            answerStr = "<div>" + answerModelInfo.get_answer() + "</div>\n"

            if len(answerModelInfo.get_relation_question_list()) > 0:
                answerStr += "<div>更多相关问题，请回复相应数字：</div>\n"

            num = 1
            for question in answerModelInfo.get_relation_question_list():
                answerStr += "<div>" + str(num) + "、" + question + "</div>\n"
                self.cacheQuestion[str(num)] = question
                num += 1

        else:
            answerStr = "<div>您是否想咨询以下问题</div>\n"
            answerStr += "<div>输入【*】返回主菜单，请回复相应数字</div>\n"

            num = 1
            for i in range(len(lst)):
                if lst[i].score >= 0.4:
                    answerStr += "<div>" + str(num) + "、" + lst[i].questionId + "【相似度：" + str(
                        lst[i].score) + "】</div>\n"
                    self.cacheQuestion[str(num)] = lst[i].questionId
                    num += 1
        return answerStr
