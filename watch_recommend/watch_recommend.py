import pandas as pd

genre_data = pd.read_csv("./data/data_for_watch_recommend.csv", encoding="utf-8")

# 러닝 타임 기반 추천(사람과 상관 없이 공통 추천)
# 추천에 사용할 시청 시간 기반 비율 결과 데이터를 저장
# 추천은 별도의 파일의 함수에서 수행
def runningtime_recommendation():
    # 시청 기록을 저장할 dict
    watch_dict = {}
    
    # 데이터프레임을 순회하면서 러닝 타임의 합계와 시청 횟수 계산
    for _, item in genre_data.iterrows():
        running_time = item['disp_rtm_s']
        watch_time = item['use_tms']
        content_name = item['asset_nm_new']

        # 아직 dict 가 생성되지 않은 경우
        if content_name not in watch_dict:
            watch_dict[content_name] = [watch_time, running_time, 1]
        # 이미 dict 에 데이터가 들어있는 경우
        else:
            value = watch_dict[content_name]
            watch_dict[content_name] = [value[0] + watch_time, value[1] + running_time, value[2] + 1]
    
    # 러닝타임 대비 시청 시간 비율 계산
    for item in watch_dict:
        w, r, times = watch_dict[item]
        if r != 0.0:
            watch_dict[item] = [w / r, times]
        else:
            watch_dict[item] = [0, times]
            
    # 시청 횟수 기준 설정
    watch_times_limit = 5
    del_times_list = []
    
    # 시청 횟수 기준 이하인 리스트 생성
    for item in watch_dict:
        if watch_dict[item][1] <= watch_times_limit:
            del_times_list.append(item)
    # 시청 횟수가 기준 이하인 데이터 삭제        
    for item in del_times_list:
        del(watch_dict[item])
        
            
    # 러닝 타임 대비 시청 시간 비율 순서대로 정렬
    sorted_dict = sorted(watch_dict.items(), key = lambda item: item[1], reverse = True)

    rec_list = []
    # 러닝 타임 대비 시청 시간 비율이 높은 순서대로 상위 10개 출력
    for item in sorted_dict[:10]:
        rec_list.append(item)

    rec_df = pd.DataFrame(rec_list)
    rec_df.to_csv("./data/watch.csv", index=False)

runningtime_recommendation()