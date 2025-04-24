from typing import Any

from pymongo.collection import Collection

from load.loader import DataLoader
from utils.database import DataBaseClient


class MongoLoader(DataLoader):
    """
    MongoDB에 데이터를 적재하는 클래스.
    db_client는 DataBaseClient 인터페이스를 따르며, MongoDBClient로 주입되어야 함.
    """

    def __init__(self, db_client: DataBaseClient, collection_name: str) -> None:
        self.db_client = db_client
        self.collection_name = collection_name

    def load(self, data: list[dict[str, Any]]) -> None:
        if not data:
            print("No data to insert.")
            return

        # MongoDB 전용 Collection 타입으로 캐스팅 (런타임 보장용)
        collection: Collection = self.db_client.db[self.collection_name]
        collection.insert_many(data)
        print(f"{len(data)} documents inserted into '{self.collection_name}'")
