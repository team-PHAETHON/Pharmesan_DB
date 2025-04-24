from pathlib import Path
import configparser


class ConfigLoader:
    """
    설정 파일(conf.ini)에서 값을 불러오는 클래스
    기본적으로 openData 섹션에서 apiKey를 로드할 수 있음
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = str(Path(__file__).resolve().parents[2] / "config" / "conf.ini")

        self.parser = configparser.ConfigParser()
        self.parser.read(config_path)

    def get(self, section: str, key: str) -> str:
        return self.parser.get(section, key)
