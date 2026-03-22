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
            f"src/main/java/{pkg_path}/ai/LLMClient.java": self._render_llm_client(base_pkg),
            f"src/main/java/{pkg_path}/ai/ChatController.java": self._render_chat_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return (
            "ai:\n"
            "  api-key: ${AI_API_KEY:your-api-key-here}\n"
            "  base-url: https://dashscope.aliyuncs.com/compatible-mode/v1\n"
            "  model: qwen-turbo\n"
        )

    def _render_llm_client(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;

/**
 * AI大语言模型客户端 - CodeAlchemy注入
 * 对接阿里云通义API（兼容OpenAI格式）
 */
@Component
public class LLMClient {{

    @Value("${{ai.api-key}}")
    private String apiKey;

    @Value("${{ai.base-url:https://dashscope.aliyuncs.com/compatible-mode/v1}}")
    private String baseUrl;

    @Value("${{ai.model:qwen-turbo}}")
    private String model;

    private final HttpClient httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
    private final ObjectMapper mapper = new ObjectMapper();

    /**
     * 调用大语言模型
     * @param systemPrompt 系统提示词
     * @param userMessage  用户消息
     * @return 模型回复内容
     */
    public String chat(String systemPrompt, String userMessage) {{
        try {{
            ObjectNode body = mapper.createObjectNode();
            body.put("model", model);
            ArrayNode messages = body.putArray("messages");

            ObjectNode sysMsg = messages.addObject();
            sysMsg.put("role", "system");
            sysMsg.put("content", systemPrompt);

            ObjectNode userMsg = messages.addObject();
            userMsg.put("role", "user");
            userMsg.put("content", userMessage);

            String json = mapper.writeValueAsString(body);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/chat/completions"))
                    .header("Content-Type", "application/json")
                    .header("Authorization", "Bearer " + apiKey)
                    .timeout(Duration.ofSeconds(60))
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            HttpResponse<String> response = httpClient.send(request,
                    HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() != 200) {{
                return "AI服务暂时不可用，请稍后重试。(HTTP " + response.statusCode() + ")";
            }}

            Map<?, ?> result = mapper.readValue(response.body(), Map.class);
            List<?> choices = (List<?>) result.get("choices");
            Map<?, ?> choice = (Map<?, ?>) choices.get(0);
            Map<?, ?> msg = (Map<?, ?>) choice.get("message");
            return String.valueOf(msg.get("content"));

        }} catch (Exception e) {{
            return "AI服务调用异常: " + e.getMessage();
        }}
    }}
}}"""

    def _render_chat_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * AI智能对话接口 - CodeAlchemy注入
 * 前端调用: POST /api/ai/chat
 */
@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*")
public class ChatController {{

    @Autowired
    private LLMClient llmClient;

    /**
     * 智能对话
     * 请求体: {{"message": "用户输入", "mode": "auto|query|knowledge"}}
     * 响应体: {{"reply": "AI回复", "mode": "..."}}
     */
    @PostMapping("/chat")
    public Map<String, String> chat(@RequestBody Map<String, String> req) {{
        String message = req.getOrDefault("message", "");
        String mode = req.getOrDefault("mode", "auto");

        String systemPrompt = "你是一个智能助手，帮助用户解答问题和查询信息。请用简洁、友好的中文回答。";
        if ("query".equals(mode)) {{
            systemPrompt = "你是一个数据查询助手，帮助用户理解和查找系统中的数据。";
        }} else if ("knowledge".equals(mode)) {{
            systemPrompt = "你是一个知识问答助手，请基于系统业务知识回答用户问题。";
        }}

        String reply = llmClient.chat(systemPrompt, message);
        return Map.of("reply", reply, "mode", mode);
    }}
}}"""
