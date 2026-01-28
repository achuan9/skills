#!/usr/bin/env python3
"""
DTS 文档查询主脚本
演示完整的查询流程
"""

import sys
import json
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from scripts.http_fetcher import fetch
from scripts.html_parser import parse
from scripts.cache_manager import check_cache, save_to_cache
from scripts.doc_generator import generate_markdown, get_default_output_dir

BASE_URL = 'https://sdk.freedo3d.com/doc/api/'

def query_api(api_path: str, method_name: str = None, save_doc: bool = True, output_dir: Path = None) -> dict:
    """查询 API 文档

    Args:
        api_path: API 路径，如 "acApi.marker"
        method_name: 可选的方法名，如 "add"
        save_doc: 是否自动保存 Markdown 文档，默认 True
        output_dir: 文档输出目录，默认使用用户主目录下的 DTS-Docs

    Returns:
        查询结果字典
    """
    # 1. 解析类名
    # acApi.marker -> Marker (忽略方法名)
    # acApi.marker.add -> Marker
    parts = api_path.split('.')

    # 移除 "acApi" 前缀
    if parts[0] == 'acApi':
        parts = parts[1:]

    # 取第一个部分作为类名（忽略方法名）
    # acApi.marker.add -> ['marker', 'add'] -> 'marker' -> 'Marker'
    # acApi.marker -> ['marker'] -> 'marker' -> 'Marker'
    if parts:
        class_name = parts[0].capitalize()
    else:
        class_name = 'Marker'  # 默认值

    print(f"Querying: {api_path}")
    print(f"Class name: {class_name}")
    if method_name:
        print(f"Method: {method_name}")

    # 2. 检查缓存
    print("\n1. Checking cache...")
    cached_data = check_cache(class_name)

    if cached_data:
        print("   [OK] Cache hit!")
        result = cached_data
    else:
        print("   [INFO] Cache miss, downloading...")

        # 3. 下载 HTML
        url = f"{BASE_URL}{class_name}.html"
        print(f"\n2. Downloading: {url}")
        html, status = fetch(url, f'data/cache/{class_name}.html')

        if status == 404:
            return {
                'success': False,
                'error': f'Class {class_name} not found (404)',
                'suggestion': f'Please check the class name or provide the correct URL'
            }

        if not html:
            return {
                'success': False,
                'error': f'Failed to download {class_name}'
            }

        print(f"   [OK] Downloaded (status: {status})")

        # 4. 解析 HTML
        print(f"\n3. Parsing HTML...")
        result = parse(f'data/cache/{class_name}.html')
        result['source_url'] = url

        print(f"   [OK] Parsed {len(result['methods'])} methods")

        # 5. 保存到缓存
        print(f"\n4. Saving to cache...")
        save_to_cache(class_name, result)
        print("   [OK] Cached")

    # 6. 提取方法（如果指定）
    if method_name and result['methods']:
        print(f"\n5. Extracting method: {method_name}")
        for method in result['methods']:
            if method['name'] == method_name:
                print(f"   [OK] Found method: {method_name}")
                result['focused_method'] = method
                break
        else:
            print(f"   [ERROR] Method not found: {method_name}")
            return {
                'success': False,
                'error': f'Method {method_name} not found in {class_name}'
            }

    result_dict = {
        'success': True,
        'data': result
    }

    # 7. 自动保存文档
    if save_doc:
        print(f"\n6. Saving documentation...")
        try:
            doc_path = generate_markdown(result_dict, output_dir)
            print(f"   [OK] Documentation saved: {doc_path}")
        except Exception as e:
            print(f"   [WARNING] Failed to save documentation: {e}")

    return result_dict

def format_result(result: dict, format_type: str = 'detailed') -> str:
    """格式化查询结果为 Markdown

    Args:
        result: 查询结果
        format_type: 格式类型 (detailed, compact, code-only)

    Returns:
        Markdown 文本
    """
    if not result.get('success'):
        return f"❌ 错误：{result.get('error', 'Unknown error')}"

    data = result['data']

    # 如果有聚焦的方法，只显示该方法
    if 'focused_method' in data:
        method = data['focused_method']
        return format_method(method, data['class_name'], format_type)

    # 否则显示所有方法概览
    lines = [
        f"# {data['class_name']}\n",
        f"**描述**: {data['description']}\n",
        f"**包含方法**: {len(data['methods'])} 个\n",
        "## 方法列表\n"
    ]

    for method in data['methods'][:10]:  # 只显示前 10 个
        lines.append(f"- **{method['signature']}**: {method['description'][:80]}...")

    if len(data['methods']) > 10:
        lines.append(f"\n... 还有 {len(data['methods']) - 10} 个方法")

    return '\n'.join(lines)

def format_method(method: dict, class_name: str, format_type: str) -> str:
    """格式化单个方法"""
    if format_type == 'code-only':
        if method['examples']:
            return '\n\n'.join([f"```javascript\n{ex}\n```" for ex in method['examples']])
        return "# 无代码示例"

    lines = [
        f"# {class_name}.{method['name']}\n",
        f"**签名**: `{method['signature']}`\n",
        f"**描述**: {method['description']}\n"
    ]

    if method['parameters']:
        lines.append("\n**参数**:")
        for param in method['parameters']:
            lines.append(f"- `{param['name']}` ({param['type']}): {param['description'][:100]}...")

    if method['returns']:
        lines.append(f"\n**返回值**: {method['returns']}")

    if method['examples'] and format_type == 'detailed':
        lines.append("\n**示例**:")
        for ex in method['examples']:
            lines.append(f"```javascript\n{ex}\n```")

    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python query.py <api_path> [method_name] [format] [options]")
        print("\nExamples:")
        print("  python query.py acApi.marker")
        print("  python query.py acApi.marker add")
        print("  python query.py acApi.marker add code-only")
        print("  python query.py acApi.marker --no-save")
        print("  python query.py acApi.marker --output-dir \"C:\\MyDocs\"")
        sys.exit(1)

    api_path = sys.argv[1]
    method_name = None
    format_type = 'detailed'
    save_doc = True
    output_dir = None

    # 解析参数
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--no-save':
            save_doc = False
            i += 1
        elif arg == '--output-dir':
            if i + 1 < len(sys.argv):
                output_dir = Path(sys.argv[i + 1])
                i += 2
            else:
                print("Error: --output-dir requires a path argument")
                sys.exit(1)
        elif not arg.startswith('--'):
            # 位置参数
            if method_name is None:
                method_name = arg
            elif format_type == 'detailed':
                format_type = arg
            i += 1
        else:
            print(f"Error: Unknown option {arg}")
            sys.exit(1)

    result = query_api(api_path, method_name, save_doc, output_dir)
    markdown = format_result(result, format_type)
    print("\n" + "="*50)
    print(markdown)
