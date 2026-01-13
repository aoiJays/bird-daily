import html2text
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()
    # 必须保留的无头模式配置，否则无法在 Action 中运行
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def run_scraper():
    driver = None
    target_url = "https://www.zhihu.com/people/xule.null/posts"
    search_keyword = "AI早报"
    
    try:
        driver = setup_driver()
        
        # 1. 访问列表页
        driver.get(target_url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ContentItem-title")))
        
        # 2. 查找符合条件的文章链接
        articles = driver.find_elements(By.CLASS_NAME, "ContentItem-title")
        target_link = None
        target_title = None

        for article in articles:
            try:
                link_elem = article.find_element(By.TAG_NAME, "a")
                title = link_elem.text
                if search_keyword in title:
                    target_title = title
                    target_link = link_elem.get_attribute("href")
                    break # 找到最新的第一篇就退出循环
            except:
                continue

        if not target_link:
            print("未找到包含 'AI早报' 的文章")
            return

        # 3. 进入详情页
        driver.get(target_link)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Post-RichText")))
        
        content_element = driver.find_element(By.CLASS_NAME, "Post-RichText")
        content_html = content_element.get_attribute("innerHTML")

        # 4. 转换为 Markdown
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.body_width = 0
        markdown_content = converter.handle(content_html)
        
        # 5. 直接输出字符串 (按照你的要求)
        final_output = f"# {target_title}\n\nOriginal URL: {target_link}\n\n---\n\n{markdown_content}"
        print(final_output)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_scraper()