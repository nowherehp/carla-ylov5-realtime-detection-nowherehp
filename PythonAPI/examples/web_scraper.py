
# # =================================================================================================
# # -- IMPORT ---------------------------------------------------------------------------------------
# # =================================================================================================

# import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import pandas as pd
# import time
# import requests
# import colorama 
# from colorama import Fore, Back, Style
# from selenium.webdriver.common.by import By

# colorama.init()

# # =================================================================================================
# # -- LIST OF URLS ---------------------------------------------------------------------------------
# # =================================================================================================

# def fetch_image_urls(query: str, max_link_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):

#     # scroll to the end of the page 
#     def scroll_to_end(wd):
#         wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(5)

#     # make the url with the search term
#     search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

#     # load the page 
#     wd.get(search_url.format(q=query))

#     image_urls = set()
#     image_count = 0
#     results_start = 0

#     # looping over in page to find images 
#     while image_count < max_link_to_fetch:

#         scroll_to_end(wd)

#         # get all image thumbnail results 
#         # thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
#         thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
#         number_results = len(thumbnail_results)

#         print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

#         # clicking on the images and waiting till it loads 
#         for img in thumbnail_results[results_start:number_results]:
#             try: 
#                 img.click()
#                 time.sleep(sleep_between_interactions)
#             except Exception:
#                 continue 

#         # extract image urls
#             actual_images =wd.find_elements(By.CSS_SELECTOR,'img.sFlh5c')
#             for actual_image in actual_images:
#                 if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
#                     image_urls.add(actual_image.get_attribute('src'))

#             image_count = len(image_urls)

#             if len(image_urls) >= max_link_to_fetch:
#                 print(f"Found: {len(image_urls)} image links, done!")
#                 break
#         else: 
#             print("Found:", len(image_urls), "image links, looking for more ...")
#             time.sleep(30)
#             load_more_button = wd.find_elements(By.CSS_SELECTOR,".mye4qd")
#             if load_more_button:
#                 wd.execute_script("document.querySelector('.mye4qd').click();")

#         # move the result startpoint further down
#         results_start = len(thumbnail_results)

#     return image_urls

# # =================================================================================================
# # --  ---------------------------------------------------------------------------------------------
# # =================================================================================================

# def persist_image(folder_path: str, url: str, counter):
#     try:
#         image_content = requests.get(url).content
#     except Exception as e:
#         print(f"ERROR - Could not download {url} - {e}")


#     try:
#         f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
#         f.write(image_content)
#         f.close()

#         print(f"SUCCESS - saved {url} - as {folder_path}")

#     except Exception as e:
#         print(f"ERROR - Could not save {url} - {e}")

# # =================================================================================================
# # -- DOWNLOADING THE IMAGES -----------------------------------------------------------------------
# # =================================================================================================

# def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images: int=5): 

#     target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))            # updates the target folder path to .\image\search-term

#     if not os.path.exists(target_folder):                                                          # makes the directory if there is none
#         os.makedirs(target_folder)

#     # with webdriver.Chrome(executable_path=driver_path) as wd:                                      # finds the chrome driver 
#     from selenium.webdriver.chrome.service import Service

#     service = Service(driver_path)
#     with webdriver.Chrome(service=service) as wd:
#         res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=15)   # gathers the urls 
 
#     for counter, elem in enumerate(res):                                                           # loops over the urls 
#         persist_image(target_folder, elem, counter)                                                # downloads the content of the urls


# # =================================================================================================
# # -- LOOP -----------------------------------------------------------------------
# # =================================================================================================

# def loop():
    
#     DRIVER_PATH = 'C:\\webdriver\\chromedriver.exe'
#     ############################################
    
#     # looping over until input "exit" recieved by user
#     while True: 
#         print(Fore.GREEN + "\nexit - quit the script", "s search--term - starts searching the web" + Fore.WHITE, sep='\n')

#         input_string = input("Input command: ") # input command

#         if input_string == "exit":              # in case of entering "exit", exits the scripts
#             break

#         elif input_string[0] == "s":            # in case of entering "s search-term", initialize the search and download script
#             search_term = input_string[2:]
#             try:
#                 N_IMAGES = int(input('Number of Images: '))
#             except:
#                 print(Fore.RED + "Input must be an integer" + Fore.WHITE)
#                 continue
#             search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=N_IMAGES)
        
#         else:                                   # in any other case of input, goes back to the start of the loop
#             pass

        

# # =================================================================================================
# # -- DOWNLOADING THE IMAGES -----------------------------------------------------------------------
# # =================================================================================================

# loop()

# import os
# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from colorama import Fore, Style, init

# init(autoreset=True)

# def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
#     def scroll_to_end(wd):
#         wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # 缩短等待时间

#     # 生成搜索 URL
#     search_url = f"https://www.google.com/search?safe=off&site=&tbm=isch&q={query}"
#     wd.get(search_url)

#     image_urls = set()
#     results_start = 0

#     while len(image_urls) < max_links_to_fetch:
#         scroll_to_end(wd)  # 滚动页面以加载更多图片
#         thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
#         number_results = len(thumbnail_results)

#         print(f"Found: {number_results} thumbnail results. Extracting links...")

#         for img in thumbnail_results[results_start:number_results]:
#             try:
#                 img.click()  # 点击缩略图以加载大图
#                 time.sleep(sleep_between_interactions)
#             except Exception:
#                 continue

#             # 获取大图 URL
#             actual_images = wd.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
#             for actual_image in actual_images:
#                 src = actual_image.get_attribute("src")
#                 if src and "http" in src:
#                     image_urls.add(src)

#             if len(image_urls) >= max_links_to_fetch:
#                 print(f"Found {len(image_urls)} image links, stopping search.")
#                 break

#         # 更新结果起点，避免重复点击同样的缩略图
#         results_start = len(thumbnail_results)

#         # 如果已经达到目标数量，则停止
#         if len(image_urls) >= max_links_to_fetch:
#             break

#     return image_urls

# def persist_image(folder_path: str, url: str, counter):
#     try:
#         image_content = requests.get(url).content
#     except Exception as e:
#         print(f"ERROR - Could not download {url} - {e}")
#         return

#     try:
#         with open(os.path.join(folder_path, f"jpg_{counter}.jpg"), 'wb') as f:
#             f.write(image_content)
#         print(f"SUCCESS - saved {url} - as {folder_path}")
#     except Exception as e:
#         print(f"ERROR - Could not save {url} - {e}")

# def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images: int=30): 
#     # 设置目标文件夹
#     target_folder = os.path.join(target_path, '_'.join(search_term.lower().split()))
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)

#     service = Service(driver_path)
#     with webdriver.Chrome(service=service) as wd:
#         res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=1)
 
#     for counter, elem in enumerate(res):  # 保存图片
#         persist_image(target_folder, elem, counter)

# def loop():
#     DRIVER_PATH = 'C:\\webdriver\\chromedriver.exe'
    
#     while True: 
#         print(Fore.GREEN + "\nexit - quit the script", "s search--term - starts searching the web" + Style.RESET_ALL)
#         input_string = input("Input command: ")  # 输入指令

#         if input_string == "exit":
#             break
#         elif input_string.startswith("s "):
#             search_term = input_string[2:]
#             try:
#                 N_IMAGES = int(input('Number of Images: '))
#             except ValueError:
#                 print(Fore.RED + "Input must be an integer" + Style.RESET_ALL)
#                 continue
#             search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=N_IMAGES)
#         else:
#             print(Fore.RED + "Invalid command." + Style.RESET_ALL)

# loop()


# import os, requests, lxml, re, json, urllib.request
# from bs4 import BeautifulSoup
# from serpapi import GoogleSearch

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    
# }

# params = {
#     "q": "mincraft wallpaper 4k", # search query
#     "tbm": "isch",                # image results
#     "hl": "en",                   # language of the search
#     "gl": "us",                   # country where search comes from
#     "ijn": "0" ,                   # page number
#     "api_key": "b3cd5d3fef9b60966ea037d0600c11b3f212ddf4a2bc97de84ad4cf572757a39"     # SerpAPI API Key
# }

# html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
# soup = BeautifulSoup(html.text, "lxml")

# def get_images_with_request_headers():
#     del params["ijn"]
#     params["content-type"] = "image/png" # parameter that indicate the original media type

#     return [img["src"] for img in soup.select("img")]

# def get_suggested_search_data():
#     suggested_searches = []

#     all_script_tags = soup.select("script")

#     # https://regex101.com/r/48UZhY/6
#     matched_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))

#     # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
#     # if you try to json.loads() without json.dumps it will throw an error:
#     # "Expecting property name enclosed in double quotes"
#     matched_images_data_fix = json.dumps(matched_images)
#     matched_images_data_json = json.loads(matched_images_data_fix)

#     # search for only suggested search thumbnails related
#     # https://regex101.com/r/ITluak/2
#     suggested_search_thumbnails = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

#     # https://regex101.com/r/MyNLUk/1
#     suggested_search_thumbnail_encoded = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails)

#     for suggested_search, suggested_search_fixed_thumbnail in zip(soup.select(".PKhmud.sc-it.tzVsfd"), suggested_search_thumbnail_encoded):
#         suggested_searches.append({
#             "name": suggested_search.select_one(".VlHyHc").text,
#             "link": f"https://www.google.com{suggested_search.a['href']}",
#             # https://regex101.com/r/y51ZoC/1
#             "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
#             # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
#             "thumbnail": bytes(suggested_search_fixed_thumbnail, "ascii").decode("unicode-escape")
#         })

#     return suggested_searches

# def get_original_images():

#     """
#     https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
#     if you try to json.loads() without json.dumps() it will throw an error:
#     "Expecting property name enclosed in double quotes"
#     """

#     google_images = []

#     all_script_tags = soup.select("script")

#     # # https://regex101.com/r/48UZhY/4
#     matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

#     matched_images_data_fix = json.dumps(matched_images_data)
#     matched_images_data_json = json.loads(matched_images_data_fix)

#     # https://regex101.com/r/pdZOnW/3
#     matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

#     # https://regex101.com/r/NnRg27/1
#     matched_google_images_thumbnails = ", ".join(
#         re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
#                    str(matched_google_image_data))).split(", ")

#     thumbnails = [
#         bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
#     ]

#     # removing previously matched thumbnails for easier full resolution image matches.
#     removed_matched_google_images_thumbnails = re.sub(
#         r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

#     # https://regex101.com/r/fXjfb1/4
#     # https://stackoverflow.com/a/19821774/15164646
#     matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

#     full_res_images = [
#         bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
#     ]

#     for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
#         google_images.append({
#             "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
#             "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
#             "source": metadata.select_one(".fxgdke").text,
#             "thumbnail": thumbnail,
#             "original": original
#         })

#         # Download original images
#         print(f'Downloading {index} image...')

#         opener=urllib.request.build_opener()
#         opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')]
#         urllib.request.install_opener(opener)

#         urllib.request.urlretrieve(original, f'Bs4_Images/original_size_img_{index}.jpg')

#     return google_images


# # 主程序入口
# if __name__ == "__main__":
#     # 创建保存图片的文件夹
#     if not os.path.exists("Bs4_Images"):
#         os.makedirs("Bs4_Images")

#     # 获取并打印原始图片链接
#     google_images = get_original_images()
#     print("Downloaded images info:", google_images)

import os
import json
import urllib.request
from serpapi import GoogleSearch

def serpapi_get_google_images():
    image_results = []

    # 替换 API_KEY 环境变量
    api_key = "b3cd5d3fef9b60966ea037d0600c11b3f212ddf4a2bc97de84ad4cf572757a39"

    for query in ["road with cars and people"]:
        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            "api_key": api_key                # SerpAPI API Key
        }

        search = GoogleSearch(params)         # where data extraction happens

        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary

            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if image["original"] not in image_results:
                        image_results.append(image["original"])

                # update to the next page
                params["ijn"] += 1
            else:
                images_is_present = False
                print(results["error"])

    # -----------------------
    # 创建图片保存的目录
    os.makedirs("SerpApi_Images", exist_ok=True)

    # 下载图片
    for index, image_url in enumerate(image_results, start=1):
        print(f"Downloading image {index}...")

        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
        urllib.request.install_opener(opener)

        try:
            urllib.request.urlretrieve(image_url, f"SerpApi_Images/original_size_img_{index}.jpg")
            print(f"Image {index} downloaded successfully.")
        except Exception as e:
            print(f"Error downloading image {index}: {e}")

    # 打印结果
    print(json.dumps(image_results, indent=2))
    print(f"Total images downloaded: {len(image_results)}")

# 调用函数
serpapi_get_google_images()
