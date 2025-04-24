import sys
sys.path.append('/workspace/QDMS/src')  # noqa: E402 # 구름 IDE에서 직접 개발한 라이브러리를 불러오기 위한 설정

from utils.config import ConfigLoader
from utils.database import MongoDBClient
from extract.opendata import OpenDataAPI
from extract.from_mongo import MongoExtractor
from transformation.search_schema import PillSchemaMapper
from load.to_mongo import MongoLoader


def delete_all():

    # MongoDBClient 인스턴스화 및 연결
    db_client = MongoDBClient()
    db_client.connect(db_name="medicine")  # DB 연결

    # db_client.db["identification"].delete_many({})
    # db_client.db["easy_info"].delete_many({})
    db_client.db["search"].delete_many({})

    db_client.close()


def count_all():

    # MongoDBClient 인스턴스화 및 연결
    db_client = MongoDBClient()
    db_client.connect(db_name="medicine")  # DB 연결

    print(db_client.db["identification"].count_documents({}))
    print(db_client.db["easy_info"].count_documents({}))
    print(db_client.db["search"].count_documents({}))

    db_client.close()


def show_sample_data():

    # MongoDBClient 인스턴스화 및 연결
    db_client = MongoDBClient()
    db_client.connect(db_name="medicine")  # DB 연결

    print(db_client.db["search"].find({}).limit(1)[0])


def openapi_to_mongo():
    # OpenAPI에서 데이터를 수집 해 MongoDB에 저장하는 함수입니다.

    # 설정 파일에서 API 키 가져오기
    config = ConfigLoader()
    api_key = config.get("open_data", "api_key")
    id_endpoint = config.get("open_data", "id_endpoint")
    easy_endpoint = config.get("open_data", "easy_endpoint")

    open_api_id = OpenDataAPI(api_key, id_endpoint)
    open_api_easy = OpenDataAPI(api_key, easy_endpoint)

    # MongoDBClient 인스턴스화 및 연결
    db_client = MongoDBClient()
    db_client.connect(db_name="medicine")  # DB 연결

    # MongoLoader 사용하여 데이터 추출
    mongo_loader_id = MongoLoader(db_client=db_client,
                                  collection_name="identification")
    mongo_loader_easy = MongoLoader(db_client=db_client,
                                    collection_name="easy_info")

    for page in range(1, 260):
        params = {"pageNo": page}

        medicine_list = open_api_id.extract(params)
        mongo_loader_id.load(medicine_list["body"]["items"])

        if page < 49:
            easy_list = open_api_easy.extract(params)
            mongo_loader_easy.load(easy_list["body"]["items"])

    db_client.close()


def mongo_to_search():
    # MongoDB에 적재 된 의약외품 API 데이터를 가공하여 검색용 문서를 생성하는 함수입니다.

    # MongoDBClient 인스턴스화 및 연결
    db_client = MongoDBClient()
    db_client.connect(db_name="medicine")  # DB 연결

    # MongoDB에서 병합할 데이터 추출
    mongo_extractor_id = MongoExtractor(db_client=db_client,
                                        collection_name="identification")
    mongo_extractor_easy = MongoExtractor(db_client=db_client,
                                          collection_name="easy_info")

    # EasyInfo 데이터 추출
    easy_attri = ["itemSeq", "itemName", "entpName", "efcyQesitm", "useMethodQesitm",
             "atpnWarnQesitm", "atpnQesitm", "intrcQesitm", "seQesitm", "itemImage"]
    easy_data_list = mongo_extractor_easy.extract({}, easy_attri)
    easy_data_map = {item["itemSeq"]: item for item in easy_data_list}

    # Identification 데이터 추출
    id_attri = ["ITEM_SEQ", "CHART", "PRINT_FRONT", "PRINT_BACK", "DRUG_SHAPE", "COLOR_CLASS1", 
            "COLOR_CLASS2", "LINE_FRONT", "LINE_BACK", "LENG_LONG", "LENG_SHORT", "THICK",
             "CLASS_NO", "CLASS_NAME", "ETC_OTC_NAME", "FORM_CODE_NAME", "ITEM_ENG_NAME"]
    id_data_list = mongo_extractor_id.extract({"ITEM_SEQ": {"$in": list(easy_data_map.keys())}}, id_attri)

    # 검색용 데이터로 변환
    normalized_data_list = []
    for id_data in id_data_list:
        item_seq = id_data.get("ITEM_SEQ")
        easy_data = easy_data_map.get(item_seq)

        if easy_data:
            # 먼저 두 딕셔너리를 병합
            merged_data = {**id_data, **easy_data}

            # 키 변환
            normalized_merged_data = {
                PillSchemaMapper.convert(k): v
                for k, v in merged_data.items()
            }
            normalized_merged_data.pop("ITEM_SEQ")
            normalized_data_list.append(normalized_merged_data)

    # 변환 된 데이터 업로드
    mongo_loader = MongoLoader(db_client=db_client, collection_name="search")
    mongo_loader.load(normalized_data_list)

    db_client.close()


if __name__ == "__main__":

    # delete_all()
    # openapi_to_mongo()
    # mongo_to_search()
    # count_all()
    show_sample_data()
