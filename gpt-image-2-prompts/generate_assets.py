#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0f0d14'
PANEL = '#1a1722'
TEXT = '#f0eef5'
DIM = '#9b95a8'
PURPLE = '#a855f7'
CYAN = '#22d3ee'
PINK = '#f472b6'
AMBER = '#fbbf24'
GRID = '#2e2840'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：好提示词的五个零件 ─────────────────────────────────────────────────
def draw_anatomy():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis('off')

    ax.text(6, 6.5, '一条好提示词的五个零件', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.0, '按顺序写，漏一个，命中率就掉一档', fontsize=12.5, color=DIM, ha='center')

    parts = [
        ('1 Subject', '主体', '具体名词，别写「一个人」', PURPLE),
        ('2 Style', '风格', '只定一种视觉语言', PINK),
        ('3 Composition', '构图', '机位、焦距、景别', CYAN),
        ('4 Lighting', '光线', '承担 60% 的情绪', AMBER),
        ('5 Detail anchors', '锚点', '比例、配色、图中文字', PURPLE),
    ]

    w = 9.2; h = 0.78; x = (12 - w) / 2; y = 4.95
    for title, cn, desc, color in parts:
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.3, y + h/2, title, fontsize=13, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + 3.0, y + h/2, cn, fontsize=11, color=TEXT, ha='left', va='center')
        ax.text(x + w - 0.3, y + h/2, desc, fontsize=9.5, color=DIM, ha='right', va='center')

        # arrow down to next box
        if y > 1.4:
            ax.annotate('', xy=(6, y - 0.55), xytext=(6, y),
                        arrowprops=dict(arrowstyle='->', color=GRID, lw=1.5))
        y -= (h + 0.55)

    ax.text(6, 0.55, 'GPT Image 2 吃长提示词。你写得越像镜头脚本，它跟得越准。',
            fontsize=10.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'anatomy.png')


# ── 2：四个常见错误 ───────────────────────────────────────────────────────
def draw_mistakes():
    fig, ax = plt.subplots(figsize=(12, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6, 6.7, '四个让命中率从 30% 掉到 80% 的坑', fontsize=21, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.2, '反过来避掉它们，出图稳定度会高很多', fontsize=12, color=DIM, ha='center')

    items = [
        ('塞太多主体', '一次只放一个主角', PINK),
        ('模糊形容词', '换成技术风格词', AMBER),
        ('混搭不兼容风格', '一种视觉语言一条 prompt', CYAN),
        ('不写画幅比例', 'prompt + API size 同时写', PURPLE),
    ]

    for i, (wrong, fix, color) in enumerate(items):
        col = i % 2; row = i // 2
        x = 0.55 + col * 5.9
        y = 4.95 - row * 2.8
        ax.add_patch(FancyBboxPatch((x, y - 2.3), 5.5, 2.3,
                                    boxstyle='round,pad=0.05,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.3, y - 0.45, '×', fontsize=18, color='#ef4444', ha='left', va='center')
        ax.text(x + 0.9, y - 0.45, wrong, fontsize=13, fontweight='bold',
                color=TEXT, ha='left', va='center')
        ax.text(x + 0.3, y - 1.2, fix, fontsize=10.5, color=DIM, ha='left', va='center',
                linespacing=1.6)
        ax.add_patch(FancyBboxPatch((x + 0.3, y - 1.95), 1.8, 0.45,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 1.2, y - 1.72, 'FIX', fontsize=9, color=BG,
                fontweight='bold', ha='center', va='center')

    save(fig, 'mistakes.png')


# ── 3：五条现成模板 ───────────────────────────────────────────────────────
def draw_templates():
    fig, ax = plt.subplots(figsize=(12, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6, 6.9, '五条可以复制的模板', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.4, '替换 {} 占位符就能跑', fontsize=12.5, color=DIM, ha='center')

    templates = [
        ('Cinematic portrait', '电影感人像', PURPLE),
        ('Product mockup', '产品样机', PINK),
        ('Typographic poster', '字体海报', CYAN),
        ('Educational infographic', '信息图', AMBER),
        ('Character sheet', '角色设定表', PURPLE),
    ]

    w = 10.8; h = 0.9; gap = 0.35; x = (12 - w) / 2; y = 5.55
    for name, cn, color in templates:
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.3, y + h/2, name, fontsize=12.5, fontweight='bold',
                color=color, ha='left', va='center', fontfamily='monospace')
        ax.text(x + w - 0.3, y + h/2, cn, fontsize=11, color=DIM, ha='right', va='center')
        y -= (h + gap)

    ax.text(6, 0.35, '先套模板跑一次，确认模型理解了结构，再往里填自己的主体。',
            fontsize=10.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'templates.png')


# ── 4：怎么用 ─────────────────────────────────────────────────────────────
def draw_access():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.35, '两条入口，尺寸别只靠 prompt', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.85, 'ChatGPT 零代码 / API 批量生产，size 参数也要设', fontsize=12.5,
            color=DIM, ha='center')

    # left card
    ax.add_patch(FancyBboxPatch((0.6, 2.0), 5.0, 3.4,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=PURPLE, linewidth=2))
    ax.text(3.1, 5.0, 'ChatGPT', fontsize=15, fontweight='bold', color=PURPLE, ha='center')
    ax.text(3.1, 4.5, 'Plus / Pro / Team / Enterprise', fontsize=10, color=DIM, ha='center')
    ax.text(3.1, 3.85, '直接粘贴 prompt', fontsize=11, color=TEXT, ha='center')
    ax.text(3.1, 3.35, '适合设计师、内容创作者', fontsize=9.5, color=DIM, ha='center')
    ax.text(3.1, 2.5, '每小时约 30-50 张', fontsize=9.5, color=DIM, ha='center')

    # right card
    ax.add_patch(FancyBboxPatch((6.4, 2.0), 5.0, 3.4,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=CYAN, linewidth=2))
    ax.text(8.9, 5.0, 'Images API', fontsize=15, fontweight='bold', color=CYAN, ha='center')
    ax.text(8.9, 4.5, 'model: gpt-image-2', fontsize=10, color=DIM, ha='center',
            fontfamily='monospace')
    ax.text(8.9, 3.85, 'POST /v1/images/generations', fontsize=10, color=TEXT, ha='center',
            fontfamily='monospace')
    ax.text(8.9, 3.35, '控制 size / quality / n', fontsize=9.5, color=DIM, ha='center')
    ax.text(8.9, 2.5, '适合批量、产品集成', fontsize=9.5, color=DIM, ha='center')

    # bottom sizes
    sizes = [('1:1', '1024×1024'), ('2:3 竖版', '1024×1536'), ('3:2 横版', '1536×1024')]
    sx = 1.8
    for ratio, px in sizes:
        ax.add_patch(FancyBboxPatch((sx, 0.6), 2.5, 0.95,
                                    boxstyle='round,pad=0.05,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=GRID, linewidth=1))
        ax.text(sx + 1.25, 1.15, ratio, fontsize=11, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(sx + 1.25, 0.82, px, fontsize=8.5, color=DIM, ha='center', va='center',
                fontfamily='monospace')
        sx += 3.1

    save(fig, 'access.png')


if __name__ == '__main__':
    draw_anatomy(); draw_mistakes(); draw_templates(); draw_access()
    print('done')
