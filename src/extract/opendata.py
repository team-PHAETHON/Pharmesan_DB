import requests
from typing import Any

from extract.extracter import DataExtractor


class OpenDataAPI(DataExtractor):
    """
    공공데이터 API 요청을 처리하는 클래스
    """

    BASE_URL = "https://apis.data.go.kr/1471000"

    def __init__(self, api_key: str, endpoint: str) -> None:
        self.api_key: str = api_key
        self.endpoint: str = endpoint
        self.default_params = {
            "numOfRows": 100,
            "serviceKey": self.api_key,
            "type": "json",
        }

    def extract(self, params: dict[str, Any] = {}, attri: list[str] | None = None) -> dict[str, Any]:
        """
        API 호출 및 JSON 반환

        :param endpoint: API 엔드포인트
        :param params: 요청 파라미터 딕셔너리
        :return: JSON 응답을 딕셔너리 형태로 반환
        """
        url: str = f"{self.BASE_URL}/{self.endpoint}"
        params = {**self.default_params, **params}
        response: requests.Response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
