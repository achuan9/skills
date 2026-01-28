#!/usr/bin/env python3
"""
HTTP 请求客户端
下载 DTS SDK 文档 HTML，支持重试和超时
"""

import requests
from pathlib import Path
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import chardet

def fetch(url: str, output_file: str = None) -> tuple[str, int]:
    """下载 HTML 内容

    Args:
        url: 目标 URL
        output_file: 可选的输出文件路径

    Returns:
        (HTML 内容, 状态码)
    """
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, timeout=30)

        # 智能编码检测
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            detected = chardet.detect(response.content)
            if detected['confidence'] > 0.9:
                response.encoding = detected['encoding']
            else:
                # 尝试常见中文编码
                for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                    try:
                        response.content.decode(enc)
                        response.encoding = enc
                        break
                    except:
                        continue

        html = response.text
        status_code = response.status_code

        if status_code == 200 and output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            Path(output_file).write_text(html, encoding='utf-8')

        return html, status_code
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None, 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python http_fetcher.py <url> [output_file]")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    html, status = fetch(url, output)

    if html:
        print(f"Status: {status}")
        if status == 200:
            print("Successfully fetched HTML")
        else:
            print(f"HTTP Error: {status}")
    else:
        print("Failed to fetch HTML")
        sys.exit(1)
