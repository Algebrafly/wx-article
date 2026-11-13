#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes 项目管理系列 · 统一封面与目录页"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0d1117'
PANEL = '#161b22'
CARD = '#1c2430'
LINE = '#2d3846'
TEXT = '#e6edf3'
DIM = '#8b98a8'

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(OUT, exist_ok=True)

SERIES = [
    ('01', '整体框架', '把项目经理拆成三层来配', '#22d3ee'),
    ('02', '范围管理', '把范围写成事实', '#fb7185'),
    ('03', '进度管理', '估得准，盯得早', '#34d399'),
    ('04', '成本管理', '花得值不值', '#e8b04b'),
    ('05', '质量管理', '把「算不算完成」钉死', '#f472b6'),
    ('06', '资源管理', '人不是可分配的单位', '#a3e635'),
    ('07', '沟通管理', '把没说出口的放到台面上', '#60a5fa'),
    ('08', '风险管理', '登记册为什么会死', '#fbbf24'),
    ('09', '采购管理', '合同就是一张风险分配表', '#f97316'),
    ('10', '干系人管理', '名单之外的人才是变量', '#c084fc'),
    ('11', '整合管理', '十个领域打架时听谁的', '#2dd4bf'),
]


def canvas(w, h):
    fig = plt.figure(figsize=(w, h), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 13)
    ax.set_ylim(0, h)
    ax.axis('off')
    ax.set_facecolor(BG)
    return fig, ax


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.14)
    plt.close(fig)
    print(f'✓ {name}')


# ── 系列封面 ───────────────────────────────────────────────────────────
def cover():
    h = 5.5
    fig, ax = canvas(13, h)

    ax.plot([0.0, 13.0], [h - 0.06, h - 0.06], color='#1f2937', lw=0)
    ax.text(6.5, 4.42, '用 Hermes 做项目管理', fontsize=33, fontweight='bold',
            color=TEXT, ha='center', va='center')
    ax.text(6.5, 3.88, '十大领域 · 十一个过程组 · 一套可落地的 SKILL',
            fontsize=13.5, color='#22d3ee', ha='center', va='center')

    ax.plot([4.1, 8.9], [3.56, 3.56], color='#2d3846', lw=1.2)
    ax.text(6.5, 3.28, '从章程到归档，让十个领域的数字能互相对上',
            fontsize=11.5, color=DIM, ha='center', va='center')

    cw, ch, gx, gy = 2.72, 0.56, 0.18, 0.11
    total = 4 * cw + 3 * gx
    x0 = (13 - total) / 2
    for i, (num, name, tag, c) in enumerate(SERIES):
        row = 0 if i < 4 else (1 if i < 8 else 2)
        col = i - row * 4
        ncol = 4 if row < 2 else 3
        rowx0 = (13 - (ncol * cw + (ncol - 1) * gx)) / 2
        x = rowx0 + col * (cw + gx)
        y = 2.42 - row * (ch + gy)
        ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                    boxstyle='round,pad=0.03,rounding_size=0.10',
                                    facecolor=CARD, edgecolor=c + '60', linewidth=1.1))
        ax.text(x + 0.17, y + ch / 2, num, fontsize=8.4, fontweight='bold',
                color=c, ha='left', va='center')
        ax.text(x + 0.66, y + ch / 2, name, fontsize=8.8, color='#cdd8e4',
                ha='left', va='center')

    ax.text(6.5, 0.52, '输入 · 技术 · 输出 → 六份文档模板 → 组织过程资产 → 群消息格式',
            fontsize=9.2, color='#5f6d7e', ha='center', va='center')
    save(fig, 'series-cover.png')


# ── 系列目录页 ─────────────────────────────────────────────────────────
def toc():
    h = 10.4
    fig, ax = canvas(13, h)

    ax.text(6.5, 9.95, '系列目录 · 十一篇', fontsize=22, fontweight='bold',
            color=TEXT, ha='center', va='center')
    ax.text(6.5, 9.52, '每一篇都是同一个结构：过程 ITTO、两到三个重点、文档模板、归档、群消息、边界',
            fontsize=9.6, color=DIM, ha='center', va='center')

    x0 = 0.55
    ws = [0.95, 2.45, 5.85, 2.75]
    heads = ['', '领域', '这一篇在说什么', '关键产出']
    ytop = 9.12

    hx = x0
    for c, w in zip(heads, ws):
        if c:
            ax.text(hx + 0.14, ytop - 0.24, c, fontsize=8.0, fontweight='bold',
                    color='#22d3ee', ha='left', va='center')
        hx += w
    ax.plot([x0, x0 + sum(ws)], [ytop - 0.44, ytop - 0.44], color='#334155', lw=1)

    outs = ['框架与 Profile', '需求跟踪矩阵', 'PERT 与 CPM', 'EVM 与 EAC',
            'COQ 与控制图', '负荷与产能', '沟通漏斗', '5×5 矩阵',
            '合同风险谱', '四象限与信号', '变更分级与收尾']

    y = ytop - 0.44
    for i, (num, name, tag, c) in enumerate(SERIES):
        rh = 0.62
        ax.add_patch(FancyBboxPatch((x0, y - rh), sum(ws), rh,
                                    boxstyle='round,pad=0.02,rounding_size=0.05',
                                    facecolor=CARD if i % 2 == 0 else PANEL,
                                    edgecolor='none'))
        ax.text(x0 + 0.30, y - rh / 2, num, fontsize=9.4, fontweight='bold',
                color=c, ha='center', va='center')
        ax.text(x0 + ws[0] + 0.14, y - rh / 2, name, fontsize=9.2,
                fontweight='bold', color='#e6edf3', ha='left', va='center')
        ax.text(x0 + ws[0] + ws[1] + 0.14, y - rh / 2, tag, fontsize=8.6,
                color='#a8b6c6', ha='left', va='center')
        ax.text(x0 + ws[0] + ws[1] + ws[2] + 0.14, y - rh / 2, outs[i],
                fontsize=8.2, color=c, ha='left', va='center')
        y -= rh + 0.045

    ax.text(6.5, 0.85, '统一主键、统一口径、统一模板——这是让交叉比对成立的前提',
            fontsize=9.6, color='#fbbf24', ha='center', va='center')
    ax.text(6.5, 0.45, '十个领域各自做得再精细，如果数字对不上，最后仍然只能靠开会吵架来决策',
            fontsize=8.6, color=DIM, ha='center', va='center')
    save(fig, 'series-toc.png')


if __name__ == '__main__':
    cover()
    toc()
    print('✓ 全部生成完毕')
