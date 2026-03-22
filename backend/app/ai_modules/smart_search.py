from typing import Any, Dict
from app.ai_modules.base import AIModule


class SmartSearchModule(AIModule):
    MODULE_ID = "smart_search"
    MODULE_NAME = "智能语义搜索"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/SmartSearchService.java":
                self._render(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return "ai:\n  search:\n    enabled: true\n"

    def _render(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.stereotype.Service;
import java.util.List;

/**
 * 智能语义搜索服务 - AI赋能注入
 * 与精准搜索并行，用户可通过 searchMode 参数选择
 * searchMode="smart" 使用语义搜索，searchMode="precise" 使用原有精准搜索
 */
@Service
public class SmartSearchService {{

    /**
     * 语义搜索：将自然语言查询向量化后进行相似度匹配
     * @param query 用户自然语言输入，如"关于Java编程的入门书"
     * @param mode "smart"=语义搜索，"precise"=精准搜索（由原有逻辑处理）
     */
    public List<String> search(String query, String mode) {{
        if ("smart".equals(mode)) {{
            // TODO: 调用向量化API进行语义检索
            return List.of("语义搜索结果占位: " + query);
        }}
        return List.of();
    }}
}}"""
