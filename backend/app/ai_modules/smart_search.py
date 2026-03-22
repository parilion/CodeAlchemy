from typing import Any, Dict
from app.ai_modules.base import AIModule


class SmartSearchModule(AIModule):
    MODULE_ID = "smart_search"
    MODULE_NAME = "智能语义搜索"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/SmartSearchService.java": self._render_service(base_pkg),
            f"src/main/java/{pkg_path}/ai/SmartSearchController.java": self._render_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return "ai:\n  search:\n    enabled: true\n"

    def _render_service(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 智能语义搜索服务 - CodeAlchemy注入
 * 将自然语言查询转换为关键词，配合原有搜索逻辑实现语义搜索
 */
@Service
public class SmartSearchService {{

    @Autowired
    private LLMClient llmClient;

    /**
     * 从自然语言查询中提取搜索关键词
     * 示例: "关于Java编程的入门书" → "Java 编程 入门"
     */
    public String extractKeywords(String naturalQuery) {{
        String systemPrompt = "你是一个搜索关键词提取助手。" +
            "请从用户的自然语言查询中提取1-3个最关键的搜索词，" +
            "只返回关键词，用空格分隔，不要其他内容。";
        return llmClient.chat(systemPrompt, naturalQuery).trim();
    }}
}}"""

    def _render_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 智能搜索接口 - CodeAlchemy注入
 * mode=smart: 语义搜索（返回提取的关键词）
 * mode=precise: 精准搜索（直接返回原始输入）
 */
@RestController
@RequestMapping("/api/ai/search")
@CrossOrigin(origins = "*")
public class SmartSearchController {{

    @Autowired
    private SmartSearchService smartSearchService;

    @PostMapping
    public Map<String, String> search(@RequestBody Map<String, String> req) {{
        String query = req.getOrDefault("query", "");
        String mode = req.getOrDefault("mode", "smart");

        if ("precise".equals(mode)) {{
            return Map.of("keywords", query, "mode", "precise", "original", query);
        }}

        String keywords = smartSearchService.extractKeywords(query);
        return Map.of("keywords", keywords, "mode", "smart", "original", query);
    }}
}}"""
