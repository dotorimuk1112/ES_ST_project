import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
import pandas as pd
from elasticsearch import Elasticsearch
# from elastic_api import search_index, search_index_with_date_range

es = Elasticsearch('http://localhost:9200')

questionable_cube_probabilities = {'에픽': 0.009901, '유니크': 0, '레전드리': 0}
black_cube_probabilities = {'에픽': 0.15, '유니크': 0.035, '레전드리': 0.014}

st.title("당신의 큐브 운은?")
st.markdown("<h1 style='text-align: right;'>with MapleStory Open API</h1>", unsafe_allow_html=True)
st.image(r'st-es-practice\image\proba.png')
st.text('')
st.text('')
st.text('')
st.markdown(
    """     <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width:250px;}     </style>
    """, unsafe_allow_html=True )

st.sidebar.header("큐브 종류와 목표 등급을 선택하세요.")
cube_options = ['수상한 큐브', '블랙 큐브']
cube_type = st.sidebar.selectbox('큐브 종류', cube_options)

grade_options = ['에픽', '유니크', '레전드리']
item_grade = st.sidebar.selectbox('목표 등급', grade_options)

query1 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"cube_type.keyword": cube_type}},
                {"match": {"potential_option_grade.keyword": item_grade}}
            ]
        }
    }
}

query2 = {
    "query": {
        "bool": {
            "must": [
                {"match": {"item_upgrade_result": "성공"}},
                {"match": {"cube_type.keyword": cube_type}},
                {"match": {"potential_option_grade.keyword": item_grade}}
            ]
        }
    }
}

response1 = es.search(index="ins_test", body=query1)
response2 = es.search(index="ins_test", body=query2)
total_documents = response1["hits"]["total"]["value"]
success_documents = response2["hits"]["total"]["value"]

if cube_type == '수상한 큐브':
    expec = total_documents * questionable_cube_probabilities[item_grade]
    st.image(r'st-es-practice\image\occult.PNG', width=200)
else:
    expec = total_documents * black_cube_probabilities[item_grade]
    st.image(r'st-es-practice\image\black.PNG', width=200)

if st.sidebar.button("버튼을 눌러 결과를 확인하세요"):
    # 결과 출력

    st.text('')
    st.text('')
    if expec == 0:
        st.subheader(f'{cube_type}로는 {item_grade} 등급에 도달할 수 없습니다.')
    else:
        if expec > success_documents:
            st.text(f'당신이 {cube_type}을 이용해서 {item_grade} 등업에 도전한 횟수는 {total_documents}회 입니다.')
            st.text(f'{total_documents}회 도전했으면, 성공 기대값은 {expec}회입니다.')
            st.subheader(f'근데 당신은 {success_documents}번밖에 성공 못 하셨네요??')
            st.subheader('운이 안 좋으시네요. 앞으로는 좋으실 듯?')

        else:
            st.text(f'당신이 {cube_type}을 이용해서 {item_grade} 등업에 도전한 횟수는 {total_documents}회 입니다.')
            st.text(f'{total_documents}회 도전했으면, 성공 기대값은 {expec}회입니다.')
            st.subheader(f'근데 당신은 {success_documents}번이나 성공하셨네요?')
            st.subheader('운 좋으시네요. 앞으로 계속 좋으실 듯?')