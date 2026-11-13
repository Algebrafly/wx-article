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

BG = '#1a0f2e'
PANEL = '#2d1b4e'
TEXT = '#f0ecff'
DIM = '#9a8dbf'
PURPLE = '#a855f7'
TEAL = '#14b8a6'
PINK = '#ec4899'
AMBER = '#f59e0b'
GRID = '#4c3d7a'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：三种模式 ──────────────────────────────────────────────────────
def draw_modes():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.3, '三种输入模式，公式不同', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.8, '文生视频、图生视频、参考生视频各有一条公式', fontsize=12.5, color=DIM, ha='center')

    modes = [
        ('文生视频', 'prompt', '从纯文字到视频\n最自由也最需要结构化', PURPLE, '主体 + 场景 + 运动'),
        ('图生视频', 'image → video', '首帧 / 首尾帧\n主体风格已由图定\n只描述运动和运镜', TEAL, '运动 + 运镜'),
        ('参考生视频', 'ref video + ref image', '多参考文件\n用 图n / 视频n 指代\n可保持人物外观音色', PINK, '参考指代 + 动作 + 场景 + 台词'),
    ]

    w = 3.55; h = 3.6; gap = 0.25
    x = (12 - (w * 3 + gap * 2)) / 2
    for name, input_src, desc, color, formula in modes:
        ax.add_patch(FancyBboxPatch((x, 1.2), w, h,
                                    boxstyle='round,pad=0.06,rounding_size=0.16',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + w/2, 4.55, name, fontsize=14, fontweight='bold', color=color, ha='center')
        ax.text(x + w/2, 4.0, input_src, fontsize=9.5, color=DIM, ha='center')
        ax.text(x + w/2, 2.9, desc, fontsize=10, color=TEXT, ha='center', va='center',
                linespacing=1.6)
        # formula box
        ax.add_patch(FancyBboxPatch((x + 0.25, 1.55), w - 0.5, 0.9,
                                    boxstyle='round,pad=0.05,rounding_size=0.1',
                                    facecolor='#1a0f2e', edgecolor=color, linewidth=1.5))
        ax.text(x + w/2, 2.0, formula, fontsize=9.5, color=color, ha='center', va='center')
        x += w + gap

    save(fig, 'modes.png')


# ── 2：基础 vs 进阶 vs 图生 ──────────────────────────────────────────────
def draw_formulas():
    fig, ax = plt.subplots(figsize=(12, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6, 7.3, '三条核心公式', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.8, '视频独有的「运动」维度，是和图像 prompt 最大的差别', fontsize=12.5, color=DIM, ha='center')

    formulas = [
        ('基础公式', '面向新手 / 灵感启发', '主体  +  场景  +  运动', PURPLE),
        ('进阶公式', '追求画质与故事性',
         '主体（主体描述）+ 场景（场景描述）+ 运动（运动描述）+ 美学控制 + 风格化', TEAL),
        ('图生视频公式', '图像已定主体和风格', '运动  +  运镜', PINK),
    ]

    w = 11.0; x = (12 - w) / 2
    positions = [(x, 5.35), (x, 3.15), (x, 1.0)]
    h_list = [1.55, 1.95, 1.4]
    for (title, sub, formula, color), (bx, by), bh in zip(formulas, positions, h_list):
        ax.add_patch(FancyBboxPatch((bx, by), w, bh,
                                    boxstyle='round,pad=0.06,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(bx + 0.3, by + bh - 0.35, title, fontsize=12, fontweight='bold',
                color=color, ha='left')
        ax.text(bx + 0.3, by + bh - 0.75, sub, fontsize=9.5, color=DIM, ha='left')
        ax.text(bx + w/2, by + bh/2 - 0.3, formula, fontsize=14, fontweight='bold',
                color=TEXT, ha='center')

    save(fig, 'formulas.png')


# ── 3：声音三类 ─────────────────────────────────────────────────────────
def draw_sound():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.3, '视频声音：万相 3.0+ 支持原生音频', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.8, '声音公式：主体 + 场景 + 运动 + 声音描述（人声/音效/BGM）',
            fontsize=11.5, color=DIM, ha='center')

    items = [
        ('人声',
         '说话内容 + 情绪 + 语调 + 语速 + 音色 + 口音',
         '例：一个男人讲脱口秀\n他说道："好好学习"\n语气轻松，语速适中，声音清亮，美式英文',
         PURPLE),
        ('音效',
         '音源材质 + 行为 + 环境音',
         '例：玻璃小球从桌面掉在木质地面\n发出"砰"的声音\n室内安静环境',
         AMBER),
        ('BGM',
         '背景音乐/配乐 + 风格',
         '例：雨夜，阴森窄小的走廊\n尽头有一扇窗户\n配有悬疑风格背景音乐',
         TEAL),
    ]

    w = 3.55; h = 3.8; gap = 0.25
    x = (12 - (w * 3 + gap * 2)) / 2
    for title, structure, example, color in items:
        ax.add_patch(FancyBboxPatch((x, 1.1), w, h,
                                    boxstyle='round,pad=0.06,rounding_size=0.16',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + w/2, 4.55, title, fontsize=14, fontweight='bold', color=color, ha='center')
        ax.text(x + w/2, 3.85, structure, fontsize=9.5, color=TEXT, ha='center', va='center',
                linespacing=1.5)
        ax.add_patch(FancyBboxPatch((x + 0.25, 1.5), w - 0.5, 1.7,
                                    boxstyle='round,pad=0.05,rounding_size=0.1',
                                    facecolor='#1a0f2e', edgecolor=GRID, linewidth=1))
        ax.text(x + w/2, 2.35, example, fontsize=9, color=DIM, ha='center', va='center',
                linespacing=1.5, style='italic')
        x += w + gap

    save(fig, 'sound.png')


# ── 4：多镜头公式 ────────────────────────────────────────────────────────
def draw_multi_shot():
    fig, ax = plt.subplots(figsize=(12, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6, 6.9, '多镜头公式（万相 2.7/2.6）', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.4, '总体描述 + 镜头序号 + 时间戳 + 分镜内容', fontsize=12.5, color=DIM, ha='center')

    # 总体描述（顶部长条）
    ax.add_patch(FancyBboxPatch((0.55, 5.05), 10.9, 0.95,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=PURPLE, linewidth=2))
    ax.text(0.85, 5.52, '总体描述', fontsize=10.5, fontweight='bold', color=PURPLE, ha='left')
    ax.text(2.5, 5.52, '第三人称视角，关于放弃与重拾希望的短剧',
            fontsize=11, color=TEXT, ha='left')

    # 三个分镜
    shots = [
        ('镜头1 [0-3秒]', PINK,
         '男孩在操场角落独坐，低头望着信纸，轻轻叹气，眼神迷茫'),
        ('镜头2 [4-6秒]', AMBER,
         '硬切转场，固定机位，聚焦男孩的眼睛，泪光闪烁'),
        ('镜头3 [7-10秒]', TEAL,
         '转至简朴教室，女孩温和坚定地走到男孩身边安慰他'),
    ]
    y = 3.55
    for label, color, content in shots:
        ax.add_patch(FancyBboxPatch((0.55, y), 10.9, 1.15,
                                    boxstyle='round,pad=0.05,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(0.85, y + 0.75, label, fontsize=11, fontweight='bold',
                color=color, ha='left')
        ax.text(0.85, y + 0.35, content, fontsize=10.5, color=TEXT,
                ha='left')
        y -= 1.3

    ax.text(6, 0.75, '想一镜到底：中文写"生成单镜头"，英文写"Generate single shot."',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'multi_shot.png')


if __name__ == '__main__':
    draw_modes(); draw_formulas(); draw_sound(); draw_multi_shot()
    print('done')
