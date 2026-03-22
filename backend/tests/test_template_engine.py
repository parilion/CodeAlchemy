import pytest
import shutil
from pathlib import Path
from app.services.template_engine import TemplateEngine


def test_template_engine_matches_library():
    engine = TemplateEngine()
    template = engine.match_template("图书馆管理系统")
    assert template == "library"


def test_template_engine_matches_secondhand():
    engine = TemplateEngine()
    template = engine.match_template("二手商城系统，需要商品发布和交易功能")
    assert template == "secondhand"


def test_template_engine_matches_appointment():
    engine = TemplateEngine()
    template = engine.match_template("医院预约挂号系统")
    assert template == "appointment"


def test_template_engine_matches_pet():
    engine = TemplateEngine()
    template = engine.match_template("宠物管理系统")
    assert template == "pet"


def test_template_engine_unknown_returns_best_guess():
    engine = TemplateEngine()
    template = engine.match_template("学生信息管理系统")
    assert template in ("library", "secondhand", "appointment", "pet")


def test_template_engine_generate_copies_template(tmp_path):
    engine = TemplateEngine()
    output = str(tmp_path / "generated")
    template_used = engine.generate("图书馆管理系统", output, [])
    assert template_used == "library"
    # 输出目录存在（即使模板目录是空的也应该创建）
    assert Path(output).exists()


def test_template_engine_partial_keyword_match():
    engine = TemplateEngine()
    # "商品" 是 secondhand 的关键词
    template = engine.match_template("商品库存管理系统")
    assert template == "secondhand"
