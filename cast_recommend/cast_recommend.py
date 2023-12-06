import pandas as pd
from collections import Counter

view_data = pd.read_csv(r"C:\Users\USER\Desktop\project\test\cast_recommend\data\cast_data.csv")

# 사용자 번호를 입력받아서 시청한 컨텐츠에 출연한 출연진 기반 추천

# 사용자 번호를 받아서 이와 관련된 점수 데이터를 생성하고 저장
def cast_data(subsr_num):
    user_data = view_data[view_data['subsr'] == subsr_num]
    
    # 출연진 정보를 저장할 list
    actr_list = []

    # 시청 데이터를 순회하면서 출연진 정보를 저장
    for _, item in user_data.iterrows():
        actr = item['ACTR_DISP']
        
        if ',' in actr:
            item_list = actr.split(',')
        else:
            item_list = [actr]

        for actr in item_list:
            if actr != '-':
                actr_list.append(actr)
            
    count = Counter(actr_list)

    # 가장 많이 출연한 상위 N 명의 출연진 정보
    N_people = 30
    bestN_actr = count.most_common(N_people)
    
    # 상위 N위 출연진에 대해 가중치 설정
    score_sum = 0
    for actr_score in bestN_actr:
        score_sum += actr_score[1]

    w_bestN = []
    # 출연진 가중치 점수를 소수 아래 2자리 반올림
    for actr_score in bestN_actr:
        w_bestN.append([actr_score[0], round((actr_score[1] / score_sum), 2)])
        
        
    actr_score_list = []
    # 각 행을 순회하면서 출연진 정보에 대한 점수를 더해서 데이터 생성
    for _, item in user_data.iterrows():
        score_data = 0

        for name_score in w_bestN:
            if name_score[0] in str(item['ACTR_DISP']):
                score_data += name_score[1]
        actr_score_list.append(score_data)

    # 기존 데이터에 컬럼 추가
    user_data['ATCR_SCORE'] = actr_score_list

    # 출연진 점수를 기준으로 순위 부여
    user_data['rank'] = user_data['ATCR_SCORE'].rank(method = 'min', na_option = 'bottom',
                                                    ascending = False)
    
    # 출연진 점수 및 순위 데이터 저장
    save_data = user_data[['subsr','asset_nm_new', 'ATCR_SCORE', 'rank']]
    save_data.to_csv(r"C:\Users\USER\Desktop\project\Recommendation Fastapi\cast_recommend\data\\" + str(subsr_num) + ".csv")
    


# 저장되어 있는 출연진 기반 점수 데이터를 가지고 추천
# 관련 데이터가 저장되어 있지 않은 경우는 유효하지 않은 사용자 번호로 처리  
def cast_recommend(subsr_num):
    try:
        data = pd.read_csv(r"C:\Users\USER\Desktop\project\test\cast_recommend\data\\" + str(subsr_num) + ".csv")
        count_data = data.groupby(['asset_nm_new', 'ATCR_SCORE']).count().reset_index()
        
        # ATCR_SCORE 를 기준으로 정렬을 수행
        sorted_ac_data = count_data.sort_values(by = ['ATCR_SCORE', 'asset_nm_new'], ascending = False)
        
        # 상위 10개 컨텐츠의 정보를 리스트로 생성
        top10 = list(sorted_ac_data['asset_nm_new'][:10])
        return(top10)
    except:
        return(["Invalid Subsr"])