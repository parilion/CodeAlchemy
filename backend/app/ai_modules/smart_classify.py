from typing import Any, Dict
from app.ai_modules.base import AIModule


class SmartClassifyModule(AIModule):
    MODULE_ID = "smart_classify"
    MODULE_NAME = "智能分类"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/SmartClassifyService.java":
                self._render(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return "ai:\n  classify:\n    enabled: true\n"

    def _render(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.stereotype.Service;
import java.util.List;

/**
 * 智能分类服务 - AI赋能注入
 * 根据内容自动推荐分类标签，用户可采纳或手动修改
 */
@Service
public class SmartClassifyService {{

    /**
     * @param content 待分类的内容（书名、商品名等）
     * @return 推荐的分类标签列表
     */
    public List<String> suggestCategories(String content) {{
        // TODO: 调用LLM进行内容智能分类
        return List.of("未分类");
    }}
}}"""
