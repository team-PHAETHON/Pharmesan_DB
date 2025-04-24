from abc import ABC, abstractmethod
from typing import Any


# 추상화된 데이터 추출기
class DataExtractor(ABC):
    @abstractmethod
    def extract(self, query_params: dict[str, Any], attri: list[str] | None = None) -> Any:
        """데이터 추출"""
        pass
