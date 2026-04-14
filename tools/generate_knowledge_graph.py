#!/usr/bin/env python3
"""
知识图谱生成工具 — 使用 pyecharts 生成可交互的知识图谱 HTML

模块: tools
Python 版本: >= 3.9
最后验证: 2025-07-14

运行方式:
    python tools/generate_knowledge_graph.py
    python tools/generate_knowledge_graph.py --dir ./
    python tools/generate_knowledge_graph.py --output my_graph.html

描述:
    扫描项目目录结构和 README.md 文件中的引用关系，使用 pyecharts
    生成可交互的知识图谱 HTML 文件。图谱中以不同颜色区分学习阶段，
    以有向边表示模块间的前置依赖关系，支持节点点击跳转。
    本工具为通用型，可复用于任意 Markdown 项目的目录结构可视化。
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    from pyecharts import options as opts
    from pyecharts.charts import Graph
except ImportError:
    print(
        "错误: 缺少 pyecharts 依赖。请先安装:\n"
        "  pip install pyecharts>=2.0.0\n"
        "或:\n"
        "  pip install -r tools/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


# 学习阶段颜色配置
# 蓝色: 第一阶段, 绿色: 第二阶段, 橙色: 第三阶段, 红色: 第四阶段, 紫色: 贯穿全程
STAGE_COLORS = {
    "stage1": "#e1f5fe",  # 蓝色 — 第一阶段（01-python-basics）
    "stage2": "#e8f5e9",  # 绿色 — 第二阶段（02-common-features, 03-mini-tools）
    "stage3": "#fff3e0",  # 橙色 — 第三阶段（04-frameworks）
    "stage4": "#fce4ec",  # 红色 — 第四阶段（05-crawler, 06-ai-apps, 07-yolo-cv）
    "cross":  "#f3e5f5",  # 紫色 — 贯穿全程（08-interview）
    "other":  "#f5f5f5",  # 灰色 — 其他（tools, templates 等）
}

# 阶段边框颜色（用于增强视觉区分）
STAGE_BORDER_COLORS = {
    "stage1": "#0288d1",
    "stage2": "#388e3c",
    "stage3": "#f57c00",
    "stage4": "#c62828",
    "cross":  "#7b1fa2",
    "other":  "#9e9e9e",
}

# 模块到学习阶段的映射
MODULE_STAGE_MAP = {
    "01-python-basics": "stage1",
    "02-common-features": "stage2",
    "03-mini-tools": "stage2",
    "04-frameworks": "stage3",
    "05-crawler": "stage4",
    "06-ai-apps": "stage4",
    "07-yolo-cv": "stage4",
    "08-interview": "cross",
}

# 模块间的前置依赖关系（有向边: 源 → 目标，表示"源"是"目标"的前置条件）
MODULE_DEPENDENCIES = [
    ("01-python-basics", "02-common-features"),
    ("01-python-basics", "03-mini-tools"),
    ("02-common-features", "04-frameworks"),
    ("03-mini-tools", "04-frameworks"),
    ("04-frameworks", "05-crawler"),
    ("04-frameworks", "06-ai-apps"),
    ("04-frameworks", "07-yolo-cv"),
]

# 阶段中文名称
STAGE_NAMES = {
    "stage1": "第一阶段：必修基础",
    "stage2": "第二阶段：核心应用",
    "stage3": "第三阶段：架构提升",
    "stage4": "第四阶段：进阶应用",
    "cross":  "贯穿全程",
    "other":  "辅助工具",
}


def get_stage(dir_name: str) -> str:
    """根据目录名获取学习阶段"""
    return MODULE_STAGE_MAP.get(dir_name, "other")


def scan_modules(project_dir: Path) -> list[dict]:
    """
    扫描项目目录，收集模块信息。

    参数:
        project_dir: 项目根目录路径

    返回:
        模块信息列表，每个元素包含 name, label, stage, path, subtopics
    """
    modules = []

    try:
        entries = sorted(project_dir.iterdir(), key=lambda e: e.name)
    except PermissionError:
        return modules

    for entry in entries:
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name in ("__pycache__", "venv", ".venv"):
            continue

        # 读取 README.md 获取模块标题
        label = entry.name
        readme_path = entry / "README.md"
        if readme_path.exists():
            try:
                content = readme_path.read_text(encoding="utf-8")
                # 提取第一个 # 标题
                match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if match:
                    label = match.group(1).strip()
            except (OSError, UnicodeDecodeError):
                pass

        stage = get_stage(entry.name)

        # 收集子知识点
        subtopics = []
        for sub in sorted(entry.iterdir(), key=lambda e: e.name):
            if sub.is_dir() and not sub.name.startswith(".") and sub.name != "__pycache__":
                sub_label = sub.name
                sub_readme = sub / "README.md"
                if sub_readme.exists():
                    try:
                        sub_content = sub_readme.read_text(encoding="utf-8")
                        sub_match = re.search(r"^#\s+(.+)$", sub_content, re.MULTILINE)
                        if sub_match:
                            sub_label = sub_match.group(1).strip()
                    except (OSError, UnicodeDecodeError):
                        pass
                subtopics.append({
                    "name": sub.name,
                    "label": sub_label,
                    "path": str(sub.relative_to(project_dir)),
                })

        modules.append({
            "name": entry.name,
            "label": label,
            "stage": stage,
            "path": str(entry.relative_to(project_dir)),
            "subtopics": subtopics,
        })

    return modules


def parse_references(project_dir: Path) -> list[tuple[str, str]]:
    """
    解析 README.md 文件中的 Markdown 链接引用关系。

    参数:
        project_dir: 项目根目录路径

    返回:
        引用关系列表，每个元素为 (源模块名, 目标模块名) 元组
    """
    references = []
    link_pattern = re.compile(r"\[.*?\]\(([^)]+)\)")

    for readme_path in project_dir.rglob("README.md"):
        try:
            content = readme_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        source_dir = readme_path.parent
        if source_dir == project_dir:
            continue

        # 获取源模块名（取顶层模块目录名）
        rel = source_dir.relative_to(project_dir)
        source_module = rel.parts[0] if rel.parts else None
        if not source_module:
            continue

        # 查找所有 Markdown 链接
        for match in link_pattern.finditer(content):
            link_target = match.group(1)
            # 跳过外部链接和锚点
            if link_target.startswith(("http://", "https://", "#", "mailto:")):
                continue

            # 解析相对路径，提取目标模块
            try:
                target_path = (source_dir / link_target).resolve()
                target_rel = target_path.relative_to(project_dir.resolve())
                target_module = target_rel.parts[0] if target_rel.parts else None
                if target_module and target_module != source_module:
                    ref = (source_module, target_module)
                    if ref not in references:
                        references.append(ref)
            except (ValueError, OSError):
                continue

    return references


def build_graph(modules: list[dict], references: list[tuple[str, str]]) -> Graph:
    """
    构建 pyecharts Graph 图表。

    参数:
        modules: 模块信息列表
        references: 引用关系列表

    返回:
        pyecharts Graph 对象
    """
    nodes = []
    links = []
    categories = []

    # 创建分类（学习阶段）
    for stage_key, stage_name in STAGE_NAMES.items():
        categories.append(opts.GraphCategory(
            name=stage_name,
            symbol="circle",
        ))

    stage_keys = list(STAGE_NAMES.keys())

    # 创建模块节点
    for module in modules:
        stage = module["stage"]
        color = STAGE_COLORS.get(stage, STAGE_COLORS["other"])
        border_color = STAGE_BORDER_COLORS.get(stage, STAGE_BORDER_COLORS["other"])
        category_idx = stage_keys.index(stage) if stage in stage_keys else len(stage_keys) - 1

        nodes.append(opts.GraphNode(
            name=module["name"],
            value=module["label"],
            symbol_size=40,
            category=category_idx,
            itemstyle_opts=opts.ItemStyleOpts(
                color=color,
                border_color=border_color,
                border_width=2,
            ),
            label_opts=opts.LabelOpts(
                is_show=True,
                font_size=11,
                formatter=module["label"],
            ),
        ))

        # 创建子知识点节点
        for sub in module["subtopics"]:
            sub_node_name = f"{module['name']}/{sub['name']}"
            nodes.append(opts.GraphNode(
                name=sub_node_name,
                value=sub["label"],
                symbol_size=18,
                category=category_idx,
                itemstyle_opts=opts.ItemStyleOpts(
                    color=color,
                    border_color=border_color,
                    border_width=1,
                ),
                label_opts=opts.LabelOpts(
                    is_show=True,
                    font_size=9,
                    formatter=sub["name"],
                ),
            ))

            # 模块到子知识点的边
            links.append(opts.GraphLink(
                source=module["name"],
                target=sub_node_name,
                linestyle_opts=opts.LineStyleOpts(
                    color="#cccccc",
                    width=1,
                    opacity=0.5,
                ),
            ))

    # 创建模块间依赖边（有向边）
    module_names = {m["name"] for m in modules}
    for source, target in MODULE_DEPENDENCIES:
        if source in module_names and target in module_names:
            links.append(opts.GraphLink(
                source=source,
                target=target,
                linestyle_opts=opts.LineStyleOpts(
                    color="#666666",
                    width=2,
                    curve=0.2,
                ),
                label_opts=opts.LabelOpts(
                    is_show=False,
                ),
            ))

    # 添加文档引用关系边
    for source, target in references:
        if source in module_names and target in module_names:
            # 避免与依赖边重复
            dep_pair = (source, target)
            if dep_pair not in MODULE_DEPENDENCIES:
                links.append(opts.GraphLink(
                    source=source,
                    target=target,
                    linestyle_opts=opts.LineStyleOpts(
                        color="#aaaaaa",
                        width=1,
                        type_="dashed",
                        opacity=0.6,
                    ),
                ))

    # 构建图表
    graph = (
        Graph(
            init_opts=opts.InitOpts(
                width="100%",
                height="800px",
                page_title="Python 学习知识库 — 知识图谱",
            )
        )
        .add(
            series_name="",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="force",
            is_roam=True,
            is_draggable=True,
            is_focusnode=True,
            repulsion=300,
            gravity=0.05,
            edge_length=[80, 200],
            edge_symbol=["", "arrow"],
            edge_symbol_size=[0, 8],
            label_opts=opts.LabelOpts(
                is_show=True,
                position="bottom",
                font_size=10,
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Python 学习知识库 — 知识图谱",
                subtitle="节点颜色区分学习阶段，有向边表示前置依赖关系",
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="left",
                pos_top="middle",
            ),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="保存为图片"),
                    restore=opts.ToolBoxFeatureRestoreOpts(title="还原"),
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="{b}: {c}",
            ),
        )
    )

    return graph


def get_default_dir() -> Path:
    """获取默认扫描目录（tools/ 的父目录，即项目根目录）"""
    return Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="使用 pyecharts 生成可交互的知识图谱 HTML 文件。"
        "本工具为通用型，可复用于任意 Markdown 项目。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 生成知识图谱（默认扫描项目根目录）
  python tools/generate_knowledge_graph.py

  # 指定扫描目录
  python tools/generate_knowledge_graph.py --dir ./01-python-basics

  # 指定输出文件
  python tools/generate_knowledge_graph.py --output my_graph.html

颜色说明:
  蓝色 (#e1f5fe) — 第一阶段：必修基础（01-python-basics）
  绿色 (#e8f5e9) — 第二阶段：核心应用（02-common-features, 03-mini-tools）
  橙色 (#fff3e0) — 第三阶段：架构提升（04-frameworks）
  红色 (#fce4ec) — 第四阶段：进阶应用（05-crawler, 06-ai-apps, 07-yolo-cv）
  紫色 (#f3e5f5) — 贯穿全程（08-interview）
        """,
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="要扫描的目录路径（默认: 项目根目录，即 tools/ 的父目录）",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出 HTML 文件路径（默认: 项目根目录下的 knowledge_graph.html）",
    )
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 确定扫描目录
    if args.dir:
        scan_dir = Path(args.dir).resolve()
    else:
        scan_dir = get_default_dir()

    if not scan_dir.is_dir():
        print(f"错误: 目录不存在 — {scan_dir}", file=sys.stderr)
        sys.exit(1)

    # 确定输出路径
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = scan_dir / "knowledge_graph.html"

    # 扫描模块信息
    print(f"正在扫描目录: {scan_dir}")
    modules = scan_modules(scan_dir)
    print(f"发现 {len(modules)} 个模块")

    # 解析文档引用关系
    references = parse_references(scan_dir)
    print(f"发现 {len(references)} 条文档引用关系")

    # 构建并渲染图表
    graph = build_graph(modules, references)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph.render(str(output_path))
    print(f"知识图谱已生成: {output_path}")


if __name__ == "__main__":
    main()
