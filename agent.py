

```python
# -*- coding: utf-8 -*-
"""
【大三计算机课程实践】简易网页文本爬虫（教学版）
功能：抓取指定网页中的所有段落文本（<p>标签），清洗后保存为 Excel 文件
目标URL：http://httpbin.org/html （公开、稳定、无反爬、适合练习）
依赖库：requests, beautifulsoup4, pandas, openpyxl
安装命令（首次运行前执行）：
    pip install requests beautifulsoup4 pandas openpyxl
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

def fetch_html(url: str) -> str:
    """获取网页HTML内容，带基础请求头和错误处理"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        print(f"正在请求 {url} ...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误（如404、500）
        response.encoding = response.apparent_encoding  # 自动识别编码
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        sys.exit(1)

def parse_paragraphs(html: str) -> list:
    """解析HTML，提取所有 <p> 标签内的纯文本（去空行、去首尾空格）"""
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:  # 过滤空段落
            paragraphs.append(text)
    print(f"✅ 成功提取 {len(paragraphs)} 段有效文本")
    return paragraphs

def save_to_excel(data: list, filename: str = "scraped_data.xlsx"):
    """将文本列表保存为 Excel（单列：'Text'）"""
    df = pd.DataFrame({"Text": data})
    try:
        df.to_excel(filename, index=False)
        print(f"✅ 数据已保存至：{filename}")
        print(f"📊 共 {len(df)} 行数据")
    except Exception as e:
        print(f"❌ 保存Excel失败：{e}")
        sys.exit(1)

def main():
    # 🔧 可修改此处URL（务必确保合法合规！）
    target_url = "http://httpbin.org/html"

    print("🚀 开始执行爬虫任务...")
    html = fetch_html(target_url)
    texts = parse_paragraphs(html)
    
    if not texts:
        print("⚠️  未提取到任何文本，请检查网页结构或URL是否正确。")
        return

    save_to_excel(texts, "web_text_output.xlsx")

if __name__ == "__main__":
    main()
```

---

