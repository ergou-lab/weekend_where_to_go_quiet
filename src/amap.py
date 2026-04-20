"""
高德地图 API 封装
"""
import os
import requests
from typing import Optional


class AmapClient:
    """高德地图 API 客户端"""

    BASE_URL = "https://restapi.amap.com/v3"

    def __init__(self, key: Optional[str] = None):
        self.key = key or os.getenv("AMAP_KEY", "")

    def geocode(self, address: str, city: str = "") -> Optional[dict]:
        """
        地理编码：将地址转换为经纬度

        Args:
            address: 地址
            city: 城市名（提高准确性）

        Returns:
            {"lat": float, "lon": float} 或 None
        """
        params = {
            "key": self.key,
            "address": address,
            "output": "json",
        }
        if city:
            params["city"] = city

        resp = requests.get(f"{self.BASE_URL}/geocode/geo", params=params, timeout=10)
        data = resp.json()

        if data.get("status") == "1" and data.get("geocodes"):
            loc = data["geocodes"][0]["location"].split(",")
            return {"lon": float(loc[0]), "lat": float(loc[1])}
        return None

    def driving_route(
        self, origin: tuple, destination: tuple
    ) -> Optional[dict]:
        """
        驾车路径规划：计算两点间的距离和耗时

        Args:
            origin: (lon, lat)
            destination: (lon, lat)

        Returns:
            {"distance": int, "duration": int} 距离(米), 耗时(秒)
        """
        params = {
            "key": self.key,
            "origin": f"{origin[0]},{origin[1]}",
            "destination": f"{destination[0]},{destination[1]}",
            "strategy": "0",  # 最速度优先
            "output": "json",
        }

        resp = requests.get(f"{self.BASE_URL}/direction/driving", params=params, timeout=10)
        data = resp.json()

        if data.get("status") == "1" and data.get("route"):
            paths = data["route"]["paths"]
            if paths:
                return {
                    "distance": int(paths[0]["distance"]),
                    "duration": int(paths[0]["time"]),
                }
        return None

    def district(self, keywords: str, subdistrict: int = 1) -> Optional[list]:
        """
        行政区划查询：获取下级行政区

        Args:
            keywords: 上一级行政区名称，如"上海"、"杭州市"
            subdistrict: 向下查询的层级，0=不查下级，1=查区县，2=查街道/乡镇

        Returns:
            [{"name": str, "center": "lon,lat", "level": str}, ...]
        """
        params = {
            "key": self.key,
            "keywords": keywords,
            "subdistrict": subdistrict,
            "output": "json",
        }

        resp = requests.get(f"{self.BASE_URL}/config/district", params=params, timeout=10)
        data = resp.json()

        if data.get("status") == "1" and data.get("districts"):
            result = []
            for d in data["districts"][0].get("districts", []):
                result.append({
                    "name": d["name"],
                    "center": d.get("center", ""),
                    "level": d.get("level", ""),
                })
            return result
        return None
