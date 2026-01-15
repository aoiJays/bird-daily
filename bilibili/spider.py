from spider import setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import time


def get_up_video_list(up_id: int):
    print("启动 Chrome 浏览器...")

    result = []
    try:
        driver = setup_driver()
        print('浏览器启动成功')


        url = f"https://space.bilibili.com/{up_id}/upload/video" 
        print(f"正在访问: {url}")
        driver.get(url)
        time.sleep(10)  # 等待页面加载
        print('页面加载完成，开始解析视频列表...')

        try:
            # 此时页面已渲染，获取所有视频元素（Selenium 直接查找，无需 BS4）
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

        except Exception as e:
            print(f"加载超时或出错: {e}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭。")
        print('spider结束')

    print(f"共获取到 {len(result)} 个视频。")
    return result