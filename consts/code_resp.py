from vo.customer_err import CustomError

Err_System = CustomError(10000, "系统异常")
Err_Question_Empty = CustomError(10001, "question is empty")
Err_GameId_Empty = CustomError(10002, "gameId is empty")
