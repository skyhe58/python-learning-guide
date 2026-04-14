#!/usr/bin/env python3
"""
数据清洗模块

模块: 05-crawler（爬虫）
知识点: 完整爬虫项目 - 数据清洗
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    由 crawler.py 调用

描述:
    对采集到的原始数据进行清洗：去重、格式校验、字段标准化。
"""

import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class DataCleaner:
    """数据清洗器。"""

    def clean(self, raw_data: list[dict]) -> list[dict]:
        """清洗数据：去重、校验、标准化。"""
        logger.info(f"开始清洗，原始数据 {len(raw_data)} 条")

        cleaned = []
        seen_ids: set[str] = set()

        for item in raw_data:
            # 1. 去重（按 ID）
            item_id = str(item.get("id", "")).strip()
            if not item_id or item_id in seen_ids:
                continue
            seen_ids.add(item_id)

            # 2. 校验必填字段
            title = item.get("title", "").strip()
            if not title:
                logger.warning(f"跳过无标题的记录: id={item_id}")
                continue

            # 3. 标准化字段
            cleaned_item = {
                "id": int(item_id) if item_id.isdigit() else item_id,
                "title": title,
                "author": item.get("author", "").strip() or "未知",
                "views": self._parse_views(item.get("views", "0")),
                "date": self._parse_date(item.get("date", "")),
                "tags": [t.strip() for t in item.get("tags", []) if t.strip()],
            }
            cleaned.append(cleaned_item)

        logger.info(f"清洗完成: {len(raw_data)} → {len(cleaned)} 条（去除 {len(raw_data) - len(cleaned)} 条）")
        return cleaned

    @staticmethod
    def _parse_views(views_str: str) -> int:
        """解析浏览量字符串为整数。"""
        digits = re.sub(r"[^\d]", "", str(views_str))
        return int(digits) if digits else 0

    @staticmethod
    def _parse_date(date_str: str) -> str:
        """解析并标准化日期格式。"""
        date_str = date_str.strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return ""


if __name__ == "__main__":
    # 单独测试清洗模块
    test_data = [
        {"id": "1", "title": "  测试文章  ", "author": "作者", "views": "1,234", "date": "2025-01-01", "tags": ["Python"]},
        {"id": "1", "title": "重复文章", "author": "作者", "views": "100", "date": "2025-01-01", "tags": []},
        {"id": "2", "title": "", "author": "", "views": "abc", "date": "invalid", "tags": []},
        {"id": "3", "title": "有效文章", "author": "", "views": "500", "date": "2025/06/15", "tags": ["测试"]},
    ]
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    cleaner = DataCleaner()
    result = cleaner.clean(test_data)
    for item in result:
        print(item)
