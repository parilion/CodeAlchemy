from typing import Any, Dict
from app.ai_modules.base import AIModule


class CollaborativeFilterModule(AIModule):
    MODULE_ID = "collaborative_filter"
    MODULE_NAME = "协同过滤推荐"

    def get_inject_files(self, project_analysis: Dict[str, Any]) -> Dict[str, str]:
        base_pkg = project_analysis.get("base_package", "com.example.app")
        pkg_path = base_pkg.replace(".", "/")
        return {
            f"src/main/java/{pkg_path}/ai/RecommendService.java": self._render_service(base_pkg),
            f"src/main/java/{pkg_path}/ai/RecommendController.java": self._render_controller(base_pkg),
        }

    def get_config_snippet(self) -> str:
        return "ai:\n  recommend:\n    enabled: true\n    strategy: user-based\n"

    def _render_service(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * 协同过滤推荐服务 - CodeAlchemy注入
 * 基于用户行为数据的个性化推荐（内存存储，重启后清空）
 */
@Service
public class RecommendService {{

    // 用户行为矩阵: userId -> {{itemId -> score}}
    private final Map<String, Map<String, Double>> userItemMatrix = new ConcurrentHashMap<>();

    /**
     * 记录用户行为（在原有业务逻辑中调用此方法）
     * @param userId 用户ID
     * @param itemId 物品ID（商品/图书/商品等）
     * @param score  行为权重（浏览=1.0, 收藏=2.0, 购买/借阅=3.0）
     */
    public void recordBehavior(String userId, String itemId, double score) {{
        userItemMatrix
            .computeIfAbsent(String.valueOf(userId), k -> new ConcurrentHashMap<>())
            .merge(String.valueOf(itemId), score, Double::sum);
    }}

    /**
     * 基于用户的协同过滤推荐
     * @param userId 目标用户ID
     * @param topN   推荐数量
     * @return 推荐物品ID列表
     */
    public List<String> recommendForUser(String userId, int topN) {{
        Map<String, Double> targetItems = userItemMatrix.getOrDefault(
            String.valueOf(userId), Collections.emptyMap());
        if (targetItems.isEmpty()) return Collections.emptyList();

        Map<String, Double> candidateScores = new HashMap<>();
        for (Map.Entry<String, Map<String, Double>> other : userItemMatrix.entrySet()) {{
            if (other.getKey().equals(String.valueOf(userId))) continue;
            double sim = cosineSimilarity(targetItems, other.getValue());
            if (sim <= 0) continue;
            for (Map.Entry<String, Double> item : other.getValue().entrySet()) {{
                if (!targetItems.containsKey(item.getKey())) {{
                    candidateScores.merge(item.getKey(), sim * item.getValue(), Double::sum);
                }}
            }}
        }}

        return candidateScores.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .limit(topN)
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
    }}

    private double cosineSimilarity(Map<String, Double> a, Map<String, Double> b) {{
        double dot = 0, normA = 0, normB = 0;
        for (Map.Entry<String, Double> e : a.entrySet()) {{
            dot += e.getValue() * b.getOrDefault(e.getKey(), 0.0);
            normA += e.getValue() * e.getValue();
        }}
        for (double v : b.values()) normB += v * v;
        return (normA == 0 || normB == 0) ? 0 : dot / (Math.sqrt(normA) * Math.sqrt(normB));
    }}
}}"""

    def _render_controller(self, base_pkg: str) -> str:
        return f"""package {base_pkg}.ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 协同过滤推荐接口 - CodeAlchemy注入
 * POST /api/ai/recommend/behavior  记录用户行为
 * GET  /api/ai/recommend/{{userId}}  获取推荐列表
 */
@RestController
@RequestMapping("/api/ai/recommend")
@CrossOrigin(origins = "*")
public class RecommendController {{

    @Autowired
    private RecommendService recommendService;

    /** 记录用户行为（浏览/收藏/购买）*/
    @PostMapping("/behavior")
    public Map<String, String> recordBehavior(@RequestBody Map<String, Object> req) {{
        String userId = String.valueOf(req.getOrDefault("userId", ""));
        String itemId = String.valueOf(req.getOrDefault("itemId", ""));
        double score = Double.parseDouble(String.valueOf(req.getOrDefault("score", "1.0")));
        if (!userId.isBlank() && !itemId.isBlank()) {{
            recommendService.recordBehavior(userId, itemId, score);
        }}
        return Map.of("status", "ok");
    }}

    /** 获取个性化推荐 */
    @GetMapping("/{{userId}}")
    public List<String> recommend(@PathVariable String userId,
                                   @RequestParam(defaultValue = "5") int topN) {{
        return recommendService.recommendForUser(userId, topN);
    }}
}}"""
