#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes Enterprise Knowledge 配图生成"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

plt.rcParams["font.family"] = ["Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(WORK_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)
BG = "#0a1420"

# ========== 图 1: 8 Memory Providers 对比 ==========
def draw_providers():
    fig, ax = plt.subplots(figsize=(14, 6.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    providers = [
        # (name, tagline, color, best_for, data_storage)
        ("Hindsight", "Knowledge Graph", "#f97316", "知识图谱推理", "Cloud / Local Embedded PG"),
        ("RetainDB", "Hybrid Search", "#3b82f6", "结构化知识库", "Self-hosted"),
        ("ByteRover", "Auto Curation", "#22c55e", "自动知识提炼", "Self-hosted"),
        ("OpenViking", "Tiered Retrieval", "#06b6d4", "分层上下文", "Self-hosted (AGPL)"),
        ("Mem0", "Auto Extraction", "#a855f7", "零维护自动抽取", "Mem0 Cloud"),
        ("Honcho", "User Modeling", "#ec4899", "跨会话用户画像", "Cloud / Self-hosted"),
        ("Holographic", "Local SQLite", "#f59e0b", "纯本地轻量", "Local SQLite"),
        ("Supermemory", "Semantic Recall", "#14b8a6", "语义召回", "—"),
    ]

    cols = 4
    rows = 2
    card_w = 3.0
    card_h = 2.6
    gap_x = 0.17
    gap_y = 0.2

    for i, (name, tagline, color, best, storage) in enumerate(providers):
        col = i % cols
        row = i // cols
        x = 0.3 + col * (card_w + gap_x)
        y = 3.6 - row * (card_h + gap_y)

        # 卡片
        card = FancyBboxPatch((x, y), card_w, card_h, boxstyle="round,pad=0.1",
                               fc="#1e293b", ec=color, lw=1.5)
        ax.add_patch(card)
        # 顶部色带
        top = FancyBboxPatch((x + 0.05, y + card_h - 0.42), card_w - 0.1, 0.37,
                               boxstyle="round,pad=0.02",
                               fc=color, ec="none")
        ax.add_patch(top)

        ax.text(x + card_w/2, y + card_h - 0.23, name,
                ha="center", va="center", fontsize=9, fontweight="bold", color="white")
        ax.text(x + card_w/2, y + card_h - 0.8, tagline,
                ha="center", va="center", fontsize=7.5, color=color)
        ax.text(x + 0.15, y + card_h - 1.25, "Best for:",
                ha="left", va="center", fontsize=7, color="#64748b")
        ax.text(x + 0.15, y + card_h - 1.5, best,
                ha="left", va="center", fontsize=7.5, color="#cbd5e1")
        ax.text(x + 0.15, y + card_h - 1.85, "Storage:",
                ha="left", va="center", fontsize=7, color="#64748b")
        ax.text(x + 0.15, y + card_h - 2.1, storage,
                ha="left", va="center", fontsize=7.5, color="#94a3b8")

    ax.text(7, 6.2, "Hermes Agent — 8 Memory Providers",
            ha="center", va="center", fontsize=15, fontweight="bold", color="white")
    ax.text(7, 5.85, "企业知识库选谁？一张卡看清每个 provider 的定位",
            ha="center", va="center", fontsize=9.5, color="#94a3b8")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "memory_providers.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ memory_providers.png")


# ========== 图 2: 知识摄取管道 ==========
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(14, 4.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    steps = [
        ("文档源", "API Docs\nCode Repos\nWiki\n产品手册", "#f97316"),
        ("摄取", "hermes tools\nadd_resource\nbrowse_url", "#3b82f6"),
        ("自动抽取", "实体识别\n关系提取\n事实去重", "#22c55e"),
        ("存储", "Hindsight KG\nOpenViking\nSQLite / PG", "#a855f7"),
        ("检索", "语义召回\n图遍历\n分层读取", "#06b6d4"),
        ("对外服务", "API Server\nMCP / A2A\nGateway", "#ec4899"),
    ]

    for i, (title, desc, color) in enumerate(steps):
        x = 0.35 + i * 2.2
        # 卡片
        card = FancyBboxPatch((x, 1.0), 2.0, 2.8, boxstyle="round,pad=0.12",
                               fc="#1e293b", ec=color, lw=2)
        ax.add_patch(card)
        # 顶部色带
        top = FancyBboxPatch((x + 0.05, 3.25), 1.9, 0.45, boxstyle="round,pad=0.02",
                               fc=color, ec="none")
        ax.add_patch(top)
        ax.text(x + 1.0, 3.47, title,
                ha="center", va="center", fontsize=9, fontweight="bold", color="white")
        ax.text(x + 1.0, 2.3, desc,
                ha="center", va="center", fontsize=7.5, color="#cbd5e1", linespacing=1.35)
        # 底部步骤号
        ax.text(x + 1.0, 1.3, f"0{i+1}",
                ha="center", va="center", fontsize=7, color="#475569")

        # 箭头
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 2.15, 2.4), xytext=(x + 2.0, 2.4),
                        arrowprops=dict(arrowstyle="-|>", color="#475569", lw=2))

    ax.text(7, 4.55, "Hermes 企业知识摄取 → 存储 → 服务 Pipeline",
            ha="center", va="center", fontsize=14, fontweight="bold", color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "pipeline.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ pipeline.png")


# ========== 图 3: 对外知识服务架构 ==========
def draw_services():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # 底层：知识库（Hindsight KG + OpenViking + ...）
    kb_box = FancyBboxPatch((1.0, 0.3), 10.0, 1.3, boxstyle="round,pad=0.1",
                             fc="#1e293b", ec="#f97316", lw=2)
    ax.add_patch(kb_box)
    ax.text(6.0, 1.15, "Hermes Memory Providers — 企业知识库",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#f97316")
    ax.text(6.0, 0.65, "Hindsight Knowledge Graph  |  OpenViking Tiered Store  |  RetainDB  |  Honcho  |  ByteRover",
            ha="center", va="center", fontsize=8.5, color="#94a3b8")

    # 中间：Hermes Agent + Gateway
    gw_box = FancyBboxPatch((2.0, 2.4), 8.0, 1.3, boxstyle="round,pad=0.1",
                             fc="#1e293b", ec="#3b82f6", lw=2)
    ax.add_patch(gw_box)
    ax.text(6.0, 3.15, "Hermes Agent — Retrieval + Reasoning + Caching",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#3b82f6")
    ax.text(6.0, 2.65, "hindsight_recall / viking_search / honcho_search → LLM 综合 → 可信答案",
            ha="center", va="center", fontsize=8, color="#94a3b8")

    # 连接箭头（知识库 → Agent）
    ax.annotate("", xy=(6.0, 2.3), xytext=(6.0, 1.6),
                arrowprops=dict(arrowstyle="-|>", color="#3b82f6", lw=2))
    ax.annotate("", xy=(6.0, 1.6), xytext=(6.0, 2.3),
                arrowprops=dict(arrowstyle="-|>", color="#3b82f6", lw=2))
    ax.text(6.4, 1.95, "读 / 写", ha="left", va="center", fontsize=7.5, color="#3b82f6")

    # 顶层：四种对外暴露
    services = [
        ("API Server", "OpenAI-compatible\n/v1/chat/completions", "#22c55e", 1.5),
        ("MCP Server", "stdio / SSE\nexpose as tool", "#06b6d4", 4.5),
        ("A2A Gateway", "HTTP + JSON-RPC\npeer-to-peer", "#a855f7", 7.5),
        ("Messaging", "WeCom / Feishu\nTelegram Bot", "#ec4899", 10.5),
    ]

    for name, desc, color, cx in services:
        svc = FancyBboxPatch((cx - 1.3, 5.2), 2.6, 1.3, boxstyle="round,pad=0.1",
                              fc="#1e293b", ec=color, lw=2)
        ax.add_patch(svc)
        ax.text(cx, 5.95, name, ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)
        ax.text(cx, 5.45, desc, ha="center", va="center",
                fontsize=7, color="#cbd5e1", linespacing=1.2)
        # 连接到 Agent
        ax.annotate("", xy=(cx, 5.1), xytext=(6.0, 3.7),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5,
                                    connectionstyle="arc3,rad=-0.1"))

    # 员工图标（右侧终端用户）
    ax.text(11.0, 4.2, "End Users", ha="center", va="center", fontsize=9, color="#f97316",
            bbox=dict(boxstyle="round,pad=0.3", fc="#1e293b", ec="#f97316", lw=1.5))

    ax.text(6, 6.7, "企业知识服务 — 一条知识，四种入口",
            ha="center", va="center", fontsize=13, fontweight="bold", color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "services.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ services.png")


# ========== 图 4: Hindsight 知识图谱配置速查 ==========
def draw_hindsight_config():
    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    # 三列：安装 → 配置 → 运行时三工具
    col_xs = [0.3, 4.6, 8.9]
    col_titles = [
        ("安装", "#f97316"),
        ("hindsight/config.json", "#3b82f6"),
        ("三个核心工具", "#22c55e"),
    ]

    # 安装列
    install_box = FancyBboxPatch((col_xs[0], 0.4), 4.1, 4.6, boxstyle="round,pad=0.1",
                                  fc="#1e293b", ec="#f97316", lw=1.5)
    ax.add_patch(install_box)
    ax.text(col_xs[0] + 2.05, 4.75, "安装 & 启用", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#f97316")

    install_steps = [
        "hermes plugins install hindsight",
        "hermes memory setup  # pick hindsight",
        "hermes config set memory.provider hindsight",
        "echo HINDSIGHT_API_KEY=... >> .env",
        "# local mode:",
        "hermes config set memory.hindsight.mode local",
    ]
    for i, step in enumerate(install_steps):
        ax.text(col_xs[0] + 0.25, 4.25 - i * 0.47, step,
                ha="left", va="center", fontsize=8,
                color="#cbd5e1", fontfamily="Consolas,Menlo,monospace")

    # 配置列
    cfg_box = FancyBboxPatch((col_xs[1], 0.4), 4.1, 4.6, boxstyle="round,pad=0.1",
                               fc="#1e293b", ec="#3b82f6", lw=1.5)
    ax.add_patch(cfg_box)
    ax.text(col_xs[1] + 2.05, 4.75, "config.json 关键字段", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#3b82f6")

    cfg_rows = [
        ("mode", "cloud / local", "#94a3b8"),
        ("bank_id", "my-project-kg", "#94a3b8"),
        ("recall_budget", "low / mid / high", "#94a3b8"),
        ("memory_mode", "hybrid / context / tools", "#94a3b8"),
        ("auto_retain", "true  (自动存对话)", "#94a3b8"),
        ("auto_recall", "true  (每轮预取)", "#94a3b8"),
    ]
    for i, (k, v, _) in enumerate(cfg_rows):
        y = 4.2 - i * 0.57
        ax.text(col_xs[1] + 0.25, y, k, ha="left", va="center",
                fontsize=8, fontweight="bold", color="#3b82f6",
                fontfamily="Consolas,Menlo,monospace")
        ax.text(col_xs[1] + 0.25, y - 0.22, v, ha="left", va="center",
                fontsize=7.5, color="#64748b")

    # 三工具列
    tool_box = FancyBboxPatch((col_xs[2], 0.4), 3.8, 4.6, boxstyle="round,pad=0.1",
                                fc="#1e293b", ec="#22c55e", lw=1.5)
    ax.add_patch(tool_box)
    ax.text(col_xs[2] + 1.9, 4.75, "Agent 可调用工具", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#22c55e")

    tools = [
        ("hindsight_retain", "带实体提取存知识", "#22c55e"),
        ("hindsight_recall", "多策略检索召回", "#22c55e"),
        ("hindsight_reflect", "跨记忆综合推理", "#22c55e"),
    ]
    for i, (name, desc, color) in enumerate(tools):
        y = 4.3 - i * 1.2
        tb = FancyBboxPatch((col_xs[2] + 0.15, y - 0.55), 3.5, 0.95,
                              boxstyle="round,pad=0.05",
                              fc="#0f172a", ec=color, lw=1.2)
        ax.add_patch(tb)
        ax.text(col_xs[2] + 1.9, y - 0.25, name,
                ha="center", va="center", fontsize=8.5, fontweight="bold", color=color)
        ax.text(col_xs[2] + 1.9, y - 0.6, desc,
                ha="center", va="center", fontsize=7, color="#94a3b8")

    ax.text(6.5, 5.25, "Hindsight 知识图谱 — 从安装到推理三卡速查",
            ha="center", va="center", fontsize=13, fontweight="bold", color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "hindsight_cfg.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ hindsight_cfg.png")


if __name__ == "__main__":
    draw_providers()
    draw_pipeline()
    draw_services()
    draw_hindsight_config()
    print(f"\n全部生成于 {ASSETS}")
