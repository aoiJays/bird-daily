from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver
