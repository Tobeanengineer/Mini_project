# -*- coding: utf-8 -*-

"""
Spyder Editor

This is a temporary script file.
"""

# 9/21 파이썬 데이터처리 세미나 정리파일

import pandas as pd
import numpy as np
import seaborn as sns
import folium
import matplotlib.pyplot as plt

df_store = pd.read_csv("C:\\Users\\Kim Chanwoo\\Downloads\\information_201906_01.csv")
# 판다스를 이용해 공공데이터 csv파일을 읽어오고 변수 저장

drop_columns = ["상권업종중분류코드", "상권업종소분류코드", 
                "건물관리번호", "표준산업분류코드", "표준산업분류명", 
                "지번부번지", "층정보", "건물명", "호정보", 
                "지점명", "건물부번지", "동정보"] 
# 결측치가 너무 많고 쓸모없는 컬럼을 제거

df_store = df_store.drop(drop_columns, axis=1) 
# 불필요한 컬럼을 제거, 제거하고 남은 값을 원래 변수에 다시 저장
coffee = df_store[df_store['상권업종소분류명'].str.contains('커피')]
#파일 내부 상권업종소분류코드 안 커피라는 값을 가진 요소를 리스트화, coffee라는 변수를 만듬

df_seoul = df_store.loc[df_store['시도명'].str.startswith('서울')].copy()
# 서울에 위치하는 업소들을 리스트로 만들어 저장
df_seoul['상호명_소문자'] = df_seoul['상호명'].str.lower() #영문 상호명을 소문자화
df_cafe = df_seoul[df_seoul['상호명_소문자'].str.contains('스타벅스|starbucks|STARBUCKS|이디야|ediya|EDIYA')]

df_cafe.loc[df_cafe['상호명'].str.contains('스타벅스|starbucks|STARBUCKS'), '브랜드명'] = '스타벅스'
df_cafe['브랜드명'] = df_cafe['브랜드명'].fillna('이디야')


# 위도와 경도를 토대로 한 좌표 시각화 과정

ax = df_cafe[df_cafe["브랜드명"] == '스타벅스' ].plot.scatter(x='경도', y='위도',
            color='g', label='스타벅스')
df_cafe[df_cafe['브랜드명'] == '이디야'].plot.scatter(x='경도', y='위도',
       color='b', label='이디야', grid=True, figsize=(10, 7), ax=ax)




geo_df = df_cafe
map = folium.Map(location=[geo_df['위도'].mean(), geo_df['경도'].mean()],
                              zoom_start=12, tiles='Stamen Toner')
for n in geo_df.index:
    popup_name = geo_df.loc[n, '상호명'] + '-' + geo_df.loc[n, '도로명주소']
    if geo_df.loc[n, '상호명'] == '스타벅스':
        icon_color = 'green'
    else: icon_color = 'blue'
    
folium.CircleMarker(
        location=[geo_df.loc[n,'위도'], geo_df.loc[n, '경도']],
        radius=3,
        popup=popup_name,
        color= icon_color,
        fill=True,
        fill_color=icon_color
    ).add_to(map)

print(map)



