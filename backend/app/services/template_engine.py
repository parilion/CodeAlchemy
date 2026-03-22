import shutil
from pathlib import Path
from typing import List

TEMPLATE_KEYWORDS = {
    "library": ["图书馆", "图书", "借阅", "馆藏", "借书", "还书"],
    "secondhand": ["二手", "商城", "交易", "商品", "购物", "卖家", "买家"],
    "appointment": ["预约", "挂号", "就诊", "医院", "诊断", "门诊", "科室"],
    "pet": ["宠物", "动物", "领养", "饲养", "兽医", "猫", "狗"],
}


class TemplateEngine:
    def __init__(self, templates_dir: str = "project_templates"):
        self.templates_dir = Path(templates_dir)

    def match_template(self, requirement: str) -> str:
        scores = {
            template: sum(1 for kw in keywords if kw in requirement)
            for template, keywords in TEMPLATE_KEYWORDS.items()
        }
        best = max(scores, key=lambda k: scores[k])
        # 若所有分数都是0，默认返回 library（最通用的）
        if scores[best] == 0:
            return "library"
        return best

    def generate(self, requirement: str, output_path: str, selected_modules: List[str]) -> str:
        template_name = self.match_template(requirement)
        template_dir = self.templates_dir / template_name
        out = Path(output_path)
        if template_dir.exists() and any(template_dir.iterdir()):
            shutil.copytree(str(template_dir), output_path, dirs_exist_ok=True)
        else:
            # 模板目录为空（MVP阶段），仍然创建输出目录
            out.mkdir(parents=True, exist_ok=True)
        return template_name
