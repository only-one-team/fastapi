from fastapi import APIRouter
# 요청을 처리할 수 있는 APIRouter

from models import Todo
# 모델을 사용할 수 있도록 import

# 추천 모델 가져오기
from watch_recommend.recommend import watch_rec
from smry_recommend.smry_recommend import smry_recommend
from cast_recommend.cast_recommend import cast_recommend

# 유효한 subsr
subsr_list = [64154000, 64659000]

#라우터 객체 생성
todo_router = APIRouter()

#데이터를 저장할 list 생성
todo_list = []

#todo 요청을 post 방식으로 요청한 경우 처리
@todo_router.post("/todo")
#매개변수를 받아서 todo_list에 삽입
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
    "message" : "Data added successfully."
    }

# todo 요청을 get 방식으로 요청한 경우 처리
# subsr 을 받아서 데이터를 리턴하는 요청을 처리
@todo_router.get("/todo/{subsr_id}")
async def get_subsr_id(subsr_id : int) -> dict:
    for subsr in subsr_list:
        if subsr == subsr_id :
            smry_result = smry_recommend(subsr)
            cast_result = cast_recommend(subsr)
            return {
                "subsr" : subsr,
                "genre recommend" : smry_result,
                "cast recommend" : cast_result
            }

    return {
        "message" : "유효하지 않는 입력입니다."
    }

# 기본 주소
@todo_router.get("/todo")
async def showrecommend():
    watch_result = watch_rec()
    return{
        "message" : "test success",
        "watch based recommend result" : watch_result
    }