from fastapi import FastAPI
from todo import todo_router

# fastapi 객체 생성
app = FastAPI()


# 기본 요청(/ 주소에 get 요청)이 오면 수행
# 요청에 따라 아래의 함수를 수행하고 결과를 리턴함
@app.get("/")
async def welcomefunc() -> dict:
    return {
        "message" : "welcome message"
    }

# fastapi 객체가 라우터를 포함하도록 만듦
app.include_router(todo_router)
