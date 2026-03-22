import json
from typing import Any, Dict
from app.ai_modules.base import AIModule

INTENT_PROMPT = """你是一个意图分类器。根据用户输入判断是"查询型"还是"知识问答型"。
查询型：用户想查找/过滤数据库中的数据。返回: {"intent": "query", "entity": "实体名", "condition": "条件描述"}
知识问答型：用户询问业务规则/操作流程等知识。返回: {"intent": "knowledge"}
只返回JSON，不要其他文字。"""


class ChatAssistantModule(AIModule):
    MODULE_ID = "chat_assistant"
    MODULE_NAME = "智能对话助手"

    def __init__(self, llm, knowledge_manager):
        self.llm = llm
        self.km = knowledge_manager

    async def classify_intent(self, user_input: str) -> Dict:
        response = await self.llm.chat([
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_input},
        ])
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"intent": "knowledge"}

    async def handle_query(self, user_input: str) -> Dict:
        intent = await self.classify_intent(user_input)
        intent["type"] = "query"
        return intent

    async def handle_knowledge_qa(self, question: str) -> str:
        context_chunks = self.km.query(question)
        context = "\n".join(context_chunks) if context_chunks else "暂无相关知识库内容。"
        return await self.llm.chat([
            {"role": "system", "content": f"基于以下知识库内容回答用户问题：\n{context}"},
            {"role": "user", "content": question},
        ])

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/ChatController.java":
                self._render_chat_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return (
            "ai:\n"
            "  chat:\n"
            "    enabled: true\n"
            "    llm-provider: ${AI_LLM_PROVIDER:openai}\n"
        )

    def _render_chat_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

/**
 * AI智能对话接口 - AI赋能注入
 * 支持查询型和知识问答型两种对话模式
 */
@RestController
@RequestMapping("/api/ai/chat")
public class ChatController {{

    @PostMapping
    public Map<String, String> chat(@RequestBody Map<String, String> req) {{
        String message = req.getOrDefault("message", "");
        // TODO: 接入 AI 服务实现实际对话
        return Map.of("reply", "AI回复: " + message, "type", "knowledge");
    }}
}}"""
