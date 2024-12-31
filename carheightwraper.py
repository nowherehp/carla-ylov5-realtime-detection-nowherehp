import requests
from bs4 import BeautifulSoup
import time
import re
from application_graph import ApplicationGraph  # 导入特征图模块

app_graph = ApplicationGraph()

# Wikipedia API URL
API_URL = "https://en.wikipedia.org/w/api.php"

# 修正后的车辆列表
vehicles = [
    "audi a2",
    "Audi ETron",
    "Audi TT",
    "BMW GranTourer",
    "Chevrolet Impala",
    "Citroen C3",
    "Dodge Charger 2020",
    "Dodge Police Charger",
    "Ford  Crown",
    "Ford  Mustang",
    "Jeep  Wrangler Rubicon",
    "Lincoln  MKZ 2017",
    "Lincoln  MKZ 2020",
    "Mercedes  Coupe",
    "Mercedes  Coupe 2020",
    "Micro Microlino",
    "Mini Cooper S",
    "Mini Cooper S 2021",
    "Nissan Micra",
    "Nissan Patrol",
    "Nissan Patrol 2021",
    "Seat Leon",
    "Tesla  Model 3",
    "Toyota  Prius",
    "CARLA Motors CarlaCola",
    "European HGV (cab-over-engine type)",
    "Firetruck",
    "Tesla  Cybertruck",
    "Mercedes  Sprinter",
    "Volkswagen T2",
    "Volkswagen  T2 2021",
    "Mitsubishi  Fusorosa",
    "Harley Davidson Low Rider",
    "Kawasaki  Ninja",
    "Vespa ZX 125",
    "Yamaha YZF",
    "BH Crossbike",
    "Diamondback  Century",
    "Gazelle Omafiets"
]

# 添加初始化任务到特征图
app_graph.add_task("Initialize Vehicle Height Extraction", compute_time=0.2, data_volume=1)

# 定义函数从所有 Infobox 提取高度并简化输出
def get_vehicle_height_from_all_infoboxes(vehicle_name):
    # 添加任务到特征图
    app_graph.add_task("Fetch Vehicle Data", ["Initialize Vehicle Height Extraction"], compute_time=0.3, data_volume=2)
    # 获取页面标题
    title = get_best_match_title(vehicle_name)
    if not title:
        return f"{vehicle_name}: cannot get it"

    # 获取页面 HTML
    params = {
        "action": "parse",
        "page": title,
        "format": "json"
    }
    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        return f"{vehicle_name}: cannot get it"

    data = response.json()
    html_content = data.get("parse", {}).get("text", {}).get("*", "")
    if not html_content:
        return f"{vehicle_name}: cannot get it"

    # 解析 HTML 并遍历所有 Infobox
    soup = BeautifulSoup(html_content, "html.parser")
    infoboxes = soup.find_all("table", {"class": "infobox"})  # 找到所有 Infobox
    if not infoboxes:
        return f"{vehicle_name}: cannot get it"

    # 遍历 Infobox，寻找高度
    for infobox in infoboxes:
        rows = infobox.find_all("tr")
        for row in rows:
            header = row.find("th")
            if header and "height" in header.text.lower():
                height_data = row.find("td")
                if height_data:
                    # 提取高度并简化为 "数字+in"
                    height_text = height_data.text.strip()
                    match = re.search(r"([\d.]+)\s*in", height_text)
                    if match:
                        return f"{vehicle_name}: {match.group(1)}in"  # 提取第一个 in 前的数值

    return f"{vehicle_name}: cannot get it"

# 获取页面标题
def get_best_match_title(vehicle_name):
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": vehicle_name,
        "format": "json"
    }
    response = requests.get(API_URL, params=search_params)
    if response.status_code != 200:
        return None

    search_data = response.json()
    search_results = search_data.get("query", {}).get("search", [])
    if not search_results:
        return None

    return search_results[0]["title"]

# 保存结果到文件
output_file = "vehicle_heights_simplified.txt"

with open(output_file, "w") as file:
    for vehicle in vehicles:
        # 添加每个车辆提取任务到特征图
        app_graph.add_task(f"Extract Height for {vehicle}", ["Fetch Vehicle Data"], compute_time=0.1, data_volume=1)
        result = get_vehicle_height_from_all_infoboxes(vehicle)
        print(result)  # 同时打印结果到控制台
        file.write(result + "\n")
        time.sleep(1)  # 延迟避免触发速率限制

# 添加保存结果任务到特征图
app_graph.add_task("Save Results", ["Extract Height for Vehicles"], compute_time=0.5, data_volume=1)

# 分析并可视化特征图
app_graph.analyze_graph()
app_graph.visualize_graph()