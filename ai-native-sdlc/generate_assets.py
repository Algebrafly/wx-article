#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import matplotlib.patches as mpatches

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0f1115'
PANEL = '#181b21'
TEXT = '#e8eaed'
TEXT_DIM = '#9aa0a6'
ACCENT = '#4ea1f7'
ACCENT2 = '#34d399'
ACCENT3 = '#f59e0b'
ACCENT4 = '#f87171'
GRID = '#2a2e36'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 图 1：传统 vs AI-native SDLC 对比 ──────────────────────────────────────
def draw_shift():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(6, 7.4, '传统 SDLC vs AI-native SDLC', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.8, '代码不再是瓶颈，慢的是人走过的流程', fontsize=13,
            color=TEXT_DIM, ha='center')

    rows = [
        ('Plan', '开会写 PRD', 'intent.md，自然语言起步'),
        ('Design', '分析师写需求，设计师再画稿', '一次会话产出 spec.md'),
        ('Build', '工程师手写代码', 'plan.md 定计划，agent 实现'),
        ('Test', 'QA 阶段 gate', '持续 eval + agent 自检'),
        ('Deploy', '人审每一行代码', 'AI review + hook 审批门'),
        ('Maintain', '人等告警', '触发器自动写回 intent.md'),
    ]

    y = 5.8
    h = 0.72
    for stage, trad, ainative in rows:
        # 阶段标签
        ax.text(0.6, y, stage, fontsize=12, fontweight='bold', color=ACCENT,
                ha='left', va='center')
        # 传统列
        rect1 = FancyBboxPatch((2.2, y - h/2), 4.0, h,
                               boxstyle='round,pad=0.02,rounding_size=0.08',
                               facecolor=PANEL, edgecolor=GRID, linewidth=1)
        ax.add_patch(rect1)
        ax.text(2.4, y, trad, fontsize=10, color=TEXT_DIM, ha='left', va='center')
        # AI-native 列
        rect2 = FancyBboxPatch((6.4, y - h/2), 5.0, h,
                               boxstyle='round,pad=0.02,rounding_size=0.08',
                               facecolor=PANEL, edgecolor=ACCENT2, linewidth=1.5)
        ax.add_patch(rect2)
        ax.text(6.6, y, ainative, fontsize=10, color=TEXT, ha='left', va='center')
        y -= 0.95

    # 列标题
    ax.text(4.2, 6.35, '传统 SDLC', fontsize=13, fontweight='bold',
            color=TEXT_DIM, ha='center', va='center')
    ax.text(8.9, 6.35, 'AI-native SDLC', fontsize=13, fontweight='bold',
            color=ACCENT2, ha='center', va='center')

    save(fig, 'shift.png')


# ── 图 2：六个阶段 + artifact 链 ───────────────────────────────────────────
def draw_artifacts():
    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.text(6.5, 5.0, 'AI-native SDLC 的 artifact 链', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 4.5, '每个阶段提交一份机器可读、人类可审的 artifact', fontsize=13,
            color=TEXT_DIM, ha='center')

    stages = [
        ('Plan', 'intent.md', ACCENT),
        ('Design', 'spec.md', ACCENT),
        ('Build', 'plan.md\nCLAUDE.md', ACCENT2),
        ('Test', 'evals/', ACCENT2),
        ('Deploy', 'PR + review', ACCENT3),
        ('Maintain', 'incident\nintent.md', ACCENT4),
    ]

    x = 1.0
    w = 1.7
    h = 1.2
    for i, (stage, artifact, color) in enumerate(stages):
        rect = FancyBboxPatch((x, 2.4), w, h,
                              boxstyle='round,pad=0.02,rounding_size=0.1',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, 3.25, stage, fontsize=12, fontweight='bold',
                color=color, ha='center', va='center')
        ax.text(x + w/2, 2.75, artifact, fontsize=9, color=TEXT,
                ha='center', va='center', linespacing=1.4)

        # 箭头
        if i < len(stages) - 1:
            ax.annotate('', xy=(x + w + 0.15, 3.0), xytext=(x + w - 0.15, 3.0),
                        arrowprops=dict(arrowstyle='->', color=GRID, lw=2))
        x += w + 0.45

    # 循环回 Plan
    ax.annotate('', xy=(1.0, 2.25), xytext=(12.0, 2.25),
                arrowprops=dict(arrowstyle='->', color=ACCENT4, lw=1.5,
                               connectionstyle='arc3,rad=-0.25'))
    ax.text(6.5, 1.6, '维护阶段发现的异常写回 intent.md，循环重新开始', fontsize=11,
            color=TEXT_DIM, ha='center', va='center')

    save(fig, 'artifacts.png')


# ── 图 3：三层控制模型 ─────────────────────────────────────────────────────
def draw_controls():
    fig, ax = plt.subplots(figsize=(11, 8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.4, '三层控制模型', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(5.5, 6.8, '从建议到强制，从软约束到硬边界', fontsize=13,
            color=TEXT_DIM, ha='center')

    layers = [
        ('Skills', '建议层', '把规范写进 SKILL.md\nAgent 写代码时主动参考', ACCENT),
        ('Hooks', '强制层', 'PreToolUse 脚本\nallow / ask / block', ACCENT3),
        ('Permissions + Sandbox', '边界层', '工具级 deny + OS 级隔离\n控制网络和凭证', ACCENT4),
    ]

    y = 5.5
    h = 1.1
    for title, subtitle, desc, color in layers:
        w = 8.5
        rect = FancyBboxPatch((5.5 - w/2, y - h/2), w, h,
                              boxstyle='round,pad=0.05,rounding_size=0.12',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(5.5 - w/2 + 0.35, y + 0.18, title, fontsize=16, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(5.5 - w/2 + 0.35, y - 0.18, desc, fontsize=11,
                color=TEXT, ha='left', va='center', linespacing=1.4)
        ax.text(5.5 + w/2 - 0.35, y, subtitle, fontsize=12, fontweight='bold',
                color=color, ha='right', va='center', alpha=0.8)
        y -= 1.7

    # 右侧说明
    ax.text(10.2, 5.5, '越来越\n软', fontsize=11, color=TEXT_DIM, ha='center',
            va='center', linespacing=1.5)
    ax.text(10.2, 2.1, '越来越\n硬', fontsize=11, color=TEXT_DIM, ha='center',
            va='center', linespacing=1.5)
    ax.annotate('', xy=(10.2, 2.8), xytext=(10.2, 4.8),
                arrowprops=dict(arrowstyle='->', color=TEXT_DIM, lw=1.5))

    save(fig, 'controls.png')


# ── 图 4：采纳路径 ─────────────────────────────────────────────────────────
def draw_adoption():
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(6, 5.4, 'AI-native SDLC 采纳路径', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 4.8, '不用一次性改造全部流程，从 artifact 链开始', fontsize=13,
            color=TEXT_DIM, ha='center')

    steps = [
        ('1', '个人', '用 /init 生成 CLAUDE.md\nplan mode 写 plan.md', ACCENT),
        ('2', '团队', '共享 CLAUDE.md 和 skills\nPR 引入 AI review', ACCENT2),
        ('3', '部门', 'CI 跑 agent evals\nhook 做代码级门禁', ACCENT3),
        ('4', '企业', 'managed settings + sandbox\n生产审批门与人审分离', ACCENT4),
    ]

    x = 1.2
    w = 2.3
    h = 2.4
    for num, title, desc, color in steps:
        rect = FancyBboxPatch((x, 1.8), w, h,
                              boxstyle='round,pad=0.05,rounding_size=0.12',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + 0.25, 3.9, num, fontsize=22, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + w/2, 3.2, title, fontsize=15, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(x + w/2, 2.55, desc, fontsize=10, color=TEXT_DIM,
                ha='center', va='center', linespacing=1.5)
        if num != '4':
            ax.annotate('', xy=(x + w + 0.2, 3.0), xytext=(x + w - 0.15, 3.0),
                        arrowprops=dict(arrowstyle='->', color=GRID, lw=2))
        x += w + 0.5

    save(fig, 'adoption.png')


if __name__ == '__main__':
    draw_shift()
    draw_artifacts()
    draw_controls()
    draw_adoption()
    print('4 张配图已生成到', ASSETS)
