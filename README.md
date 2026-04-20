# 周末去哪_安静版

> 随机选一个周边农村，说走就走，不规划，不纠结。

## 理念

生活太累了，不想做攻略。  
打开程序，随机一个目的地，两小时车程内的农村/小镇/古镇。  
不用想，去了再说。

## 功能

- 🎲 **随机目的地** — 输入你所在位置，随机选出周边农村/小镇
- 🚗 **车程筛选** — 只选2小时内能到的
- 📍 **地图展示** — 显示目的地位置和路线
- 📝 **简要信息** — 目的地简介、最佳出行季节、推荐理由

## 快速开始

### Python CLI

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（需要配置高德地图 API Key）
cp .env.example .env
# 编辑 .env，填入 AMAP_KEY

# 随机选一个目的地
python src/main.py

# 指定出发地
python src/main.py --lat 31.2304 --lon 121.4737

# 指定最大车程（分钟）
python src/main.py --max-duration 90
```

### Web界面

```bash
cd web
python -m http.server 8080
```

打开 http://localhost:8080

### Docker

```bash
docker build -t weekend-where .
docker run --env-file .env -p 8080:8080 weekend-where
```

## 项目结构

```
weekend_where_to_go_quiet/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── main.py           # CLI 入口
│   ├── picker.py         # 随机选择逻辑
│   ├── amap.py           # 高德地图 API
│   └── data_loader.py    # 数据加载
├── web/
│   ├── index.html        # Web界面
│   └── style.css
└── data/
    └── sample.json       # 示例数据
```

## 数据来源

- 行政区划数据：高德地图行政区划 API
- 地理编码：高德地图地理编码 API
- 路线规划：高德地图路径规划 API

## 免责声明

本项目仅供学习交流，API 调用产生的费用由用户自行承担。

## License

MIT
