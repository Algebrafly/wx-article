#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes A2A + SDLC 配图生成"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# 字体配置
plt.rcParams["font.family"] = ["Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(WORK_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)

BG = "#0a1420"

# ========== 图 1: SDLC 六阶段 Agent 分工时间线 ==========
def draw_sdlc_flow():
    fig, ax = plt.subplots(figsize=(14, 4.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    stages = [
        ("Plan", "规划", "#f97316", "#fed7aa"),
        ("Design", "设计", "#3b82f6", "#bfdbfe"),
        ("Build", "构建", "#22c55e", "#bbf7d0"),
        ("Test", "测试", "#a855f7", "#ddd6fe"),
        ("Deploy", "部署", "#06b6d4", "#a5f3fc"),
        ("Maintain", "维护", "#f59e0b", "#fde68a"),
    ]

    # 时间线
    ax.plot([0.5, 13.5], [2.25, 2.25], color="#334155", linewidth=2, zorder=1)

    for i, (en, cn, color, light) in enumerate(stages):
        x = 1.2 + i * 2.0
        # 节点圆点
        ax.add_patch(plt.Circle((x, 2.25), 0.35, color=color, zorder=3))
        ax.add_patch(plt.Circle((x, 2.25), 0.22, color=BG, zorder=4))
        ax.add_patch(plt.Circle((x, 2.25), 0.12, color=color, zorder=5))

        # 上方英文
        ax.text(x, 3.2, en, ha="center", va="center",
                fontsize=12, fontweight="bold", color="white")
        # 上方中文
        ax.text(x, 2.7, cn, ha="center", va="center",
                fontsize=9, color=light)
        # 下方 agent 角色
        ax.text(x, 1.6, f"{en.lower()}-agent", ha="center", va="center",
                fontsize=8.5, color="#94a3b8",
                bbox=dict(boxstyle="round,pad=0.3", fc="#1e293b", ec=color, lw=1))
        # 编号
        ax.text(x, 0.95, f"0{i+1}", ha="center", va="center",
                fontsize=7, color="#64748b", fontweight="bold")

    # 大标题
    ax.text(7, 4.1, "SDLC Six-Stage Agent Pipeline",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="white")
    ax.text(7, 3.8, "Orchestrator routes via A2A protocol",
            ha="center", va="center", fontsize=9, color="#64748b")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "sdlc_flow.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ sdlc_flow.png")


# ========== 图 2: A2A 双向通信架构 ==========
def draw_a2a_arch():
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Orchestrator（中心）
    orch = FancyBboxPatch((4.5, 2.2), 3, 1.6, boxstyle="round,pad=0.1",
                          fc="#1e293b", ec="#f97316", lw=2)
    ax.add_patch(orch)
    ax.text(6, 3.25, "Orchestrator", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#f97316")
    ax.text(6, 2.65, "hermes A2A", ha="center", va="center",
            fontsize=8, color="#94a3b8")
    ax.text(6, 2.35, "gateway", ha="center", va="center",
            fontsize=8, color="#94a3b8")

    # Left: 入站（inbound peers）
    inbound_peers = [("Plan Agent", 0.8, 4.5, "#3b82f6"),
                    ("Design Agent", 0.8, 3.0, "#a855f7"),
                    ("Build Agent", 0.8, 1.5, "#22c55e")]

    for name, x, y, color in inbound_peers:
        box = FancyBboxPatch((x, y - 0.4), 1.8, 0.8, boxstyle="round,pad=0.05",
                              fc="#1e293b", ec=color, lw=1.5)
        ax.add_patch(box)
        ax.text(x + 0.9, y, name, ha="center", va="center",
                fontsize=9, fontweight="bold", color=color)

        # 箭头
        ax.annotate("", xy=(4.5, 3.0), xytext=(x + 1.8, y),
                    arrowprops=dict(arrowstyle="->", color=color,
                                    lw=1.5, connectionstyle="arc3,rad=0.15"))

    # Right: 出站（outbound peers）
    outbound_peers = [("Test Agent", 9.4, 4.5, "#a855f7"),
                     ("Deploy Agent", 9.4, 3.0, "#06b6d4"),
                     ("Maintain Agent", 9.4, 1.5, "#f59e0b")]

    for name, x, y, color in outbound_peers:
        box = FancyBboxPatch((x, y - 0.4), 1.8, 0.8, boxstyle="round,pad=0.05",
                              fc="#1e293b", ec=color, lw=1.5)
        ax.add_patch(box)
        ax.text(x + 0.9, y, name, ha="center", va="center",
                fontsize=9, fontweight="bold", color=color)

        ax.annotate("", xy=(x, y), xytext=(7.5, 3.0),
                    arrowprops=dict(arrowstyle="->", color=color,
                                    lw=1.5, connectionstyle="arc3,rad=-0.15"))

    # 标签
    ax.text(0.5, 5.7, "Inbound", ha="left", va="center",
            fontsize=10, fontweight="bold", color="#3b82f6")
    ax.text(11.5, 5.7, "Outbound", ha="right", va="center",
            fontsize=10, fontweight="bold", color="#06b6d4")

    # 中心标注
    ax.text(6, 4.25, "A2A v1.0 Protocol",
            ha="center", va="center", fontsize=9,
            color="#f97316", style="italic")
    ax.text(6, 1.85, "Agent Card / JSON-RPC 2.0 / SSE",
            ha="center", va="center", fontsize=7.5,
            color="#64748b")

    # 标题
    ax.text(6, 5.3, "Hermes A2A Bidirectional Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "a2a_arch.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ a2a_arch.png")


# ========== 图 3: A2A 出站工具 + 入站接口 ==========
def draw_a2a_tools():
    fig, ax = plt.subplots(figsize=(14, 5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis("off")

    tools = [
        ("a2a_discover", "Fetch agent card", "#f97316"),
        ("a2a_call", "Send single task", "#3b82f6"),
        ("a2a_orchestrate", "Fan-out by capability", "#22c55e"),
        ("a2a_list", "List peers & metrics", "#a855f7"),
        ("a2a_history", "Recall conversation", "#06b6d4"),
    ]

    for i, (name, desc, color) in enumerate(tools):
        x = 0.4 + i * 2.7
        w = 2.5
        box = FancyBboxPatch((x, 1.0), w, 3.2, boxstyle="round,pad=0.12",
                              fc="#1e293b", ec=color, lw=2)
        ax.add_patch(box)

        # 顶部色带
        top = FancyBboxPatch((x + 0.05, 3.7), w - 0.1, 0.35,
                              boxstyle="round,pad=0.02",
                              fc=color, ec="none")
        ax.add_patch(top)

        ax.text(x + w/2, 3.2, name, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="white")
        ax.text(x + w/2, 2.7, desc, ha="center", va="center",
                fontsize=7.5, color="#94a3b8")

        # 底部数字
        ax.text(x + w/2, 1.45, f"tool 0{i+1}", ha="center", va="center",
                fontsize=7, color="#64748b")

    ax.text(7, 4.75, "A2A Outbound Toolset (hermes tools enable a2a)",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color="white")

    # 入站接口小标注
    ax.text(7, 0.55, "Inbound :9900  |  GET /.well-known/agent-card.json  |  POST / JSON-RPC 2.0  |  SSE streaming",
            ha="center", va="center", fontsize=8, color="#f97316",
            bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec="#f97316", lw=1.5))

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "a2a_tools.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ a2a_tools.png")


# ========== 图 4: Plan Agent ↔ Design Agent 交互流程 ==========
def draw_plan_design():
    fig, ax = plt.subplots(figsize=(14, 5.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    # 两列：Plan Agent 和 Design Agent
    agents = [
        ("Plan Agent", 3.0, "#f97316", "#fed7aa"),
        ("Design Agent", 11.0, "#3b82f6", "#bfdbfe"),
    ]

    for name, x, color, light in agents:
        box = FancyBboxPatch((x - 1.2, 4.6), 2.4, 0.6,
                              boxstyle="round,pad=0.1",
                              fc="#1e293b", ec=color, lw=2)
        ax.add_patch(box)
        ax.text(x, 4.9, name, ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)

    # 步骤（从顶到底）
    steps = [
        # (y, from_x, to_x, from_text, to_text, step_num, color, arrow_dir)
        (4.2, 3.0, 11.0, "", "receives task brief", "01", "#3b82f6", "right"),
        (3.4, 3.0, 11.0, "outputs plan.txt\nplan.json", "generates PRD + API\nspec + wireframes", "02", "#22c55e", "both"),
        (2.6, 3.0, 11.0, "", "returns artifacts\nurls / paths", "03", "#a855f7", "left"),
        (1.8, 3.0, 11.0, "validates against\nplan spec", "", "04", "#f97316", "right"),
        (1.0, 3.0, 11.0, "signs off →\nhand off to Build", "", "05", "#06b6d4", "right"),
    ]

    for y, fx, tx, ft, tt, num, color, direction in steps:
        # 中间步骤号
        mid_x = 7.0
        ax.add_patch(plt.Circle((mid_x, y), 0.28, color=color, zorder=5))
        ax.text(mid_x, y, num, ha="center", va="center",
                fontsize=8, fontweight="bold", color="white", zorder=6)

        # 左右文本
        if ft:
            ax.text(fx, y, ft, ha="center", va="center",
                    fontsize=8, color="#94a3b8",
                    bbox=dict(boxstyle="round,pad=0.2", fc="#1e293b", ec=color, lw=1))
        if tt:
            ax.text(tx, y, tt, ha="center", va="center",
                    fontsize=8, color="#94a3b8",
                    bbox=dict(boxstyle="round,pad=0.2", fc="#1e293b", ec=color, lw=1))

        # 连接线
        if direction in ("right", "both"):
            ax.plot([fx + 1.3, mid_x - 0.28], [y, y], color=color, lw=1, ls="-")
        if direction in ("left", "both"):
            ax.plot([mid_x + 0.28, tx - 1.3], [y, y], color=color, lw=1, ls="-")

    # 标题
    ax.text(7, 5.3, "Example : Plan Agent  →  Design Agent A2A Handshake",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="white")

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS, "plan_design.png"), dpi=160,
                facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print("✓ plan_design.png")


if __name__ == "__main__":
    draw_sdlc_flow()
    draw_a2a_arch()
    draw_a2a_tools()
    draw_plan_design()
    print(f"\n全部生成于 {ASSETS}")
