#!/usr/bin/env python3
"""
缓存管理器
管理 HTML 缓存和解析数据，支持过期检测
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import sys

# 默认路径
CACHE_DIR = Path('./data/cache')
PARSED_DIR = Path('./data/parsed')

def get_cache_key(url: str) -> str:
    """生成缓存键"""
    return hashlib.md5(url.encode()).hexdigest()

def check_cache(class_name: str, include_markdown: bool = True) -> dict | None:
    """检查缓存是否存在且未过期

    Args:
        class_name: 类名
        include_markdown: 是否检查 Markdown 字段（默认 True）

    Returns:
        缓存数据，如果 include_markdown=True 但缓存中没有 markdown 字段，
        则自动生成并更新缓存
    """
    cache_file = PARSED_DIR / f"{class_name}.json"

    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text(encoding='utf-8'))
        crawled_at = datetime.fromisoformat(data['crawled_at'])

        if datetime.now() - crawled_at > timedelta(days=7):
            return None

        # 向后兼容：如果没有 markdown 字段，自动生成
        if include_markdown and 'markdown' not in data:
            print("   [INFO] Backfilling markdown cache...")
            update_markdown_cache(class_name, data)
            # 重新读取更新后的缓存
            data = json.loads(cache_file.read_text(encoding='utf-8'))

        return data
    except Exception as e:
        print(f"Error reading cache: {e}", file=sys.stderr)
        return None

def save_to_cache(class_name: str, data: dict) -> None:
    """保存到缓存（包含 Markdown）"""
    from scripts.doc_generator import generate_all_markdowns

    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = PARSED_DIR / f"{class_name}.json"

    data['crawled_at'] = datetime.now().isoformat()

    # 生成 Markdown 缓存
    data['markdown'] = generate_all_markdowns(data)
    data['cache_version'] = '2.0'

    cache_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def update_markdown_cache(class_name: str, data: dict) -> None:
    """为现有缓存生成并添加 Markdown

    Args:
        class_name: 类名
        data: 解析后的 JSON 数据（包含 methods）
    """
    from scripts.doc_generator import generate_all_markdowns

    cache_file = PARSED_DIR / f"{class_name}.json"

    markdowns = generate_all_markdowns(data)
    data['markdown'] = markdowns
    data['cache_version'] = '2.0'

    cache_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )

def get_html_cache(url: str) -> str | None:
    """获取缓存的 HTML"""
    cache_key = get_cache_key(url)
    cache_file = CACHE_DIR / f"{cache_key}.html"

    if cache_file.exists():
        return cache_file.read_text(encoding='utf-8')
    return None

def save_html_cache(url: str, html: str) -> None:
    """保存 HTML 到缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_key = get_cache_key(url)
    cache_file = CACHE_DIR / f"{cache_key}.html"
    cache_file.write_text(html, encoding='utf-8')

def list_cached() -> list[str]:
    """列出所有已缓存的类"""
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    return [f.stem for f in PARSED_DIR.glob('*.json')]

def clear_cache(class_name: str = None) -> None:
    """清理缓存

    Args:
        class_name: 指定类名，None 表示清理所有
    """
    if class_name:
        # 清理指定类的缓存
        cache_file = PARSED_DIR / f"{class_name}.json"
        if cache_file.exists():
            cache_file.unlink()
            print(f"Cleared cache for {class_name}")
    else:
        # 清理所有缓存
        for f in PARSED_DIR.glob('*.json'):
            f.unlink()
        for f in CACHE_DIR.glob('*.html'):
            f.unlink()
        print("Cleared all cache")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cache_manager.py --check <class_name>")
        print("  python cache_manager.py --list")
        print("  python cache_manager.py --clear [class_name]")
        sys.exit(1)

    command = sys.argv[1]

    if command == '--check':
        if len(sys.argv) < 3:
            print("Error: class_name required for --check")
            sys.exit(1)
        result = check_cache(sys.argv[2])
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("Cache miss or expired")
    elif command == '--list':
        cached = list_cached()
        print(f"Cached classes ({len(cached)}):")
        for name in cached:
            print(f"  - {name}")
    elif command == '--clear':
        class_name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_cache(class_name)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
