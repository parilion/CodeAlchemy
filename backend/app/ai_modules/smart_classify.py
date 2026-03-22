from typing import Any, Dict
from app.ai_modules.base import AIModule


class SmartClassifyModule(AIModule):
    MODULE_ID = "smart_classify"
    MODULE_NAME = "智能分类"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/SmartClassifyService.java": self._render_service(base_pkg),
            f"src/main/java/{pkg_path}/ai/SmartClassifyController.java": self._render_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return "ai:\n  classify:\n    enabled: true\n"

    def _render_service(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 智能分类服务 - CodeAlchemy注入
 * AI自动推荐分类标签，用户可采纳或手动修改
 */
@Service
public class SmartClassifyService {{

    @Autowired
    private LLMClient llmClient;

    /**
     * @param content    待分类的内容（商品名、书名等）
     * @param categories 可选分类列表（逗号分隔），为空时AI自由分类
     * @return 推荐分类标签列表
     */
    public List<String> suggestCategories(String content, String categories) {{
        String prompt = (categories == null || categories.isBlank())
            ? "请为以下内容推荐1-3个合适的分类标签，只返回标签，用逗号分隔，不要解释：\\n\\n" + content
            : "请从以下分类中为内容选择最合适的1-3个，只返回分类名，用逗号分隔：\\n分类：" + categories + "\\n内容：" + content;

        String result = llmClient.chat("你是内容分类专家，请简洁精准地完成分类任务。", prompt);
        return Arrays.stream(result.split("[,，]"))
                .map(String::trim)
                .filter(s -> !s.isBlank())
                .collect(Collectors.toList());
    }}
}}"""

    def _render_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 智能分类接口 - CodeAlchemy注入
 * POST /api/ai/classify
 * 请求体: {{"content": "待分类内容", "categories": "可选分类1,可选分类2"}}
 */
@RestController
@RequestMapping("/api/ai/classify")
@CrossOrigin(origins = "*")
public class SmartClassifyController {{

    @Autowired
    private SmartClassifyService smartClassifyService;

    @PostMapping
    public Map<String, Object> classify(@RequestBody Map<String, String> req) {{
        String content = req.getOrDefault("content", "");
        String categories = req.getOrDefault("categories", "");
        List<String> result = smartClassifyService.suggestCategories(content, categories);
        return Map.of("categories", result, "content", content);
    }}
}}"""
