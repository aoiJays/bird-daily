from spider import setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


def get_up_video_list(up_id: int, max_retries=5):

    url = f"https://space.bilibili.com/{up_id}/upload/video"
    print(f"[get_up_video_list] 目标 URL: {url}")

    result = []
    for attempt in range(1, max_retries + 1):
        driver = None
        try:
            print(f"[get_up_video_list]--- 第 {attempt} 次尝试 ---")
            driver = setup_driver()
            
            # 设置页面加载超时，防止卡死
            driver.set_page_load_timeout(15) 
            
            print("[get_up_video_list]正在加载页面...")
            driver.get(url)

            time.sleep(1)  
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(0, -500);")
            # 【关键修改】使用显式等待 (Explicit Wait)
            # 等待直到 'bili-video-card__title' 元素出现，最多等 10 秒
            # 这比 time.sleep(30) 更快且更准
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "bili-video-card__title"))
                )
                print("[get_up_video_list]页面元素渲染成功！")
            except Exception:
                raise Exception("[get_up_video_list]等待元素超时，可能触发了反爬或网络慢，准备重试...")

            try:
                videos = driver.find_elements(By.CLASS_NAME, "bili-video-card")

                for video in videos:
                    # 使用相对定位查找内部元素
                    title_el = video.find_element(By.CLASS_NAME, "bili-video-card__title")
                    link_el = title_el.find_element(By.TAG_NAME, "a")

                    video_title = title_el.text
                    video_link = link_el.get_attribute("href")
                    date_el = video.find_element(By.CLASS_NAME, "bili-video-card__subtitle")
                    result.append({
                        "title": video_title,
                        "link": video_link,
                        "date": date_el.text
                    })
                print(f"[get_up_video_list]成功获取 {len(result)} 个视频信息。")
                break
            except Exception as e:
                raise Exception(f"[get_up_video_list]解析页面时出错: {e}")

        except Exception as e:
            print(f"第 {attempt} 次尝试失败: {e}")
            print(e)
            if attempt < max_retries:
                print("清理环境，3秒后重试...")
                time.sleep(3)
            else:
                print("所有重试均失败。")
        
        finally:
            # 【关键修改】无论成功还是失败，必须关闭浏览器
            if driver:
                print("关闭浏览器实例...")
                driver.quit()

    return result

