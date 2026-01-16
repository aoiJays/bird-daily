import json
import os
import time
import subprocess
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 导入你在 spider.py 中定义的 setup_driver
from spider import setup_driver

def _get_selenium_data(url):
    """
    内部辅助函数：启动 Selenium，渲染页面，提取 Title, PlayInfo, CID, Cookies
    """
    driver = setup_driver()
    try:
        print(f"🕵️ [Selenium] 正在渲染页面: {url}")
        driver.get(url)

        # 1. 显式等待：确保 B 站播放器核心数据加载完成
        # 等待 video 标签出现，或者等待 window.__playinfo__ 变量可用
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return (typeof window.__playinfo__ !== 'undefined')")
        )

        # 2. 提取页面标题
        title = driver.title.replace("_哔哩哔哩_bilibili", "").strip()
        # 清理非法文件名字符
        import re
        title = re.sub(r'[\\/*?:"<>|]', '', title)

        # 3. 执行 JS 获取视频流信息 (PlayInfo)
        play_info = driver.execute_script("return window.__playinfo__")

        # 4. 执行 JS 获取初始状态信息 (包含 CID)
        # B站通常将 CID 放在 window.__INITIAL_STATE__.videoData.cid
        cid = driver.execute_script("""
            try {
                return window.__INITIAL_STATE__.videoData.cid;
            } catch (e) {
                return null;
            }
        """)

        # 5. 获取当前会话的 Cookies 和 User-Agent (用于传给 requests)
        selenium_cookies = driver.get_cookies()
        user_agent = driver.execute_script("return navigator.userAgent")

        # 将 Selenium 的 Cookie 列表转换为 requests 字典格式
        cookies_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

        return {
            "title": title,
            "play_info": play_info,
            "cid": cid,
            "cookies": cookies_dict,
            "user_agent": user_agent
        }

    except Exception as e:
        print(f"❌ [Selenium] 页面解析失败: {e}")
        return None
    finally:
        driver.quit() # 务必关闭浏览器

def download_bilibili_audio(url, output_path='.', filename=None, audio_format='mp3'):
    """
    使用 Selenium 解析，Requests 下载，FFmpeg 转码
    """
    # 1. 获取数据
    data = _get_selenium_data(url)
    if not data:
        return

    # 准备路径
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    final_name = filename if filename else data['title']
    output_file = os.path.join(output_path, f"{final_name}.{audio_format}")
    temp_file = os.path.join(output_path, f"{final_name}_temp.m4s")

    # 2. 解析音频流地址
    try:
        # 尝试获取 DASH 音频流
        audios = data['play_info']['data']['dash']['audio']
        if not audios:
            print("❌ 未找到音频流。")
            return
        # 取第一个通常是最高音质
        audio_url = audios[0]['baseUrl']
    except KeyError:
        print("❌ 解析 playinfo 结构失败。")
        return

    # 3. 使用 requests 下载 (带上 Selenium 获取的 Cookie 和 UA)
    headers = {
        "User-Agent": data['user_agent'],
        "Referer": url # 必须带 Referer
    }

    print(f"⬇️ 正在下载流文件 (借助 Selenium 身份)...")
    try:
        with requests.get(audio_url, headers=headers, cookies=data['cookies'], stream=True) as r:
            if r.status_code == 412:
                print("❌ 依然触发 412，可能是 IP 限制。")
                return
            r.raise_for_status()
            with open(temp_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"❌ 下载流文件失败: {e}")
        return

    # 4. FFmpeg 转码
    print(f"🎵 正在转码为 {audio_format}...")
    try:
        cmd = [
            'ffmpeg', '-i', temp_file,
            '-vn', '-y', '-loglevel', 'error',
            output_file
        ]
        if audio_format == 'mp3':
            cmd.extend(['-acodec', 'libmp3lame', '-q:a', '0'])
        
        subprocess.run(cmd, check=True)
        os.remove(temp_file) # 清理临时文件
        print(f"✅ 音频下载完成: {output_file}")
    except Exception as e:
        print(f"❌ FFmpeg 转码失败 (请确保系统安装了 ffmpeg): {e}")

def download_danmu(video_url, output_dir="danmaku_downloads", filename=None):
    """
    使用 Selenium 获取 CID，然后下载弹幕 XML
    """
    # 1. 获取数据 (主要是 CID)
    data = _get_selenium_data(video_url)
    if not data or not data['cid']:
        print("❌ 无法获取 CID，无法下载弹幕。")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    final_name = filename if filename else data['title']
    output_file = os.path.join(output_dir, f"{final_name}.xml")

    # 2. 构造弹幕接口并下载
    # 弹幕接口不需要太严格的 cookie，普通 requests 即可
    danmu_url = f"https://comment.bilibili.com/{data['cid']}.xml"
    
    print(f"🚀 正在下载弹幕 (CID: {data['cid']})...")
    try:
        r = requests.get(danmu_url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f"✅ 弹幕保存成功: {output_file}")
    except Exception as e:
        print(f"❌ 弹幕下载失败: {e}")

if __name__ == "__main__":
    # 替换 BV 号
    target_url = "https://www.bilibili.com/video/BV1pdroBiEMg"
    
    # 1. 下载音频
    download_bilibili_audio(target_url, 
                            output_path="downloads", 
                            filename="selenium_audio", 
                            audio_format="mp3")
    
    # 2. 下载弹幕
    download_danmu(target_url)