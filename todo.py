from fastapi import APIRouter
# 요청을 처리할 수 있는 APIRouter

from models import Todo
# 모델을 사용할 수 있도록 import

from os import path
# 파일 존재 여부 검사를 위해 import

# 추천 모델 가져오기
from watch_recommend.recommend import watch_rec
from smry_recommend.smry_recommend import smry_recommend
from cast_recommend.cast_recommend import cast_recommend, cast_data

# 유효한 subsr
subsr_list = [64154000, 64659000]

#라우터 객체 생성
todo_router = APIRouter()

#데이터를 저장할 list 생성
todo_list = []

#todo 요청을 post 방식으로 요청한 경우 처리
@todo_router.post("/todo")
#매개변수를 받아서 todo_list에 삽입
async def add_data(todo: Todo) -> dict:
    number = todo.subsr
    # Post 방식으로 요청을 전달하면 
    # 그 subsr 입력이 유효한 subsr 인 경우에
    # cast_recommend 를 사용할 수 있도록 데이터 파일을 생성
    if number in subsr_list:
        # 이미 데이터 파일이 있는 경우 데이터 생성은 생략
        if path.exists(r"C:\Users\USER\Desktop\project\Recommendation Fastapi\cast_recommend\data\\" + str(number) + ".csv"):
            return {
                "message" : "이미 존재하는 데이터에 대한 입력"
            }
        # 데이터 파일이 없는 경우 데이터 파일을 생성
        else:
            # subsr 을 입력 받아서 데이터를 생성
            cast_data(number)
            return {
                "message" : "Data created successfully."
            }
    # 유효하지 않은 사용자 번호 입력에 대한 처리
    else:
        return {
            "message" : "Invalid Subsr"
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
                "genre_recommend" : smry_result,
                "cast_recommend" : cast_result
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