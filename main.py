#!/usr/bin/env python3
from fastapi import FastAPI, Request
import requests

from vo.customer_err import CustomError
from vo.response import Response
from consts.code_resp import Err_Question_Empty, Err_GameId_Empty, Err_System
from service.Question_service import QuestionService

app = FastAPI()

# 初始化问题映射表
question_service = QuestionService()
question_service.initialize_question_map()


# 初始化向量
@app.get("/getAnswer/{gameId}}")
def get_answer(gameId: str, question: str = None):
    if question is None:
        return Response.fail(Err_Question_Empty.code, Err_Question_Empty.message)
    if gameId is None:
        return Response.fail(Err_GameId_Empty.code, Err_GameId_Empty.message)
    try:
        lst = question_service.doQuestion(gameId, question, 10)
        return Response.success(lst)
    except CustomError as e:
        return Response.fail(e.code, e.message)
    except Exception as e:
        return Response.fail(Err_System.code, str(e))


@app.get("/")
def index(request: Request):
    html = """
        <html>
            <body>
                <form method="get">
                    <label for="value">Enter a value:</label>
                    <input type="text" name="value" id="value">
                    <button type="submit" name="submit">Get Data</button>
                </form>
                <div>
                    %s
                </div>
            </body>
        </html>
    """
    response_data = ""
    if "value" in request.query_params:
        value = request.query_params["value"]
        response = requests.get(f"https://localhost:80/getAnswer/{value}?gameId=dtl")
        json_data = response.json()
        if "meta" in json_data and "errCode" in json_data["meta"]:
            if json_data["meta"]["errCode"] == 0:
                response_data = json_data["data"]
            else:
                response_data = json_data["meta"]["errMsg"]
    return html % response_data
