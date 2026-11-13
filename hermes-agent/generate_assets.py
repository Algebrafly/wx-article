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

BG = '#0b1613'
PANEL = '#132420'
TEXT = '#e8f5ee'
DIM = '#7fa196'
EMERALD = '#34d399'
AMBER = '#fbbf24'
SKY = '#38bdf8'
ROSE = '#fb7185'
GRID = '#2a423a'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：学习闭环 ───────────────────────────────────────────────────────
def draw_loop():
    fig, ax = plt.subplots(figsize=(11, 8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 11); ax.set_ylim(0, 8); ax.axis('off')

    ax.text(5.5, 7.55, 'Hermes 的学习闭环', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(5.5, 7.05, '每次干完活，它都比上一次强一点', fontsize=12.5, color=DIM, ha='center')

    steps = [
        ('干活', '用工具完成任务', EMERALD),
        ('记事', '把关键信息写进记忆', SKY),
        ('提技能', '从经验里抽出 SKILL.md', AMBER),
        ('跨会话召回', '下次直接调出来用', ROSE),
    ]

    cx, cy = 5.5, 4.3
    w, h = 3.0, 1.15
    positions = [(cx - 3.5, cy + 0.75), (cx + 0.5, cy + 0.75),
                 (cx + 0.5, cy - 1.6), (cx - 3.5, cy - 1.6)]
    for (label, desc, color), (x, y) in zip(steps, positions):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.06,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=2.2))
        ax.text(x + w/2, y + h - 0.35, label, fontsize=14, fontweight='bold',
                color=color, ha='center', va='center')
        ax.text(x + w/2, y + 0.35, desc, fontsize=9.5, color=DIM, ha='center', va='center')

    ar = dict(arrowstyle='-|>', color=GRID, lw=2, mutation_scale=16)
    ax.add_patch(FancyArrowPatch((positions[0][0] + w, cy + 0.75 + h/2),
                                 (positions[1][0], cy + 0.75 + h/2), **ar))
    ax.add_patch(FancyArrowPatch((positions[1][0] + w/2, positions[1][1]),
                                 (positions[2][0] + w/2, positions[2][1] + h), **ar))
    ax.add_patch(FancyArrowPatch((positions[2][0], positions[2][1] + h/2),
                                 (positions[3][0] + w, positions[3][1] + h/2), **ar))
    ax.add_patch(FancyArrowPatch((positions[3][0] + w/2, positions[3][1] + h),
                                 (positions[0][0] + w/2, positions[0][1]), **ar))

    ax.text(5.5, 1.05, '没有这一步，「自我进化」就只是宣传语；有了这一步，它才会越用越顺手。',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'loop.png')


# ── 2：三层结构 ───────────────────────────────────────────────────────
def draw_layers():
    fig, ax = plt.subplots(figsize=(12, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6, 6.9, 'Hermes 的三层结构', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.4, '模型、能力、入口各自独立，可以随便换', fontsize=12.5, color=DIM, ha='center')

    layers = [
        ('模型层', '三十多个供应商，任何 OpenAI 兼容端点\n硬门槛：上下文 ≥ 64K', EMERALD,
         ['Nous Portal', 'Anthropic', 'OpenRouter', 'DeepSeek']),
        ('能力层', '工具 / 技能 / 记忆 / MCP / 子代理\n60+ 内置工具，按需加载', AMBER,
         ['Tools', 'Skills', 'Memory', 'MCP']),
        ('接入层', '一个 gateway，二十多个平台\nCLI 和聊天软件共用同一套会话', SKY,
         ['CLI / TUI', 'Telegram', '飞书 / 企微', 'ACP']),
    ]

    def tag_w(s):
        wide = sum(2 if ord(c) > 127 else 1 for c in s)
        return wide * 0.115 + 0.42

    y = 4.85
    for title, desc, color, tags in layers:
        ax.add_patch(FancyBboxPatch((0.6, y), 10.8, 1.45,
                                    boxstyle='round,pad=0.06,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(0.95, y + 1.0, title, fontsize=13, fontweight='bold', color=color, ha='left')
        ax.text(0.95, y + 0.42, desc, fontsize=9.5, color=DIM, ha='left', linespacing=1.4)
        tx = 4.85
        for tag in tags:
            tw = tag_w(tag)
            ax.add_patch(FancyBboxPatch((tx, y + 0.42), tw, 0.42,
                                        boxstyle='round,pad=0.03,rounding_size=0.08',
                                        facecolor='#0b1613', edgecolor=GRID, linewidth=1))
            ax.text(tx + tw/2, y + 0.63, tag, fontsize=8.5, color=TEXT, ha='center', va='center')
            tx += tw + 0.16
        y -= 1.7

    ax.text(6, 0.75, '换模型不用重装，换入口不用改配置。这三层是解耦的。',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'layers.png')


# ── 3：安装三条路 ───────────────────────────────────────────────────────
def draw_install():
    fig, ax = plt.subplots(figsize=(12, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6, 6.9, '三条安装路径', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.4, '桌面版最省事，命令行版最轻', fontsize=12.5, color=DIM, ha='center')

    paths = [
        ('A', '桌面安装包', 'macOS / Windows\n下载 DMG 或 MSIX 直接装\nCLI 和 GUI 一起搞定', EMERALD),
        ('B', 'Unix 一行命令', 'Linux / macOS / WSL2 / Termux', SKY),
        ('C', 'Windows 原生', 'PowerShell 里执行', AMBER),
    ]

    # A：宽卡片（上）
    ax.add_patch(FancyBboxPatch((0.6, 4.55), 10.8, 1.4,
                                boxstyle='round,pad=0.06,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=EMERALD, linewidth=2))
    ax.text(1.0, 5.45, 'A  桌面安装包', fontsize=13, fontweight='bold', color=EMERALD, ha='left')
    ax.text(1.0, 4.95, 'macOS / Windows，下载后双击。CLI 和图形界面一起装好，官方推荐。',
            fontsize=10.5, color=TEXT, ha='left')

    # B：代码卡
    ax.add_patch(FancyBboxPatch((0.6, 2.6), 5.25, 1.7,
                                boxstyle='round,pad=0.06,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=SKY, linewidth=2))
    ax.text(0.9, 3.95, 'B  Unix 一行命令', fontsize=12, fontweight='bold', color=SKY, ha='left')
    ax.text(0.9, 3.55, 'Linux / macOS / WSL2 / Termux', fontsize=9, color=DIM, ha='left')
    ax.text(0.9, 3.0, 'curl -fsSL\nhttps://hermes-agent.nousresearch.com/install.sh | bash',
            fontsize=8.5, color=TEXT, ha='left', va='center', linespacing=1.6)

    # C：代码卡
    ax.add_patch(FancyBboxPatch((6.15, 2.6), 5.25, 1.7,
                                boxstyle='round,pad=0.06,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=AMBER, linewidth=2))
    ax.text(6.45, 3.95, 'C  Windows 原生', fontsize=12, fontweight='bold', color=AMBER, ha='left')
    ax.text(6.45, 3.55, 'PowerShell', fontsize=9, color=DIM, ha='left')
    ax.text(6.45, 3.0, 'iex (irm\nhttps://hermes-agent.nousresearch.com/install.ps1)',
            fontsize=8.5, color=TEXT, ha='left', va='center', linespacing=1.6)

    # 验证三步
    ax.text(6, 2.15, '装完之后，三步验证', fontsize=11, fontweight='bold',
            color=DIM, ha='center')
    steps = [('1', 'hermes setup --portal', '一次 OAuth 配好模型和工具'),
             ('2', 'hermes --tui', '进 TUI，问一句能答话的问题'),
             ('3', 'hermes --continue', '确认会话能恢复')]
    sx = 0.6
    for num, cmd, note in steps:
        ax.add_patch(FancyBboxPatch((sx, 0.5), 3.45, 1.35,
                                    boxstyle='round,pad=0.05,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=GRID, linewidth=1.2))
        ax.text(sx + 0.25, 1.55, num, fontsize=14, fontweight='bold', color=EMERALD, ha='left')
        ax.text(sx + 0.65, 1.55, cmd, fontsize=8.5, color=TEXT, ha='left')
        ax.text(sx + 0.25, 0.85, note, fontsize=8.5, color=DIM, ha='left')
        sx += 3.62

    save(fig, 'install.png')


# ── 4：命令地图 ─────────────────────────────────────────────────────────
def draw_commands():
    fig, ax = plt.subplots(figsize=(12, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6, 6.7, '日常会用到的命令', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.2, '斜杠命令在 CLI 和聊天软件里通用', fontsize=12.5, color=DIM, ha='center')

    groups = [
        ('配置', ['hermes setup', 'hermes model', 'hermes config set', 'hermes tools'], EMERALD),
        ('技能', ['hermes skills browse', 'hermes skills search', 'hermes skills install'], AMBER),
        ('接入', ['hermes gateway setup', 'hermes acp', 'hermes --tui'], SKY),
    ]
    y = 4.75
    for title, cmds, color in groups:
        ax.add_patch(FancyBboxPatch((0.6, y), 2.1, 1.15,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.65, y + 0.575, title, fontsize=12.5, fontweight='bold',
                color=BG, ha='center', va='center')
        cx = 2.95
        for cmd in cmds:
            cw = len(cmd) * 0.085 + 0.42
            ax.add_patch(FancyBboxPatch((cx, y + 0.24), cw, 0.68,
                                        boxstyle='round,pad=0.04,rounding_size=0.1',
                                        facecolor=PANEL, edgecolor=color, linewidth=1.2))
            ax.text(cx + cw/2, y + 0.58, cmd, fontsize=8.5, color=TEXT,
                    ha='center', va='center')
            cx += cw + 0.15
        y -= 1.45

    ax.text(6, 0.6, '内置技能装好之后会自动变成一个斜杠命令，比如 /k8s 就能直接跑。',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'commands.png')


if __name__ == '__main__':
    draw_loop(); draw_layers(); draw_install(); draw_commands()
    print('done')
