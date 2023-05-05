class CustomError(Exception):
    def __init__(self, err_code: int, err_msg: str):
        self.code = err_code
        self.message = err_msg
        super().__init__(self.message)
