#!/usr/bin/env python3
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#12100e'
PANEL = '#1d1916'
TEXT = '#ece7e1'
DIM = '#9b938c'
O = '#e07856'
A = '#f0b429'
T = '#58c4a0'
P = '#9b8bd8'
GRID = '#2d2823'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：核心闭环 ───────────────────────────────────────────────────────────
def draw_loop():
    fig, ax = plt.subplots(figsize=(11, 8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 11); ax.set_ylim(0, 8); ax.axis('off')

    ax.text(5.5, 7.5, 'ECC 的七步闭环', fontsize=23, fontweight='bold', color=TEXT, ha='center')
    ax.text(5.5, 6.95, 'plan → test → implement → review → verify → remember → improve',
            fontsize=12, color=DIM, ha='center')

    steps = [
        ('plan', O), ('test', A), ('implement', T), ('review', P),
        ('verify', O), ('remember', A), ('improve', T),
    ]

    cx, cy, r = 5.5, 3.7, 2.05
    n = len(steps)
    for i, (name, color) in enumerate(steps):
        ang = math.pi / 2 - i * (2 * math.pi / n)
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        ax.add_patch(Circle((x, y), 0.52, facecolor=PANEL, edgecolor=color,
                            linewidth=2.2, zorder=5))
        fs = 9.5 if len(name) > 6 else 11
        ax.text(x, y, name, fontsize=fs, fontweight='bold', color=color,
                ha='center', va='center', zorder=6)

    ax.text(cx, cy + 0.22, 'ECC', fontsize=26, fontweight='bold', color=TEXT,
            ha='center', va='center')
    ax.text(cx, cy - 0.35, 'agent harness\noperating system', fontsize=9.5, color=DIM,
            ha='center', va='center', linespacing=1.5)

    ax.add_patch(plt.Circle((cx, cy), r, fill=False, color=GRID, linewidth=1.5,
                            linestyle='--'))
    ax.add_patch(plt.Circle((cx, cy), 0.95, fill=False, color=GRID, linewidth=1,
                            linestyle=':'))

    ax.text(5.5, 0.5, '整套流程装在 harness 里，不用在每条 prompt 里重写一遍。',
            fontsize=10.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'loop.png')


# ── 2：仓库里到底有什么 ───────────────────────────────────────────────────
def draw_inventory():
    fig, ax = plt.subplots(figsize=(12, 6.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.2); ax.axis('off')

    ax.text(6, 5.75, '仓库里到底有什么', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6, 5.2, '71 个 agent、311 个 skill、97 条命令，加上运行时钩子与规则',
            fontsize=12.5, color=DIM, ha='center')

    cards = [
        ('71', 'agents', '规划、复审、编译修复、\n安全、架构、领域专用', O),
        ('311', 'skills', 'TDD、研究、安全、文档、\n前端、数据、ML、运维', A),
        ('97', 'commands', '正在迁向 skill-first，\n命令保留为入口与兼容层', T),
        ('6', '组件层', 'hooks · rules · memory\n· learning · AgentShield', P),
    ]

    w = 2.6; gap = 0.28
    total = len(cards) * w + (len(cards) - 1) * gap
    x = (12 - total) / 2
    for num, label, desc, color in cards:
        ax.add_patch(FancyBboxPatch((x, 1.6), w, 3.0,
                                    boxstyle='round,pad=0.05,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + w/2, 3.95, num, fontsize=34, fontweight='bold', color=color,
                ha='center', va='center')
        ax.text(x + w/2, 3.15, label, fontsize=12, fontweight='bold', color=TEXT,
                ha='center', va='center')
        ax.text(x + w/2, 2.35, desc, fontsize=8.5, color=DIM,
                ha='center', va='center', linespacing=1.5)
        x += w + gap

    ax.text(6, 0.9, 'AgentShield 单独扫 prompts / hooks / MCP 配置 / 权限 / 密钥 / agent 文件。',
            fontsize=10, color=DIM, ha='center', va='center')

    save(fig, 'inventory.png')


# ── 3：四个核心概念 ───────────────────────────────────────────────────────
def draw_concepts():
    fig, ax = plt.subplots(figsize=(12, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6, 7.2, 'Agent、Skill、Hook、Rule', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.7, '四种东西，四种触发方式', fontsize=12.5, color=DIM, ha='center')

    items = [
        ('Agent', '被派活', '独立 subagent，限定 scope 和 tools。\nfrontmatter 写 name / tools / model，\n正文写「你是谁、怎么干」。', O, 'code-reviewer / planner / architect'),
        ('Skill', '按需加载', '可复用的工作流定义，正文就是步骤。\n主入口。可以直接调，也能被 agent 用。', A, 'tdd-workflow / security-review'),
        ('Hook', '事件触发', '挂在 tool 事件上，PreToolUse / PostToolUse\n/ Stop。命中就执行 shell，能拦也能提醒。', T, '编辑 ts 文件时警告 console.log'),
        ('Rule', '常驻', '始终加载的规范，按语言分目录。\ncommon + 你实际用的那一个语言包。', P, 'coding-style / testing / security'),
    ]

    for i, (name, trig, desc, color, ex) in enumerate(items):
        col = i % 2; row = i // 2
        x = 0.6 + col * 5.75
        y = 5.05 - row * 2.5
        ax.add_patch(FancyBboxPatch((x, y - 2.1), 5.35, 2.1,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.3, y - 0.34, name, fontsize=15, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(x + 5.05, y - 0.34, trig, fontsize=9, color=color, ha='right', va='center',
                bbox=dict(boxstyle='round,pad=0.32', facecolor=BG, edgecolor=color, linewidth=1))
        ax.text(x + 0.3, y - 0.97, desc, fontsize=9, color=TEXT, ha='left', va='center',
                linespacing=1.6)
        ax.text(x + 0.3, y - 1.75, ex, fontsize=8.5, color=DIM, ha='left', va='center',
                style='italic')

    save(fig, 'concepts.png')


# ── 4：安装与 harness 支持 ────────────────────────────────────────────────
def draw_install():
    fig, ax = plt.subplots(figsize=(12.5, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12.5); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.25, 6.8, '一个插件，七个 harness', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.25, 6.3, '原生支持 / 能力受限适配，差别不小', fontsize=12.5, color=DIM, ha='center')

    # 左：安装命令
    ax.add_patch(FancyBboxPatch((0.5, 1.1), 5.6, 4.6,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=O, linewidth=2))
    ax.text(0.85, 5.25, '装法（选一条，别叠加）', fontsize=12, fontweight='bold',
            color=O, ha='left', va='center')

    lines = [
        ('npx ecc-universal@2.2.3 setup', O),
        ('', None),
        ('/plugin marketplace add', A),
        ('  https://github.com/affaan-m/ECC', A),
        ('/plugin install ecc@ecc', A),
        ('', None),
        ('npx ecc-universal@2.2.3 \\', T),
        ('  install --guided', T),
    ]
    y = 4.65
    for txt, color in lines:
        ax.text(0.85, y, txt, fontsize=8.5, color=color if color else TEXT,
                ha='left', va='center', fontfamily='monospace')
        y -= 0.32

    ax.text(0.85, 1.5, '引导式 / 原生插件 / 多 harness 向导，\n三条路最后装的都是同一个 ecc@ecc。',
            fontsize=8.5, color=DIM, ha='left', va='center', linespacing=1.6)

    # 右：harness 矩阵
    ax.text(7.0, 5.25, 'harness 支持度', fontsize=12, fontweight='bold',
            color=T, ha='left', va='center')

    rows = [
        ('Claude Code', '原生插件', O),
        ('Codex', '原生插件', O),
        ('Qoder', '原生插件', O),
        ('Cursor', '受限适配', A),
        ('OpenCode', '受限适配', A),
        ('Gemini CLI', '受限适配', A),
        ('Zed / Copilot / Kimi', '受限适配', A),
    ]
    y = 4.7
    for name, level, color in rows:
        ax.text(7.0, y, name, fontsize=9.5, color=TEXT, ha='left', va='center')
        ax.text(10.85, y, level, fontsize=8.5, color=color, ha='right', va='center')
        ax.plot([7.0, 10.85], [y - 0.19, y - 0.19], color=GRID, lw=0.6)
        y -= 0.45

    ax.text(7.0, 1.55, '受限适配意味着 skill 能用，\n但 hook 运行时和原生 skill 发现不一定齐。',
            fontsize=8.5, color=DIM, ha='left', va='center', linespacing=1.6)

    save(fig, 'install.png')


if __name__ == '__main__':
    draw_loop(); draw_inventory(); draw_concepts(); draw_install()
    print('done')
