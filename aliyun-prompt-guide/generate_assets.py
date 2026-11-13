#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#fdf8f2'
PANEL = '#ffffff'
TEXT = '#1f1f1f'
DIM = '#8a8a8a'
ORANGE = '#ea580c'
BLUE = '#2563eb'
GREEN = '#059669'
PURPLE = '#7c3aed'
GRID = '#e5e5e5'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：Prompt 框架六块 ──────────────────────────────────────────────────
def draw_framework():
    fig, ax = plt.subplots(figsize=(12, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6, 6.7, '阿里云百炼 Prompt 框架', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.2, '六块积木，缺了哪块模型都偏', fontsize=12.5, color=DIM, ha='center')

    blocks = [
        ('背景', '任务所处的环境，帮模型理解上下文', '#fef3c7', '#d97706'),
        ('目的', '让模型完成什么，最核心的指令', '#dbeafe', '#2563eb'),
        ('风格', '输出用名人/流派/专家的哪一路', '#dcfce7', '#059669'),
        ('语气', '正式？诙谐？温馨？关怀？', '#fce7f3', '#db2777'),
        ('受众', '写给谁看，决定语言深度', '#ede9fe', '#7c3aed'),
        ('输出', '列表？JSON？报告？定死格式', '#fee2e2', '#dc2626'),
    ]

    w = 3.55; h = 2.1; gap_x = 0.2; gap_y = 0.25
    positions = [(0.5, 4.2), (4.05, 4.2), (7.6, 4.2),
                 (0.5, 1.85), (4.05, 1.85), (7.6, 1.85)]

    for (title, desc, fc, ec), (x, y) in zip(blocks, positions):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.06,rounding_size=0.16',
                                    facecolor=fc, edgecolor=ec, linewidth=2))
        ax.text(x + w/2, y + h - 0.45, title, fontsize=15, fontweight='bold',
                color=ec, ha='center', va='center')
        ax.text(x + w/2, y + 0.9, desc, fontsize=9.5, color=TEXT, ha='center',
                va='center', linespacing=1.5)

    save(fig, 'framework.png')


# ── 2：模糊 vs 清晰 ───────────────────────────────────────────────────────
def draw_clarity():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.3, '第一条铁律：写清再说话', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.8, '模型像新人同事，不给清楚就会乱做', fontsize=12.5, color=DIM, ha='center')

    # left: 模糊
    ax.add_patch(FancyBboxPatch((0.4, 1.2), 5.4, 4.0,
                                boxstyle='round,pad=0.06,rounding_size=0.16',
                                facecolor='#fef2f2', edgecolor='#dc2626', linewidth=2))
    ax.text(3.1, 4.7, '[X] 模糊', fontsize=15, fontweight='bold', color='#dc2626', ha='center')
    ax.text(3.1, 4.15, '帮我推广新产品', fontsize=11.5, color=TEXT, ha='center', va='center')
    ax.text(3.1, 3.7, '（一句话描述）', fontsize=10, color=DIM, ha='center')
    ax.text(3.1, 2.8, '→ 输出泛化，没细节', fontsize=10.5, color='#991b1b', ha='center',
            style='italic')

    # right: 清晰
    ax.add_patch(FancyBboxPatch((6.2, 1.2), 5.4, 4.0,
                                boxstyle='round,pad=0.06,rounding_size=0.16',
                                facecolor='#f0fdf4', edgecolor='#059669', linewidth=2))
    ax.text(8.9, 4.7, '[OK] 清晰', fontsize=15, fontweight='bold', color='#059669', ha='center')
    ax.text(8.9, 4.15, '写一条微博帖，突出轻薄、', fontsize=11, color=TEXT, ha='center', va='center')
    ax.text(8.9, 3.85, '高性能、便利性，贴合年轻受众', fontsize=11, color=TEXT, ha='center', va='center')
    ax.text(8.9, 3.5, '（具体卖点 + 平台 + 受众）', fontsize=10, color=DIM, ha='center')
    ax.text(8.9, 2.8, '→ 细节丰富，针对性强', fontsize=10.5, color='#065f46', ha='center',
            style='italic')

    save(fig, 'clarity.png')


# ── 3：三个优化技巧 ───────────────────────────────────────────────────────
def draw_three_tips():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.3, '三个让输出更稳的小技巧', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.8, '样例 → 步骤 → 分隔符，复杂度依次升级', fontsize=12.5, color=DIM, ha='center')

    tips = [
        ('① 给样例', '让模型模仿格式、语气、文法\n多次输出更一致', ORANGE),
        ('② 写步骤', '复杂任务告诉模型怎么分解\n尤其推理/数学题', BLUE),
        ('③ 加分隔符', '### / === / >>>\n帮模型解析复杂 prompt', PURPLE),
    ]

    w = 3.5; h = 3.0; gap = 0.25
    x = (12 - (w * 3 + gap * 2)) / 2
    for title, desc, color in tips:
        ax.add_patch(FancyBboxPatch((x, 1.5), w, h,
                                    boxstyle='round,pad=0.06,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + w/2, 4.1, title, fontsize=16, fontweight='bold', color=color, ha='center')
        ax.text(x + w/2, 2.8, desc, fontsize=10.5, color=TEXT, ha='center', va='center',
                linespacing=1.6)
        x += w + gap

    save(fig, 'three_tips.png')


# ── 4：模板 + 技巧的叠加 ──────────────────────────────────────────────────
def draw_stack():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.axis('off')

    ax.text(6, 6.0, '好 prompt 是叠出来的', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.5, '框架打底，技巧叠加，复杂度自己定', fontsize=12.5, color=DIM, ha='center')

    layers = [
        ('#背景# / #目的# / #风格# / #语气# / #受众# / #输出#', 'Prompt 框架', BLUE),
        ('再加上 #任务步骤# 或输出样例', '优化技巧', ORANGE),
        ('### 三段式分隔  或  >>> 包裹输入原文', '分隔符（复杂 prompt 才需要）', PURPLE),
    ]

    w = 10.8; h = 1.05; x = (12 - w) / 2; y = 4.3
    for content, label, color in layers:
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.3, y + h/2, content, fontsize=11, color=color, ha='left', va='center')
        ax.text(x + w - 0.3, y + h/2, label, fontsize=10, color=DIM, ha='right', va='center')
        y -= (h + 0.32)

    ax.text(6, 0.9, '框架是地基。样例、步骤、分隔符是往上盖的楼层，任务有多复杂，就盖多高。',
            fontsize=10.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'stack.png')


if __name__ == '__main__':
    draw_framework(); draw_clarity(); draw_three_tips(); draw_stack()
    print('done')
