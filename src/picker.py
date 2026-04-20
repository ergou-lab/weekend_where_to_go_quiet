"""
随机选择目的地逻辑
"""
import random
from typing import List, Optional


class DestinationPicker:
    """随机目的地选择器"""

    # 过滤掉的关键词（太城市化的地方）
    SKIP_KEYWORDS = [
        "区", "街道", "居委会",
        "管委会", "管理处",
    ]

    # 保留的关键词（农村/小镇特征）
    KEEP_KEYWORDS = [
        "镇", "乡", "村", "镇",
        "古镇", "老街", "古村",
        "渔村", "山寨", "堡",
    ]

    def __init__(self, destinations: List[dict]):
        """
        Args:
            destinations: [{"name": str, "center": "lon,lat", "level": str}, ...]
        """
        self.destinations = destinations

    def filter_rural(self) -> List[dict]:
        """过滤出农村/小镇类型的目的地"""
        rural = []
        for d in self.destinations:
            name = d["name"]
            # 跳过包含城市关键词的
            if any(kw in name for kw in self.SKIP_KEYWORDS):
                continue
            # 优先保留有农村特征的
            if any(kw in name for kw in self.KEEP_KEYWORDS):
                rural.append(d)
                continue
            # 区级也保留（城乡结合部）
            if d.get("level") == "district":
                rural.append(d)

        return rural

    def pick_random(self, filtered: Optional[List[dict]] = None) -> dict:
        """随机选一个"""
        candidates = filtered if filtered is not None else self.destinations
        if not candidates:
            raise ValueError("没有可用的目的地")
        return random.choice(candidates)
