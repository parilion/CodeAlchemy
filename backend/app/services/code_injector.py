from pathlib import Path
from typing import List, Dict, Any
from app.ai_modules.base import AIModule


class CodeInjector:
    def __init__(self, project_path: str):
        self.root = Path(project_path)

    def inject(self, modules: List[AIModule], project_analysis: Dict[str, Any]) -> None:
        for module in modules:
            inject_files = module.get_inject_files(project_analysis)
            for rel_path, content in inject_files.items():
                target = self.root / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            self._append_config(module.get_config_snippet())

        # 新增：注入前端聊天组件 + 生成 README
        self._inject_chat_widget()
        self._generate_readme(modules, project_analysis)

    def _append_config(self, snippet: str) -> None:
        yml_candidates = [
            self.root / "src/main/resources/application.yml",
            self.root / "src/main/resources/application.properties",
        ]
        for yml in yml_candidates:
            if yml.exists():
                original = yml.read_text(encoding="utf-8")
                # 取 snippet 第一行作为判重 key（如 "ai:"）
                first_line = snippet.strip().split("\n")[0]
                if first_line not in original:
                    yml.write_text(original + "\n" + snippet, encoding="utf-8")
                return

    def _inject_chat_widget(self) -> None:
        """注入前端 AI 对话悬浮窗（纯JS，兼容 Vue/HTML）"""
        widget_js = '''// AI Chat Widget - CodeAlchemy注入
(function() {
    var styles = '#ai-chat-btn{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:#1677ff;color:white;border:none;font-size:24px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.15);z-index:9999}' +
        '#ai-chat-panel{position:fixed;bottom:96px;right:24px;width:360px;height:500px;background:white;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.12);display:none;flex-direction:column;z-index:9999;overflow:hidden}' +
        '#ai-chat-header{background:#1677ff;color:white;padding:16px;font-weight:bold;display:flex;justify-content:space-between;align-items:center}' +
        '#ai-chat-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px}' +
        '.ai-msg-user{align-self:flex-end;background:#1677ff;color:white;padding:8px 12px;border-radius:12px 12px 2px 12px;max-width:80%;word-break:break-all}' +
        '.ai-msg-bot{align-self:flex-start;background:#f0f0f0;color:#333;padding:8px 12px;border-radius:12px 12px 12px 2px;max-width:80%;word-break:break-all}' +
        '#ai-chat-input-area{padding:12px;border-top:1px solid #f0f0f0;display:flex;gap:8px}' +
        '#ai-chat-input{flex:1;border:1px solid #d9d9d9;border-radius:6px;padding:8px;outline:none;font-size:14px}' +
        '#ai-chat-send{background:#1677ff;color:white;border:none;border-radius:6px;padding:8px 16px;cursor:pointer;white-space:nowrap}';

    document.addEventListener('DOMContentLoaded', function() {
        var style = document.createElement('style');
        style.textContent = styles;
        document.head.appendChild(style);

        var container = document.createElement('div');
        container.innerHTML = '<button id="ai-chat-btn" title="AI助手">&#x1F4AC;</button>' +
            '<div id="ai-chat-panel">' +
            '<div id="ai-chat-header"><span>&#x1F916; AI智能助手</span><span id="ai-chat-close" style="cursor:pointer">&#x2715;</span></div>' +
            '<div id="ai-chat-messages"><div class="ai-msg-bot">您好！我是AI助手，可以帮您查询信息或回答问题。</div></div>' +
            '<div id="ai-chat-input-area"><input id="ai-chat-input" placeholder="输入您的问题..." /><button id="ai-chat-send">发送</button></div>' +
            '</div>';
        document.body.appendChild(container);

        var panel = document.getElementById('ai-chat-panel');
        var messages = document.getElementById('ai-chat-messages');
        var input = document.getElementById('ai-chat-input');

        document.getElementById('ai-chat-btn').onclick = function() {
            panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
        };
        document.getElementById('ai-chat-close').onclick = function() {
            panel.style.display = 'none';
        };

        function addMsg(text, isUser) {
            var div = document.createElement('div');
            div.className = isUser ? 'ai-msg-user' : 'ai-msg-bot';
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function send() {
            var text = input.value.trim();
            if (!text) return;
            input.value = '';
            addMsg(text, true);
            var thinking = document.createElement('div');
            thinking.className = 'ai-msg-bot';
            thinking.textContent = '正在思考...';
            messages.appendChild(thinking);
            messages.scrollTop = messages.scrollHeight;

            fetch('/api/ai/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text, mode: 'auto'})
            }).then(function(r) { return r.json(); })
              .then(function(d) { thinking.textContent = d.reply || d.answer || '收到您的问题'; })
              .catch(function() { thinking.textContent = 'AI服务暂时不可用，请稍后再试。'; });
        }

        document.getElementById('ai-chat-send').onclick = send;
        input.addEventListener('keydown', function(e) { if (e.key === 'Enter') send(); });
    });
})();
'''
        # 寻找静态资源目录注入
        candidates = [
            self.root / "src/main/resources/static/js",
            self.root / "src/main/resources/static",
            self.root / "src/main/resources/public",
            self.root / "static/js",
            self.root / "static",
        ]
        for target_dir in candidates:
            if target_dir.exists():
                (target_dir / "ai-chat-widget.js").write_text(widget_js, encoding="utf-8")
                return
        # 如果都不存在，创建到 static/js
        fallback = self.root / "src/main/resources/static/js"
        fallback.mkdir(parents=True, exist_ok=True)
        (fallback / "ai-chat-widget.js").write_text(widget_js, encoding="utf-8")

    def _generate_readme(self, modules: List[AIModule], project_analysis: Dict[str, Any]) -> None:
        """生成 README-AI.md 说明如何配置和使用注入的AI功能"""
        module_list = "\n".join(f"- {m.MODULE_NAME}（{m.MODULE_ID}）" for m in modules)
        base_pkg = project_analysis.get("base_package", "com.example.app")

        readme = f"""# AI功能说明 - CodeAlchemy增强

## 已注入的AI模块
{module_list}

## 配置步骤

### 1. 在 application.yml 中配置 API Key

```yaml
ai:
  api-key: YOUR_API_KEY_HERE    # 填入你的阿里云通义 API Key
  base-url: https://dashscope.aliyuncs.com/compatible-mode/v1
  model: qwen-turbo             # 可选: qwen-turbo / qwen-plus / qwen-max
```

或通过环境变量设置（推荐，避免泄露）：
```bash
export AI_API_KEY=your-api-key
```

### 2. 在前端页面引入聊天组件

在 HTML 页面的 `</body>` 标签前加入：
```html
<script src="/js/ai-chat-widget.js"></script>
```

### 3. 启动项目

```bash
mvn spring-boot:run
```

访问系统后，页面右下角会出现 AI 助手悬浮按钮

## API 接口说明

| 接口 | 方法 | 功能 |
|------|------|------|
| /api/ai/chat | POST | 智能对话 |
| /api/ai/search | POST | 智能语义搜索 |
| /api/ai/classify | POST | 智能分类 |
| /api/ai/recommend/behavior | POST | 记录用户行为 |
| /api/ai/recommend/{{userId}} | GET | 获取个性化推荐 |
| /api/ai/rag/query | POST | 知识库问答 |

## 接口示例

**智能对话：**
```bash
curl -X POST http://localhost:8080/api/ai/chat \\
  -H "Content-Type: application/json" \\
  -d '{{"message": "帮我查一下外卖订单状态", "mode": "query"}}'
```

**智能搜索（获取关键词，传给原有搜索接口）：**
```bash
curl -X POST http://localhost:8080/api/ai/search \\
  -H "Content-Type: application/json" \\
  -d '{{"query": "川菜口味的外卖", "mode": "smart"}}'
```

## 源代码位置

注入的 AI 文件位于：`src/main/java/{base_pkg.replace('.', '/')}/ai/`

---
*由 CodeAlchemy 自动生成*
"""
        readme_path = self.root / "README-AI.md"
        readme_path.write_text(readme, encoding="utf-8")
