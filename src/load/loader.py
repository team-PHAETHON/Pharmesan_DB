from abc import ABC, abstractmethod
from typing import Any


# 추상화된 데이터 추출기
class DataLoader(ABC):
    @abstractmethod
    def load(self, query_params: dict[str, Any]) -> Any:
        """데이터 추출"""
        pass
