from typing import Any
from pymongo.collection import Collection

from extract.extracter import DataExtractor
from utils.database import DataBaseClient


class MongoExtractor(DataExtractor):
    """
    MongoDB에서 데이터를 추출하는 클래스
    """

    def __init__(self, db_client: DataBaseClient, collection_name: str) -> None:
        self.db_client: DataBaseClient = db_client
        self.collection_name: str = collection_name

    def extract(self, query: dict[str, Any] = None, attri: list[str] | None = None) -> list[dict[str, Any]]:
        """
        MongoDB 컬렉션에서 데이터를 추출하여 리스트로 반환

        :param query: MongoDB 쿼리
        :return: 문서 리스트
        """
        collection: Collection = self.db_client.db[self.collection_name]

        if attri is None:
            # attri가 None인 경우 전체 추출
            return list(collection.find(query, {"_id": 0}))
        else:
            # attri에 데이터가 있을 경우 attri에 해당하는 속성만 추출
            attri = {"_id": 0} | {attr: 1 for attr in attri}
            return list(collection.find(query, attri))
