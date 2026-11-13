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

BG = '#0f172a'
PANEL = '#1e293b'
TEXT = '#e2e8f0'
DIM = '#64748b'
BLUE = '#3b82f6'
CYAN = '#22d3ee'
GREEN = '#10b981'
AMBER = '#f59e0b'
ROSE = '#f43f5e'
GRID = '#334155'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：三个参数 ───────────────────────────────────────────────────────
def draw_params():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.3, '三个和 prompt 有关的参数', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.8, '文生图 V2 默认会开自动改写', fontsize=12.5, color=DIM, ha='center')

    items = [
        ('prompt', '正向提示词', '用文字描述想生成的图片\n支持中英文', BLUE),
        ('negative_prompt', '反向提示词', '描述不希望出现的内容\n能避免常见瑕疵', ROSE),
        ('prompt_extend', '智能改写', '大模型自动扩写和优化\nV2 默认 true，推荐保留', GREEN),
    ]

    w = 3.55; h = 3.0; gap = 0.25
    x = (12 - (w * 3 + gap * 2)) / 2
    for key, label, desc, color in items:
        ax.add_patch(FancyBboxPatch((x, 1.5), w, h,
                                    boxstyle='round,pad=0.06,rounding_size=0.16',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + w/2, 3.9, key, fontsize=13, fontweight='bold', color=color,
                ha='center', fontfamily='monospace')
        ax.text(x + w/2, 3.2, label, fontsize=11, color=TEXT, ha='center')
        ax.text(x + w/2, 2.35, desc, fontsize=9.5, color=DIM, ha='center', va='center',
                linespacing=1.6)
        x += w + gap

    save(fig, 'params.png')


# ── 2：基础 vs 进阶 ──────────────────────────────────────────────────────
def draw_formulas():
    fig, ax = plt.subplots(figsize=(12, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6, 6.9, '两条公式，按需选', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.4, '新手用基础，有经验往上盖', fontsize=12.5, color=DIM, ha='center')

    # 基础公式（上）
    ax.add_patch(FancyBboxPatch((0.55, 4.45), 10.9, 1.55,
                                boxstyle='round,pad=0.06,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=CYAN, linewidth=2))
    ax.text(0.85, 5.55, '基础公式', fontsize=12, fontweight='bold', color=CYAN, ha='left')
    ax.text(0.85, 5.15, '面向新手 / 灵感启发', fontsize=9.5, color=DIM, ha='left')
    ax.text(6, 4.9, '主体  +  场景  +  风格', fontsize=17, fontweight='bold',
            color=TEXT, ha='center')

    # 进阶公式（下，比基础宽一点）
    ax.add_patch(FancyBboxPatch((0.55, 1.1), 10.9, 2.9,
                                boxstyle='round,pad=0.06,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=2))
    ax.text(0.85, 3.6, '进阶公式', fontsize=12, fontweight='bold', color=BLUE, ha='left')
    ax.text(0.85, 3.2, '面向有经验用户 / 追求画质', fontsize=9.5, color=DIM, ha='left')
    ax.text(6, 2.55, '主体 + 场景 + 风格 + 镜头语言 + 氛围词 + 细节修饰',
            fontsize=13, fontweight='bold', color=TEXT, ha='center')
    ax.text(6, 2.0, '（主体描述）  （场景描述）  （定义风格）', fontsize=9.5,
            color=DIM, ha='center')

    # 箭头
    ax.annotate('', xy=(6, 4.45), xytext=(6, 4.2),
                arrowprops=dict(arrowstyle='->', color=GRID, lw=1.8))
    ax.text(6.25, 4.32, '往上加', fontsize=9, color=DIM, ha='left', va='center')

    save(fig, 'formulas.png')


# ── 3：五大词典 ─────────────────────────────────────────────────────────
def draw_lexicon():
    fig, ax = plt.subplots(figsize=(12, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6, 6.7, '五大词典维度', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.2, '每一项都有现成词可以抄', fontsize=12.5, color=DIM, ha='center')

    items = [
        ('景别', '特写 / 近景 / 中景 / 远景', AMBER),
        ('视角', '平视 / 俯视 / 仰视 / 航拍', BLUE),
        ('镜头类型', '微距 / 超广角 / 长焦 / 鱼眼', CYAN),
        ('风格', '写实 / 水彩 / 水墨 / 3D卡通 / 粘土 / 废土 …', GREEN),
        ('光线', '自然光 / 逆光 / 霓虹灯 / 氛围光', ROSE),
    ]

    w = 10.8; h = 0.85; x = (12 - w) / 2; y = 5.45
    for label, examples, color in items:
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.05,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.3, y + h/2, label, fontsize=12, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + 3.0, y + h/2, examples, fontsize=10, color=TEXT, ha='left', va='center')
        y -= (h + 0.28)

    save(fig, 'lexicon.png')


# ── 4：完整示例 ──────────────────────────────────────────────────────────
def draw_example():
    fig, ax = plt.subplots(figsize=(12, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6, 6.7, '完整示例', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.2, '正向 prompt + 反向 + 自动改写', fontsize=12.5, color=DIM, ha='center')

    # prompt（大）
    ax.add_patch(FancyBboxPatch((0.55, 3.5), 10.9, 2.3,
                                boxstyle='round,pad=0.06,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=2))
    ax.text(0.85, 5.45, 'prompt', fontsize=12, fontweight='bold', color=BLUE,
            ha='left', fontfamily='monospace')
    ax.text(0.85, 4.95, '羊毛毡制成的大熊猫，头戴大檐帽，穿着蓝色警服马甲，腰带',
            fontsize=10.5, color=TEXT, ha='left')
    ax.text(0.85, 4.65, '扎着，携带警械装备，蓝色手套，皮鞋，大步奔跑，毛毡效果',
            fontsize=10.5, color=TEXT, ha='left')
    ax.text(0.85, 4.35, '动物王国街道，夜晚，路灯，皮克斯风格，摄影镜头，居中构图，逆光',
            fontsize=10.5, color=TEXT, ha='left')

    # negative_prompt
    ax.add_patch(FancyBboxPatch((0.55, 1.25), 5.25, 1.5,
                                boxstyle='round,pad=0.06,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ROSE, linewidth=2))
    ax.text(0.85, 2.45, 'negative_prompt', fontsize=12, fontweight='bold',
            color=ROSE, ha='left', fontfamily='monospace')
    ax.text(0.85, 2.0, '写实人物，畸形手指，低分辨率',
            fontsize=10.5, color=TEXT, ha='left')

    # prompt_extend
    ax.add_patch(FancyBboxPatch((6.2, 1.25), 5.25, 1.5,
                                boxstyle='round,pad=0.06,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=2))
    ax.text(6.5, 2.45, 'prompt_extend', fontsize=12, fontweight='bold',
            color=GREEN, ha='left', fontfamily='monospace')
    ax.text(6.5, 2.0, 'true（默认，开启智能改写）',
            fontsize=10.5, color=TEXT, ha='left')

    save(fig, 'example.png')


if __name__ == '__main__':
    draw_params(); draw_formulas(); draw_lexicon(); draw_example()
    print('done')
