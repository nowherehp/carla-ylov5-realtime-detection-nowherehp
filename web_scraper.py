

import os
import json
import urllib.request
from serpapi import GoogleSearch
from application_graph import ApplicationGraph  # 导入特征图模块
app_graph = ApplicationGraph()

# 初始化 Web Scraper 的任务
app_graph.add_task("Initialize Web Scraper", compute_time=0.2, data_volume=1)


# def serpapi_get_google_images():
#     image_results = []

#     # 替换 API_KEY 环境变量
#     api_key = "b3cd5d3fef9b60966ea037d0600c11b3f212ddf4a2bc97de84ad4cf572757a39"

#     for query in ["road with cars and people"]:
#         # search query parameters
#         params = {
#             "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
#             "q": query,                       # search query
#             "tbm": "isch",                    # image results
#             "num": "100",                     # number of images per page
#             "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
#             "api_key": api_key                # SerpAPI API Key
#         }

#         search = GoogleSearch(params)         # where data extraction happens

#         images_is_present = True
#         while images_is_present:
#             results = search.get_dict()       # JSON -> Python dictionary

#             # checks for "Google hasn't returned any results for this query."
#             if "error" not in results:
#                 for image in results["images_results"]:
#                     if image["original"] not in image_results:
#                         image_results.append(image["original"])

#                 # update to the next page
#                 params["ijn"] += 1
#             else:
#                 images_is_present = False
#                 print(results["error"])

                
#     # 添加下载图片任务到特征图
#     app_graph.add_task("Download Images", ["Fetch Image URLs"], compute_time=1.5, data_volume=len(image_results) * 2)
#     # -----------------------
#     # 创建图片保存的目录
#     os.makedirs("SerpApi_Images", exist_ok=True)

#     # 下载图片
#     for index, image_url in enumerate(image_results, start=1):
#         print(f"Downloading image {index}...")

#         opener = urllib.request.build_opener()
#         opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
#         urllib.request.install_opener(opener)

#         try:
#             urllib.request.urlretrieve(image_url, f"SerpApi_Images/original_size_img_{index}.jpg")
#             print(f"Image {index} downloaded successfully.")
#         except Exception as e:
#             print(f"Error downloading image {index}: {e}")


#     # 添加完成任务节点到特征图
#     app_graph.add_task("Complete Web Scraping", ["Download Images"], compute_time=0.2, data_volume=1)

#     # 打印结果
#     print(json.dumps(image_results, indent=2))
#     print(f"Total images downloaded: {len(image_results)}")
def serpapi_get_google_images():
    image_results = []

    # 替换 API_KEY 环境变量
    api_key = "b3cd5d3fef9b60966ea037d0600c11b3f212ddf4a2bc97de84ad4cf572757a39"

    try:
        # 添加提取图片 URL 的任务到特征图
        app_graph.add_task("Fetch Image URLs", ["Initialize Web Scraper"], compute_time=0.5, data_volume=5)

        for query in ["road with cars and people"]:
            params = {
                "engine": "google",
                "q": query,
                "tbm": "isch",
                "num": "100",
                "ijn": 0,
                "api_key": api_key
            }

            search = GoogleSearch(params)
            images_is_present = True
            while images_is_present:
                results = search.get_dict()
                if "error" not in results:
                    for image in results["images_results"]:
                        if image["original"] not in image_results:
                            image_results.append(image["original"])
                    params["ijn"] += 1
                else:
                    images_is_present = False
                    print(results["error"])

        # 添加下载图片任务到特征图
        app_graph.add_task("Download Images", ["Fetch Image URLs"], compute_time=1.5, data_volume=len(image_results) * 2)

        os.makedirs("SerpApi_Images", exist_ok=True)

        for index, image_url in enumerate(image_results, start=1):
            print(f"Downloading image {index}...")
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent", "Mozilla/5.0")]
            urllib.request.install_opener(opener)

            try:
                urllib.request.urlretrieve(image_url, f"SerpApi_Images/original_size_img_{index}.jpg")
                print(f"Image {index} downloaded successfully.")
            except Exception as e:
                print(f"Error downloading image {index}: {e}")

        # 添加完成任务到特征图
        app_graph.add_task("Complete Web Scraping", ["Download Images"], compute_time=0.2, data_volume=1)

    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # 分析和可视化特征图
        app_graph.analyze_graph()
        app_graph.visualize_graph()

    # 打印结果
    print(json.dumps(image_results, indent=2))
    print(f"Total images downloaded: {len(image_results)}")

# 调用函数
serpapi_get_google_images()

