# Elasticsearch-Streamlit 프로젝트

분류: ELK

설명: 메이플스토리 open API를 활용한 Elasticsearch-Streamlit toy project

사용 데이터: https://openapi.nexon.com/

사용 기술 스택: Elasticsearch, Python, Streamlit

![proba.png](https://github.com/dotorimuk1112/ES_ST_project/blob/main/image/proba.png)

■ 프로젝트 취지

- Python 활용 Elasticsearch 데이터 CRUD 연습
- Elasticsearch와 Streamlit의 연결 경험
- 오픈 API 호출 경험

### ■ 프로젝트 개요

- 메이플스토리는 ‘운’으로 좌지우지되는 게임
- 하지만 플레이어 대부분은 본인의 운이 나쁘다고 생각한다.
(운 좋게 얻은 이익은 대부분 잊고, 운 나쁘게 잃었던 것들만 기억한다.)
- 메이플스토리에는 ‘큐브’라는 확률성 콘텐츠가 존재한다.
- 플레이어의 실제 ‘큐브’ 사용 기록으로 성공 횟수를 추출하고, 기댓값과 비교하여
플레이어의 ‘큐브운’이 좋은지 나쁜지 여부를 확인한다.

### ■ 기술 스택

- Python
    - 메이플스토리 오픈 API 호출
    - Elasticsearch 쿼리 작성
    - 시뮬레이터 랜덤 확률 추출 로직
    - streamlit 코드 구성
- Elasticsearch
    - json 형식으로 API 저장
    - 목표 등급별/큐브 종류별 ‘성공’ 여부 검색 기능
- Streamlit
    - 목표 등급/큐브 종류 선택 multiselect 버튼
    - Elasticsearch 인덱스 생성 버튼
    - 기댓값과 플레이어 성공 횟수 비교 결과 출력

### ■ 00_Are_you_lucky.py 작동 방식

1. [config.py](http://config.py) 및 insert_test.py에서 API를 호출, Elasticsearch 인덱스를 생성하고 데이터 삽입
2. 사용자는 검색을 원하는 큐브 종류와 목표 등급을 선택하고 작동 버튼을 클릭
3. 선택한 큐브 종류와 목표 등급을 변수로 받아 쿼리를 통해 조건에 맞는 document 검색 및 변수에 할당
4. 전체 횟수와 큐브 성공률을 곱해 기댓값을 구하고 성공 횟수와 비교
5. 기댓값보다 성공 횟수가 낮으면 ‘운 나쁜 사람’. 반대의 경우 ‘운 좋은 사람’ 문구 출력

### ■ 01_Cube_simulator.py 작동 방식

1. 실제 큐브 사용 기록을 불러오는 것이 아니라 큐브 성공 확률과 사용자가 지정한 횟수에 따라 Elasticsearch 인덱스 생성
2. 생성된 인덱스를 바탕으로 00_Are_you_lucky.py와 동일한 로직 작동