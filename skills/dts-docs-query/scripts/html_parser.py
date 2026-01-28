#!/usr/bin/env python3
"""
JSDoc HTML 解析器
从 DTS SDK 文档 HTML 中提取 API 信息
"""

import sys
import json
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List, Any

def parse(html_file: str) -> Dict[str, Any]:
    """解析 HTML 文件，提取 API 信息"""
    html = Path(html_file).read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    # 提取类名
    class_name = soup.find('h1', class_='page-title').text.strip().replace('Class: ', '')

    # 提取类描述
    class_desc_elem = soup.find('div', class_='class-description')
    class_description = class_desc_elem.get_text(strip=True) if class_desc_elem else ''

    # 提取所有方法
    methods = []
    method_elements = soup.find_all('h4', class_='name')

    for method_elem in method_elements:
        method_id = method_elem.get('id', '')

        # 跳过构造函数
        if method_id == class_name:
            continue

        # 提取方法签名
        signature_elem = method_elem.find('span', class_='signature')
        signature = signature_elem.text if signature_elem else ''

        # 提取方法描述
        # 找到下一个 dd 元素中的 description
        dd_element = method_elem.find_next('dd')
        description_elem = dd_element.find('div', class_='description') if dd_element else None
        description = description_elem.get_text(strip=True) if description_elem else ''

        # 提取参数
        parameters = []
        params_table = dd_element.find('table', class_='params') if dd_element else None

        if params_table:
            tbody = params_table.find('tbody')
            if tbody:
                for tr in tbody.find_all('tr'):
                    name_td = tr.find('td', class_='name')
                    type_td = tr.find('td', class_='type')
                    desc_td = tr.find('td', class_='last')

                    if name_td:
                        param_name = name_td.text.strip()
                        param_type = type_td.text.strip() if type_td else 'unknown'
                        param_desc = desc_td.get_text(strip=True) if desc_td else ''

                        parameters.append({
                            'name': param_name,
                            'type': param_type,
                            'description': param_desc
                        })

        # 提取返回值
        returns = None
        returns_elem = dd_element.find('h5', string='Returns:') if dd_element else None
        if returns_elem:
            returns_div = returns_elem.find_next('div')
            if returns_div:
                returns = returns_div.get_text(strip=True)

        # 提取示例
        examples = []
        example_elem = dd_element.find('h5', string='Example:') if dd_element else None
        if example_elem:
            pre_elem = example_elem.find_next('pre')
            if pre_elem:
                code_elem = pre_elem.find('code')
                if code_elem:
                    examples.append(code_elem.text)

        method = {
            'name': method_id,
            'signature': f"{method_id}{signature}",
            'description': description,
            'parameters': parameters,
            'returns': returns,
            'examples': examples
        }

        methods.append(method)

    result = {
        'class_name': class_name,
        'description': class_description,
        'methods': methods,
        'source_url': ''  # 将在调用时设置
    }

    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python html_parser.py <html_file>")
        sys.exit(1)

    result = parse(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
