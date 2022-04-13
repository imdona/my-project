import sqlite3
import requests
from tinydb import TinyDB, Query
from tqdm import tqdm
import time


def create_db():
    DB_FILENAME = "bank.db"
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()

    # 테이블 만들기
    cur.execute("DROP TABLE IF EXISTS bank_info")
    cur.execute(f"""CREATE TABLE bank_info(
                    address_name VARCHAR,
                    category_name VARCHAR,
                    place_name VARCHAR,
                    road_address_name VARCHAR,
                    x VARCHAR,
                    y VARCHAR
                    );""")


def get_doc():
    API_KEY = 'KakaoAK ' + 'ac220588aa994372f4482942281b92a3'

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

    params = {
        'query': '서울 국민은행',
        'category_group_code': 'BK9', # 은행
        'page': 45
    }

    headers = {
        'Authorization': API_KEY
    }

    # json 형태로 받겠다
    res = requests.get(url, params=params, headers=headers).json()

    # print(res.keys())
    # print(res['documents'])
    print(res['meta'])
    '''
    서울 국민은행으로 검색하면 -> {'is_end': True, 'pageable_count': 45, 'same_name': {'keyword': '국민은행', 'region': [], 'selected_region': '서울특별시'}, 'total_count': 974}
    서울 은행 으로 검색하면 -> {'is_end': True, 'pageable_count': 45, 'same_name': {'keyword': '은행', 'region': [], 'selected_region': '서울특별시'}, 'total_count': 8875}
    '''
    return res['documents']


def check_cordinate():
    cordinate_list = [[126.734086, 37.413294, 126.984086, 37.663294], [126.984086, 37.663294, 127.234086, 37.715133], [127.234086, 37.715133, 127.269311, 37.715133]]
    for coordinate in cordinate_list:
        print(f"{coordinate[0]}, {coordinate[1]}, {coordinate[2]}, {coordinate[3]}")
        print(type(f"{coordinate[0]}, {coordinate[1]}, {coordinate[2]}, {coordinate[3]}"))


def test_func():
    API_KEY = 'KakaoAK ' + 'ac220588aa994372f4482942281b92a3'
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    cordinate_list = [[126.734086, 37.413294, 126.984086, 37.663294], [126.984086, 37.663294, 127.234086, 37.715133], [127.234086, 37.715133, 127.269311, 37.715133]]

    for coordinate in cordinate_list:
        params = {
            'query': '서울 국민은행',
            'category_group_code': 'BK9', # 은행
            'page': 1,
            'rect': f"{coordinate[0]}, {coordinate[1]}, {coordinate[2]}, {coordinate[3]}"
        }

        headers = {
            'Authorization': API_KEY
        }

        # json 형태로 받겠다
        res = requests.get(url, params=params, headers=headers).json()

        # print(res.keys())
        # print(res['documents'])
        # print(res['meta'])
        '''
        서울 국민은행으로 검색하면 -> {'is_end': True, 'pageable_count': 45, 'same_name': {'keyword': '국민은행', 'region': [], 'selected_region': '서울특별시'}, 'total_count': 974}
        서울 은행 으로 검색하면 -> {'is_end': True, 'pageable_count': 45, 'same_name': {'keyword': '은행', 'region': [], 'selected_region': '서울특별시'}, 'total_count': 8875}
        '''
        return res['documents']

def get_info():
    tinydb = TinyDB('seoul_bank_db.json')
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    API_KEY = 'KakaoAK ' + 'ac220588aa994372f4482942281b92a3'
    headers = {'Authorization': API_KEY}


    cordinate_list = [[126.734086, 37.413294, 126.984086, 37.663294], [126.984086, 37.663294, 127.234086, 37.715133], [127.234086, 37.715133, 127.269311, 37.715133]]

    for i in tqdm(range(1, 600)):
        for coordinate in cordinate_list:
            for page in range(1, 46):
                params = {
                    'query': '서울 은행',
                    'page': page,
                    'rect': f"{coordinate[0]}, {coordinate[1]}, {coordinate[2]}, {coordinate[3]}"
                }

                res = requests.get(url, params=params, headers=headers).json()

                if len(res['documents']) == 0:
                    break

                for doc in res['documents']:
                    address_name = doc['address_name']
                    category_name = doc['category_name']
                    place_name = doc['place_name']
                    road_address_name = doc['road_address_name']
                    x = doc['x']
                    y = doc['y']

                    tinydb.insert({
                        'address_name': address_name,
                        'category_name': category_name,
                        'place_name': place_name,
                        'road_address_name': road_address_name,
                        'x': x,
                        'y': y
                    })

                    time.sleep(5)

                if res['meta']['is_end']:
                    break


def main():
    # create_db()
    # print(get_doc())
    # check_cordinate()
    # print(test_func())
    get_info()


if __name__ == "__main__":
    main()