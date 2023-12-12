from konlpy.tag import Twitter
import math
import scipy as sp
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import pandas as pd

# 데이터 원본을 가져와서 필요한 데이터만 사용
"""
origin_data = pd.read_csv(r'C:\\Users\\USER\\Desktop\\project\\test\\data\\final_vod.csv', encoding = 'cp949')
smry_data = origin_data[['subsr', 'SMRY']]
smry_data.to_csv("./data/smry_data.csv")
"""

# 줄거리를 포함한 데이터 가져오기
smry_data = pd.read_csv(r"./smry_recommend/data/smry_data.csv")

# 세부 장르 데이터 가져오기
open_file = open(r'./smry_recommend/data/detail_genre.txt', 'r', encoding = 'utf8')
text = open_file.read()
open_file.close()

# 세부 장르 리스트 생성
data_list = text.split('\n')

# data_list 의 마지막에 공백이 추가되므로 공백 제거
data_list = data_list[:-2]


# 불용어 처리
with open(r'./smry_recommend/data/stopword.txt', 'r', encoding = 'utf-8') as f:
    stopwords = f.read()
stopwords_list = stopwords.split('\n')

word_dict_data = {}

# 각 세부 장르 별로 단어 리스트 생성하고 저장
for detail_genre in data_list:
    # 각 세부 장르에 대해 단어 데이터 가져오기
    open_file = open(r'./smry_recommend/data/' + detail_genre + '_words.txt', 'r', encoding = 'utf8')
    text = open_file.read()
    
    # 파일 닫기
    open_file.close()
    
    # 각 단어 분리하기
    text_list = text.split('\n')
    text_list = text_list[:-2] # 마지막의 공백 제외
    
    # 각 장르별 주요 단어 찾기
    spliter = Twitter()
    nouns_for_dictionary = spliter.nouns(text)
    ko = nltk.Text(nouns_for_dictionary, name = detail_genre)
       
    # 불용어 제거
    ko1 = [each_word for each_word in ko if each_word not in stopwords_list]
    ko = nltk.Text(ko1, name = detail_genre)
    word_dict = dict(ko.vocab())
    
    # 단어 리스트를 dict 형태로 저장
    word_dict_data[detail_genre] = word_dict


# 장르별 벡터 저장
word_vector_dict = {}
vectorizer = CountVectorizer(min_df = 0.05)
    
# dict 형태로 저장되어 있는 단어 데이터를 읽고
# 각 단어들을 모아서 하나의 문장으로 만든 다음 저장
for detail_genre in data_list:
    contents_tokens = word_dict_data[detail_genre]

    # 벡터화를 위해 단어들을 가지고 문장 생성
    contents_for_vect = []
    sentence = ''
    # 토큰 단위로 구분된 문장을 생성
    for content in contents_tokens:
        sentence += ' ' + content

    # 생성한 문장을 리스트에 추가
    contents_for_vect.append(sentence)
    
    word_vector_dict[detail_genre] = contents_for_vect


#거리 구해주는 함수 생성
def dist_raw(v1, v2):
    # 차이를 계산
    delta = v1 - v2
    
    return sp.linalg.norm(delta.toarray())

# 사용자 번호를 입력으로 사용
def smry_recommend(subsr_num):
    # 사용자 번호가 일치하는 데이터 중 줄거리만 가져오기
    user_data = smry_data[smry_data['subsr'] == subsr_num]['SMRY']
    
    smry_list = []
    # 데이터를 순회하면서 줄거리 저장
    for item in user_data:
        if item not in smry_list:
            smry_list.append(item)
        
    smry_sentence = ''
    for smry in smry_list:
        smry_sentence += (smry + ' ')
        
    # 샘플 문장 토큰화
    spliter = Twitter()
    sample_words = spliter.nouns(smry_sentence)

    # 가장 거리가 짧은 세부 장르 계산용
    min_distance = 65536
    min_detail_genre = 'None'

    
    # 각 세부 장르별 거리 계산을 수행
    for detail_genre in data_list:
        vectorizer = CountVectorizer(min_df = 1) # 1번만 등장해도 단어 사전에 포함시키도록

        # 장르 별로 줄거리 불러오기 - dict 의 value
        contents_tokens = word_vector_dict[detail_genre]

        sentence = contents_tokens[0]

        # 생성한 문장을 리스트에 추가
        contents_for_vect = []
        contents_for_vect.append(sentence)

        # 피처 벡터화 - 띄어쓰기를 기준으로 벡터화
        X = vectorizer.fit_transform(contents_for_vect)

        # 샘플 줄거리 문장을 피처 벡터화
        new_content_vect = vectorizer.transform([smry_sentence])

        # 거리 계산
        post_vec = X.getrow(0) # 단어 문장이 1개이므로 첫번째인 0번 인덱스
        distance = dist_raw(new_content_vect, post_vec)

        # 세부 장르별 단어의 갯수를 세고 일정 갯수 이하이면 제외
        length = post_vec.shape[1]
        limit_length = 100
        limit_cor = 0.3
        if length < limit_length:
            pass

        else:
            # 일치율 계산하기
            count = 0
            for item in sample_words:
                if item in contents_tokens[0]:
                    count += 1

            cor = count / len(sample_words)

            # 일치율이 기준을 넘는 경우에만 거리를 계산
            if cor < limit_cor:
                pass

            else:
                # 결과 확인 - 장르와의 거리는 줄거리 단어의 길이를 가중치로 반영하여 계산
                weighted_distance = distance / (math.log10(length)) / cor
                '''
                print(detail_genre, ' 장르와의 거리는 : \t', weighted_distance, sep='') 
                # 1000을 곱한 이유는 쉽게 보기 위함
                print(detail_genre, ' 장르와의 거리(원본)는 : \t', distance, sep='')
                print(detail_genre, ' 장르와의 일치율은 : \t', cor * 100 , '%', sep='')
                print(detail_genre, ' 장르의 단어 길이는 : \t', length, '\n',sep='')
                '''

                if weighted_distance < min_distance:
                    min_distance = weighted_distance
                    min_detail_genre = detail_genre

    # 최종 결과         
    #print('가장 유사한 장르는 ', min_detail_genre, sep = '')
    return(min_detail_genre)