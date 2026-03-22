from typing import Any, Dict
from app.ai_modules.base import AIModule


class RagRetrievalModule(AIModule):
    MODULE_ID = "rag_retrieval"
    MODULE_NAME = "RAG增强检索"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/RagService.java": self._render_service(base_pkg),
            f"src/main/java/{pkg_path}/ai/RagController.java": self._render_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return (
            "ai:\n"
            "  rag:\n"
            "    enabled: true\n"
            "    knowledge-dir: src/main/resources/knowledge\n"
        )

    def _render_service(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

/**
 * RAG增强检索服务 - CodeAlchemy注入
 * 从本地知识库文件检索相关内容，结合LLM生成精准回答
 * 知识库文件放在: src/main/resources/knowledge/ 目录下（.txt/.md文件）
 */
@Service
public class RagService {{

    @Autowired
    private LLMClient llmClient;

    @Value("${{ai.knowledge-dir:src/main/resources/knowledge}}")
    private String knowledgeDir;

    /**
     * RAG问答：检索知识库 + LLM生成回答
     * @param question 用户问题
     * @return 基于知识库的回答
     */
    public String query(String question) {{
        String context = retrieveContext(question);
        String systemPrompt = context.isBlank()
            ? "你是一个智能助手，请根据你的知识回答用户问题。"
            : "你是一个知识问答助手，请严格基于以下知识库内容回答用户问题，如知识库中没有相关信息请如实说明：\\n\\n" + context;
        return llmClient.chat(systemPrompt, question);
    }}

    /** 从知识库文件中检索相关内容（简单关键词匹配）*/
    private String retrieveContext(String question) {{
        try {{
            Path dir = Paths.get(knowledgeDir);
            if (!Files.exists(dir)) return "";

            String[] keywords = question.split("[\\\\s，。？！,?!]+");
            List<String> relevantChunks = new ArrayList<>();

            Files.walk(dir)
                .filter(p -> p.toString().endsWith(".txt") || p.toString().endsWith(".md"))
                .forEach(p -> {{
                    try {{
                        String content = Files.readString(p);
                        String[] paragraphs = content.split("\\n{{2,}}");
                        for (String para : paragraphs) {{
                            for (String kw : keywords) {{
                                if (kw.length() > 1 && para.contains(kw)) {{
                                    relevantChunks.add(para.trim());
                                    break;
                                }}
                            }}
                        }}
                    }} catch (IOException ignored) {{}}
                }});

            return relevantChunks.stream()
                .distinct()
                .limit(3)
                .collect(Collectors.joining("\\n\\n"));
        }} catch (Exception e) {{
            return "";
        }}
    }}
}}"""

    def _render_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * RAG知识问答接口 - CodeAlchemy注入
 * POST /api/ai/rag/query
 */
@RestController
@RequestMapping("/api/ai/rag")
@CrossOrigin(origins = "*")
public class RagController {{

    @Autowired
    private RagService ragService;

    @PostMapping("/query")
    public Map<String, String> query(@RequestBody Map<String, String> req) {{
        String question = req.getOrDefault("question", "");
        String answer = ragService.query(question);
        return Map.of("answer", answer, "question", question);
    }}
}}"""
