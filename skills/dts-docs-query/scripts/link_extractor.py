#!/usr/bin/env python3
"""
链接提取器
从 HTML 中提取引用的类型链接
"""

import sys
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
import json

def extract_links(html_file: str) -> List[str]:
    """提取 HTML 中的类型链接"""
    html = Path(html_file).read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    links = []
    seen = set()

    # 查找所有 a 标签
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']

        # 只提取指向其他类的链接
        if href.endswith('.html') and '/' not in href and href != 'index.html':
            class_name = href.replace('.html', '')

            # 去重
            if class_name not in seen:
                seen.add(class_name)
                links.append(class_name)

    return links

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python link_extractor.py <html_file>")
        sys.exit(1)

    links = extract_links(sys.argv[1])

    # 输出为 JSON 格式，方便程序调用
    print(json.dumps(links, indent=2, ensure_ascii=False))
