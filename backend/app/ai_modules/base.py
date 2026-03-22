from abc import ABC, abstractmethod
from typing import Any, Dict


class AIModule(ABC):
    MODULE_ID: str = ""
    MODULE_NAME: str = ""

    @abstractmethod
    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        """返回需要注入到项目的文件，{相对文件路径: 文件内容}"""
        pass

    @abstractmethod
    def get_config_snippet(self) -> str:
        """返回需要追加到 application.yml 的配置片段"""
        pass
