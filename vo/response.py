from enum import Enum


# 定义返回值
class Response:
    ERR_CODE_SUCCESS = 0
    ERR_MSG_SUCCESS = ""

    def __init__(self, err_code, err_msg, data):
        self.meta = {"errCode": err_code, "errMsg": err_msg}
        self.data = data

    @classmethod
    def success(cls, data):
        return cls(cls.ERR_CODE_SUCCESS, cls.ERR_MSG_SUCCESS, data)

    @classmethod
    def fail(cls, err_code, err_msg):
        return cls(err_code, err_msg, None)