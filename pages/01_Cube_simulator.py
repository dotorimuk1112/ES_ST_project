from elasticsearch import Elasticsearch
import streamlit as st
import random

# Elasticsearch 클라이언트 생성
es = Elasticsearch('http://localhost:9200')

# 인덱스 이름
index_name = 'cube_simul'

st.title("당신의 큐브 운을 점쳐보세요")
st.markdown("<h1 style='text-align: right;'>with MapleStory Open API</h1>", unsafe_allow_html=True)
st.subheader("500회만큼 큐브 시뮬레이터를 돌려서 당신의 등업 확률을 점검해드립니다.")
st.image(r'st-es-practice\image\proba.png')

# 큐브 시뮬레이션 확률 설정
questionable_cube_probabilities = {'에픽': 0.009901, '유니크': 0, '레전드리': 0}
black_cube_probabilities = {'에픽': 0.15, '유니크': 0.035, '레전드리': 0.014}

# 사이드바 레이아웃 설정
st.sidebar.header("큐브 종류와 목표 등급을 선택하세요.")
cube_options = ['수상한 큐브', '블랙 큐브']
cube_type = st.sidebar.selectbox('큐브 종류', cube_options)

grade_options = ['에픽', '유니크', '레전드리']
item_grade = st.sidebar.selectbox('목표 등급', grade_options)

if st.sidebar.button("버튼을 눌러 결과를 확인하세요"):
    # 인덱스가 이미 존재하면 삭제
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    
    # 큐브 시뮬레이션 실행 및 결과 Elasticsearch에 저장
    if cube_type == '수상한 큐브':
        for _ in range(500):
            result = '성공' if random.random() < questionable_cube_probabilities[item_grade] else '실패'
            document = {
                'cube_type': cube_type,
                'target_grade': item_grade,
                'result': result,
            }
            es.index(index=index_name, body=document)
    else:
        for _ in range(500):
            result = '성공' if random.random() < black_cube_probabilities[item_grade] else '실패'
            document = {
                'cube_type': cube_type,
                'target_grade': item_grade,
                'result': result,
            }
            es.index(index=index_name, body=document)



    # Elasticsearch에 대한 명시적인 갱신
    es.indices.refresh(index=index_name)

    # Elasticsearch에서 총 문서 수 및 성공 문서 수 조회
    query1 = {"query": {"bool": {"must": [{"match": {"cube_type.keyword": cube_type}},
                                        {"match": {"target_grade.keyword": item_grade}}]}}}
    query2 = {"query": {"bool": {"must": [{"match": {"result.keyword": "성공"}},
                                        {"match": {"cube_type.keyword": cube_type}},
                                        {"match": {"target_grade.keyword": item_grade}}]}}}
    response1 = es.search(index=index_name, body=query1)
    response2 = es.search(index=index_name, body=query2)
    total_documents = response1["hits"]["total"]["value"]
    success_documents = response2["hits"]["total"]["value"]

    # 결과 출력
    if cube_type == '수상한 큐브':
        st.text(f'당신이 {cube_type}을 이용해서 {item_grade} 등업에 도전한 횟수는 {total_documents}입니다.')
        st.text(f'{total_documents}만큼 도전했으면, 최소 {total_documents * questionable_cube_probabilities[item_grade]}만큼은 성공했어야 합니다.')
        st.text(f'근데 당신은 {success_documents}번 성공하셨네요?')
        if total_documents * questionable_cube_probabilities[item_grade] > success_documents:
            st.text('운이 안 좋으시네요. 앞으로는 좋으실 듯?')
        else:
            st.text('운 좋으시네요. 앞으로 계속 좋으실 듯?')
    elif cube_type == '블랙 큐브':
        st.text(f'당신이 {cube_type}을 이용해서 {item_grade} 등업에 도전한 횟수는 {total_documents}입니다.')
        st.text(f'{total_documents}만큼 도전했으면, 최소 {total_documents * black_cube_probabilities[item_grade]}만큼은 성공했어야 합니다.')
        st.text(f'근데 당신은 {success_documents}번 성공하셨네요?')
        if total_documents * black_cube_probabilities[item_grade] > success_documents:
            st.text('운이 안 좋으시네요. 앞으로는 좋으실 듯?')
        else:
            st.text('운 좋으시네요. 앞으로 계속 좋으실 듯?')
