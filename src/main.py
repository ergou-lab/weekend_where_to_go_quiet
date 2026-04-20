#!/usr/bin/env python3
"""
周末去哪_安静版
随机选一个周边农村，说走就走
"""
import argparse
import os
import sys
import json
from dotenv import load_dotenv

# 加载 .env
load_dotenv()

from amap import AmapClient
from picker import DestinationPicker


def parse_args():
    parser = argparse.ArgumentParser(description="周末去哪_安静版")
    parser.add_argument("--lat", type=float, default=None, help="出发地纬度")
    parser.add_argument("--lon", type=float, default=None, help="出发地经度")
    parser.add_argument("--city", type=str, default=None, help="出发城市（lat/lon未提供时使用）")
    parser.add_argument("--max-duration", type=int, default=120, help="最大车程（分钟）")
    parser.add_argument("--district", type=str, default=None, help="查询的上一级行政区（默认从城市名获取）")
    parser.add_argument("--sample", action="store_true", help="使用示例数据运行（无需API Key）")
    return parser.parse_args()


def print_result(destination: dict, distance: int = 0, duration: int = 0):
    """打印结果"""
    print("\n" + "=" * 50)
    print("🎲 今日目的地")
    print("=" * 50)
    print(f"📍 {destination['name']}")
    if distance:
        print(f"🚗 距离: {distance / 1000:.1f} 公里 | 约 {duration // 60} 小时 {duration % 60} 分钟")
    print(f"📌 层级: {destination.get('level', 'unknown')}")
    if destination.get("center"):
        lon, lat = destination["center"].split(",")
        print(f"🗺️ 坐标: {lat}, {lon}")
    print("=" * 50)


def main():
    args = parse_args()
    amap = AmapClient()

    # 如果是示例模式，直接用示例数据
    if args.sample:
        from data_loader import load_sample_data
        data = load_sample_data()
        picker = DestinationPicker(data)
        rural = picker.filter_rural()
        chosen = picker.pick_random(rural)
        print_result(chosen)
        return

    # 确定出发地坐标
    origin_lon, origin_lat = args.lon, args.lat

    if not (origin_lon and origin_lat):
        if not args.city:
            print("错误: 请提供 --city 或 --lat/--lon")
            sys.exit(1)

        print(f"🔍 查找 {args.city} 的坐标...")
        loc = amap.geocode(args.city)
        if not loc:
            print(f"错误: 无法找到 {args.city} 的位置")
            sys.exit(1)
        origin_lon, origin_lat = loc["lon"], loc["lat"]
        print(f"✅ 找到: {origin_lat}, {origin_lon}")

    # 获取周边区县
    district_name = args.district or args.city or "上海"
    print(f"🔍 获取 {district_name} 周边区县...")

    districts = amap.district(district_name, subdistrict=2)
    if not districts:
        print("错误: 无法获取行政区划数据")
        sys.exit(1)

    print(f"✅ 找到 {len(districts)} 个下级行政区")

    # 随机选择并验证车程
    picker = DestinationPicker(districts)

    # 先过滤农村类型
    rural = picker.filter_rural()
    print(f"🌾 其中 {len(rural)} 个农村/小镇")

    if not rural:
        print("警告: 没有找到农村类型区域，使用全部区域")
        rural = districts

    # 尝试找到符合车程限制的目的地
    max_duration_sec = args.max_duration * 60
    chosen = None
    attempts = 0
    max_attempts = 20

    while attempts < max_attempts:
        candidate = picker.pick_random(rural)
        attempts += 1

        if not candidate.get("center"):
            continue

        dest_lon, dest_lat = candidate["center"].split(",")
        dest_lon, dest_lat = float(dest_lon), float(dest_lat)

        route = amap.driving_route(
            (origin_lon, origin_lat),
            (dest_lon, dest_lat)
        )

        if route:
            duration = route["duration"]
            distance = route["distance"]
            if duration <= max_duration_sec:
                chosen = candidate
                print_result(chosen, distance, duration)
                return

    if not chosen:
        # 没找到符合车程的，退而求其次随便选一个
        chosen = picker.pick_random(rural)
        print(f"⚠️ 未找到{args.max_duration}分钟内可达的目的地，随机选一个：")
        print_result(chosen)


if __name__ == "__main__":
    main()
