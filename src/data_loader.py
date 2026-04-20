"""
数据加载器
"""
import json
import os
from typing import Optional


def load_sample_data(path: Optional[str] = None) -> list:
    """
    加载示例数据（无需API Key就能测试）
    """
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
