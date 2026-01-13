import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def setup_driver():
    chrome_options = Options()
    
    # --- GitHub Action 核心配置 ---
    # 无头模式：因为服务器没有显示器，必须开启
    chrome_options.add_argument("--headless=new") 
    # 解决 Linux 容器中的权限和内存问题
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # --- 反爬虫伪装配置 ---
    # 设置窗口大小，防止因视窗过小被检测
    chrome_options.add_argument("--window-size=1920,1080")
    # 伪装 User-Agent，假装是正常的 Windows 电脑
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # 禁用自动化标志（关键：防止被识别为 Robot）
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 使用 webdriver_manager 自动安装并启动对应版本的驱动
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def run_scraper():
    driver = None
    try:
        print("启动 Chrome 浏览器...")
        driver = setup_driver()
        
        # 访问知乎的一个具体问题页面（比首页更容易访问，首页往往强制登录）
        url = "https://space.bilibili.com/285286947" 
        print(f"正在访问: {url}")
        
        driver.get(url)
        
        # 等待页面加载
        time.sleep(10)
        
        # 获取并打印页面标题
        title = driver.title
        print(f"页面标题: {title}")
        
        # 简单的抓取测试：尝试获取页面上的导航栏文本或某个元素
        # 注意：Zhihu 的 class name 经常变动，这里我们抓取 title 或 h1 这种通用标签
        print("页面内容片段 (前500字符):")
        print(driver.page_source[:2000])

        if "知乎" in title:
            print("✅ 成功访问知乎！")
        else:
            print("⚠️ 访问可能受限或遭遇验证码。")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭。")

if __name__ == "__main__":
    run_scraper()