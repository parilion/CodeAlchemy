from typing import Any, Dict
from app.ai_modules.base import AIModule


class RagRetrievalModule(AIModule):
    MODULE_ID = "rag_retrieval"
    MODULE_NAME = "RAG增强检索"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/RagService.java":
                self._render(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return (
            "ai:\n"
            "  rag:\n"
            "    enabled: true\n"
            "    chroma-url: ${CHROMA_URL:http://localhost:8000}\n"
        )

    def _render(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.stereotype.Service;

/**
 * RAG增强检索服务 - AI赋能注入
 * 从通用知识库+业务知识库检索相关片段，结合LLM生成高质量回答
 */
@Service
public class RagService {{

    /**
     * RAG问答：检索知识库 + LLM生成回答
     * @param question 用户问题
     * @return 基于知识库的回答
     */
    public String query(String question) {{
        // TODO: 1. 调用ChromaDB检索相关知识片段
        // TODO: 2. 组合上下文交给LLM生成回答
        return "RAG回答占位: " + question;
    }}
}}"""
