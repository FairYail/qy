#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

from vo.customer_err import CustomError
from vo.response import Response
from consts.code_resp import Err_Question_Empty, Err_GameId_Empty, Err_System
from service.Question_service import QuestionService

app = FastAPI()

# 允许跨域请求的来源
origins = [
    "http://localhost",
    "http://43.156.32.180",
    "http://customer-ai.hortorgames.com/",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件目录，这里将静态文件放在项目的 static 目录中
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板引擎，这里使用 Jinja2
templates = Jinja2Templates(directory="templates")

# 初始化问题映射表
question_service = QuestionService()
question_service.initialize_question_map()
print("csv初始化完成")


@app.get("/getAnswer")
def get_answer(question: str = Query(None)):
    if question is None:
        return Response.fail(Err_Question_Empty.code, Err_Question_Empty.message)
    try:
        lst = question_service.doQuestion("dtl", question, 10)
        return Response.success(lst)
    except CustomError as e:
        return Response.fail(e.code, e.message)
    except Exception as e:
        return Response.fail(Err_System.code, str(e))


# 路由：渲染首页
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=80, reload=True)
