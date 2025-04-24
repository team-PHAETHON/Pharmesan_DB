from abc import ABC, abstractmethod
import sys
sys.path.append('/workspace/QDMS/src')  # noqa: E402 # 구름 IDE에서 직접 개발한 라이브러리를 불러오기 위한 설정

from pymongo import MongoClient
from pymongo.database import Database

from utils.config import ConfigLoader


class DataBaseClient(ABC):
    """데이터베이스 클라이언트의 추상 베이스 클래스"""

    @abstractmethod
    def connect(self, db_name: str) -> None:
        """데이터베이스에 연결"""
        pass

    @abstractmethod
    def close(self) -> None:
        """데이터베이스 연결 종료"""
        pass

    @property
    @abstractmethod
    def db(self) -> Database:
        """연결된 데이터베이스 객체 반환"""
        pass


class MongoDBClient(DataBaseClient):
    """MongoDB 전용 클라이언트 구현"""

    def __init__(self, uri: str | None = None) -> None:
        """
        MongoDB 연결 URI를 설정하고, 초기 클라이언트 상태를 정의

        환경 설정(config)을 통해 사용자 정보, 비밀번호, 호스트, 포트 등을 로딩
        """
        config = ConfigLoader()
        user: str = config.get("mongo", "user")
        password: str = config.get("mongo", "password")
        host: str = config.get("mongo", "host")

        # 기본 URI가 주어지지 않으면 config 정보로 URI 구성
        self.uri: str = uri or f"mongodb+srv://{user}:{password}@{host}"

        self.client: MongoClient | None = None  # MongoDB 클라이언트 객체
        self._db: Database | None = None        # 선택된 데이터베이스 객체

    def connect(self, db_name: str) -> None:
        """
        MongoDB에 연결하고 특정 데이터베이스를 선택

        Args:
            db_name (str): 연결할 MongoDB 데이터베이스 이름
        """
        if self.client is None:
            self.client = MongoClient(self.uri)
        self._db = self.client[db_name]

    def close(self) -> None:
        """MongoDB 연결을 종료하고 클라이언트와 DB 참조를 초기화"""
        if self.client:
            self.client.close()
            self.client = None
            self._db = None

    @property
    def db(self) -> Database:
        """
        연결된 데이터베이스를 반환. 연결되지 않은 경우 에러 발생

        Returns:
            Database: 현재 연결된 MongoDB 데이터베이스 인스턴스
        """
        if self._db is None:
            raise RuntimeError("Database not connected. Call `connect(db_name)` first.")
        return self._db
