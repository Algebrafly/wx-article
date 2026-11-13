#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WeKnora 配图生成"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

plt.rcParams["font.family"] = ["Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(WORK_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)
BG = "#0f172a"
BLUE = "#2563eb"
TEAL = "#06b6d4"
GREEN = "#22c55e"
AMBER = "#f59e0b"
PINK = "#ec4899"
GRAY = "#94a3b8"


# ========== 图 1: 三大核心能力 ==========
def draw_core():
    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    cores = [
        ("RAG", "Retrieval Augmented\nGeneration", BLUE,
         "多模态预处理\n向量索引 + BM25 混合召回\n上下文检索增强生成"),
        ("ReAct Agent", "Reason + Act\nAutonomous", TEAL,
         "自主推理 + 工具调用\nSkill Sandbox 沙箱执行\n会话级持久环境"),
        ("Auto-Wiki", "Self-maintaining\nKnowledge Wiki", GREEN,
         "自动生成 Markdown 页面\n五种关系知识图谱\n可编辑 / Diff / 回滚"),
    ]

    col_w = 3.8
    gap = 0.25
    total = col_w * 3 + gap * 2
    start = (13 - total) / 2

    for i, (title, subtitle, color, desc) in enumerate(cores):
        x = start + i * (col_w + gap)
        y = 0.6
        w = col_w
        h = 4.4

        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                              fc="#1e293b", ec=color, lw=2.5)
        ax.add_patch(box)
        # 顶部高光条
        top = FancyBboxPatch((x + 0.08, y + h - 0.52), w - 0.16, 0.42,
                              boxstyle="round,pad=0.02",
                              fc=color, ec="none")
        ax.add_patch(top)

        ax.text(x + w/2, y + h - 0.31, title,
                ha="center", va="center", fontsize=12, fontweight="bold", color="white")
        ax.text(x + w/2, y + h - 0.9, subtitle,
                ha="center", va="center", fontsize=8, color=color, linespacing=1.25)

        # 分割线
        ax.plot([x + 0.2, x + w - 0.2], [y + h - 1.2, y + h - 1.2],
                color=color, lw=0.7, ls=":")

        ax.text(x + w/2, y + h - 2.4, desc,
                ha="center", va="center", fontsize=8, color="#cbd5e1", linespacing=1.5)

        # 标签
        ax.text(x + w/2, y + 0.3, f"CORE {i+1}",
                ha="center", va="center", fontsize=7, color="#475569", fontweight="bold")

    ax.text(6.5, 5.1, "WeKnora · Three Core Capabilities",
            ha="center", va="center", fontsize=14, fontweight="bold", color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "core.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ core.png")


# ========== 图 2: 组件技术栈 ==========
def draw_stack():
    fig, ax = plt.subplots(figsize=(12, 7.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis("off")

    layers = [
        ("Frontend", "Vue 3", "#2563eb", 6.5),
        ("Backend API", "Go  +  Gin", "#06b6d4", 5.4),
        ("DocReader", "Python  Parser", "#22c55e", 4.3),
        ("DB / Vector", "ParadeDB  (PostgreSQL + pgvector + BM25)", "#7c3aed", 3.2),
        ("Object Storage", "Local / MinIO / S3 / OSS", "#f59e0b", 2.1),
        ("LLM Layer", "20+ Providers  (OpenAI / Anthropic / Tencent Hunyuan / ...)", "#ec4899", 1.0),
    ]

    for name, tech, color, y in layers:
        box = FancyBboxPatch((0.6, y - 0.35), 10.8, 0.7, boxstyle="round,pad=0.08",
                              fc="#1e293b", ec=color, lw=1.8)
        ax.add_patch(box)
        # 左侧色点
        ax.add_patch(plt.Circle((1.1, y), 0.14, color=color, zorder=5))
        ax.text(1.35, y, name, ha="left", va="center",
                fontsize=10, fontweight="bold", color=color)
        ax.text(11.45, y, tech, ha="right", va="center",
                fontsize=8.5, color="#cbd5e1", fontfamily="Consolas,Menlo,monospace")

    ax.text(6, 7.2, "WeKnora · Technology Stack",
            ha="center", va="center", fontsize=14, fontweight="bold", color="white")
    ax.text(6, 6.85, "Open-source MIT · Tencent WeChat Team",
            ha="center", va="center", fontsize=9, color="#94a3b8")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "stack.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ stack.png")


# ========== 图 3: Wiki 模式 vs 传统 RAG ==========
def draw_compare():
    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    # Left: Traditional RAG
    lx = 0.5
    box_l = FancyBboxPatch((lx, 0.5), 5.8, 4.5, boxstyle="round,pad=0.1",
                            fc="#1e293b", ec="#64748b", lw=1.5)
    ax.add_patch(box_l)
    ax.text(lx + 2.9, 4.85, "Traditional RAG", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#64748b")

    # 左侧流程
    left_steps = [
        ("Upload Doc A", "#64748b", 3.9),
        ("Split into 6 chunks", "#64748b", 3.2),
        ("Embed → Vector DB", "#64748b", 2.5),
        ("Query: keyword search", "#64748b", 1.8),
        ("Return 3 chunks", "#ef4444", 1.1),
    ]
    for t, c, y in left_steps:
        ax.text(lx + 0.4, y, t, ha="left", va="center",
                fontsize=8.5, color=c, fontfamily="Consolas,Menlo,monospace")

    # 中间 VS
    ax.text(6.5, 3.0, "VS", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#f97316")

    # Right: WeKnora Wiki
    rx = 6.7
    box_r = FancyBboxPatch((rx, 0.5), 5.8, 4.5, boxstyle="round,pad=0.1",
                            fc="#1e293b", ec="#22c55e", lw=1.5)
    ax.add_patch(box_r)
    ax.text(rx + 2.9, 4.85, "WeKnora Auto-Wiki", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#22c55e")

    right_steps = [
        ("Upload Doc A", "#22c55e", 3.9),
        ("Agent reads full doc", "#22c55e", 3.2),
        ("Writes Markdown pages", "#22c55e", 2.5),
        ("Links + KG (5 relations)", "#22c55e", 1.8),
        ("Readable, editable, rollback", "#22c55e", 1.1),
    ]
    for t, c, y in right_steps:
        ax.text(rx + 0.4, y, t, ha="left", va="center",
                fontsize=8.5, color=c, fontfamily="Consolas,Menlo,monospace")

    # 下方说明
    ax.text(6.5, 0.3, "Chunks are for machines · Pages are for humans",
            ha="center", va="center", fontsize=9, color="#94a3b8",
            fontstyle="italic")

    ax.text(6.5, 5.25, "Traditional RAG vs WeKnora Wiki Mode",
            ha="center", va="center", fontsize=13, fontweight="bold", color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "compare.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ compare.png")


# ========== 图 4: 沙箱执行流程 ==========
def draw_sandbox():
    fig, ax = plt.subplots(figsize=(14, 4.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    steps = [
        ("User Query", "\"Write result to Docx\"", "#f97316"),
        ("ReAct Agent", "Plan · Search · Think · Act", "#2563eb"),
        ("Skill Sandbox", "Docker / E2B / Cube\nSession-persistent env", "#06b6d4"),
        ("Tool Execution", "Run JS script · Install libs", "#22c55e"),
        ("Artifact Delivery", "Docx file with cover", "#7c3aed"),
    ]

    step_w = 2.35
    gap = 0.3
    total = step_w * 5 + gap * 4
    start = (14 - total) / 2

    for i, (title, desc, color) in enumerate(steps):
        x = start + i * (step_w + gap)
        # 节点圆
        circle = plt.Circle((x + step_w/2, 3.0), 0.35, color=color, zorder=5)
        ax.add_patch(circle)
        ax.text(x + step_w/2, 3.0, f"0{i+1}",
                ha="center", va="center", fontsize=8, fontweight="bold",
                color=BG, zorder=6)

        # 标题
        ax.text(x + step_w/2, 2.2, title,
                ha="center", va="center", fontsize=9.5, fontweight="bold",
                color=color)
        # 描述
        ax.text(x + step_w/2, 1.5, desc,
                ha="center", va="center", fontsize=7.5, color="#cbd5e1", linespacing=1.3)

        # 箭头
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + step_w + gap/2, 3.0),
                        xytext=(x + step_w, 3.0),
                        arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2))

    # 最下方：沙箱后端
    ax.text(7, 0.7, "Sandbox Runtimes : Docker  (default)  ·  E2B  ·  Cube  ·  Local host-process (removed in v0.8.0)",
            ha="center", va="center", fontsize=8.5, color="#f97316",
            bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec="#f97316", lw=1.2))

    ax.text(7, 4.25, "WeKnora Skill Sandbox Runtime",
            ha="center", va="center", fontsize=13, fontweight="bold", color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "sandbox.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ sandbox.png")


if __name__ == "__main__":
    draw_core()
    draw_stack()
    draw_compare()
    draw_sandbox()
    print(f"\nAll assets in {ASSETS}")
