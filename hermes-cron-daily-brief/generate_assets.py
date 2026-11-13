#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#101828'
PANEL = '#1d2939'
CARD = '#243244'
TEXT = '#e4e7ec'
DIM = '#667085'
INDIGO = '#818cf8'
TEAL = '#2dd4bf'
AMBER = '#fbbf24'
CORAL = '#fb7185'
GREEN = '#34d399'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：四层架构 ───────────────────────────────────────────────────────────
def draw_arch():
    fig, ax = plt.subplots(figsize=(13, 8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis('off')

    ax.text(6.5, 7.5, '四层架构：采集 · 归一 · 渲染 · 投递', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.0, '每一层都是独立脚本，可单独跑、单独改、单独排错', fontsize=12, color=DIM, ha='center')

    layers = [
        (6.05, '采集层', 'collect_status.py', INDIGO,
         ['Jira', '禅道', 'PingCode', '云效']),
        (4.55, '归一化层', 'status_normalize.py', AMBER,
         ['todo', 'doing', 'done', 'closed', 'blocked']),
        (3.05, '聚合渲染层', 'render_daily.py', TEAL,
         ['按项目分组', '按人统计', '对比昨日快照']),
        (1.55, '投递层', 'webhook 路由', GREEN,
         ['项目群 A', '项目群 B', '项目群 C']),
    ]

    for y, name, script, color, chips in layers:
        # left label
        ax.add_patch(FancyBboxPatch((0.45, y - 0.5), 2.05, 1.0,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.475, y + 0.12, name, fontsize=13, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(1.475, y - 0.26, script, fontsize=7.5, color=BG,
                ha='center', va='center', alpha=0.78)

        # right body
        ax.add_patch(FancyBboxPatch((2.7, y - 0.5), 9.75, 1.0,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        # chips
        n = len(chips)
        cw = 1.75
        total = cw * n + 0.12 * (n - 1)
        x0 = 2.9 + (9.35 - total) / 2
        for i, c in enumerate(chips):
            cx = x0 + i * (cw + 0.12)
            ax.add_patch(FancyBboxPatch((cx, y - 0.28), cw, 0.56,
                                        boxstyle='round,pad=0.03,rounding_size=0.12',
                                        facecolor=CARD, edgecolor=color, linewidth=1))
            ax.text(cx + cw / 2, y, c, fontsize=9.5, color=TEXT, ha='center', va='center')

    # arrows：只画在层与层的间隙里，避免压住卡片
    for y_top, y_bottom in [(5.55, 5.05), (4.05, 3.55), (2.55, 2.05)]:
        ax.annotate('', xy=(6.5, y_bottom), xytext=(6.5, y_top),
                    arrowprops=dict(arrowstyle='->', color=DIM, lw=1.6))

    ax.text(6.5, 0.55, '前三层跑在 cron 里，第四层是脚本内自己发 webhook',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'arch.png')


# ── 2：四平台状态码映射矩阵 ────────────────────────────────────────────────
def draw_status_map():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 6.9, '四套状态码，对齐成五个枚举', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.4, '不按状态名匹配，按平台给的"状态分类"匹配 —— 这是能长期跑稳的关键',
            fontsize=11.5, color=DIM, ha='center')

    cols = ['Jira', '禅道', 'PingCode', '云效']
    col_colors = [INDIGO, AMBER, TEAL, CORAL]
    rows = [
        ('todo 未开始', ['To Do (new)', 'wait 未开始', 'unstarted', '待处理'], '#94a3b8'),
        ('doing 进行中', ['In Progress', 'doing 进行中', 'started', '处理中'], '#60a5fa'),
        ('done 已完成', ['Done (done)', 'done 已完成', 'completed', '已完成'], GREEN),
        ('closed 已关闭', ['Closed', 'closed 已关闭', 'closed', '已关闭'], '#a78bfa'),
        ('blocked 阻塞', ['Blocked 标签', 'pause 已挂起', '— 无此态', '已阻塞'], '#f87171'),
    ]

    x_start = 2.35
    cw = 2.55
    gap = 0.14
    y_header = 5.55
    row_h = 0.88

    # header
    for i, (c, color) in enumerate(zip(cols, col_colors)):
        x = x_start + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, y_header), cw, 0.55,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + cw / 2, y_header + 0.275, c, fontsize=12.5, fontweight='bold',
                color=BG, ha='center', va='center')

    # rows
    y = y_header - 0.75
    for label, cells, color in rows:
        # left label
        ax.add_patch(FancyBboxPatch((0.5, y - 0.36), 1.7, 0.72,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.35, y, label, fontsize=10, fontweight='bold',
                color=BG, ha='center', va='center')
        for i, cell in enumerate(cells):
            x = x_start + i * (cw + gap)
            ax.add_patch(FancyBboxPatch((x, y - 0.36), cw, 0.72,
                                        boxstyle='round,pad=0.03,rounding_size=0.08',
                                        facecolor=PANEL, edgecolor='#344054', linewidth=1))
            ax.text(x + cw / 2, y, cell, fontsize=9, color=TEXT, ha='center', va='center')
        y -= row_h

    ax.text(6.5, 0.5, '映射表写死在 config 里，平台加字段只改一行',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'status_map.png')


# ── 3：群消息卡片 mockup ──────────────────────────────────────────────────
def draw_card():
    fig, ax = plt.subplots(figsize=(13, 8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis('off')

    ax.text(6.5, 7.5, '业务群里长这样：一个项目一屏', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.0, '企微 markdown 消息，4096 字节硬上限，所以按项目拆条发', fontsize=11.5,
            color=DIM, ha='center')

    # card frame
    ax.add_patch(FancyBboxPatch((2.0, 0.55), 9.0, 5.85,
                                boxstyle='round,pad=0.05,rounding_size=0.16',
                                facecolor='#ffffff', edgecolor='#e4e7ec', linewidth=1.2))

    # bot avatar + name
    ax.add_patch(plt.Circle((2.55, 5.95), 0.24, facecolor=INDIGO, edgecolor='none'))
    ax.text(2.55, 5.95, 'H', fontsize=12, fontweight='bold', color='#ffffff',
            ha='center', va='center')
    ax.text(2.92, 6.02, 'Hermes 日报', fontsize=9.5, fontweight='bold', color='#344054', ha='left')
    ax.text(2.92, 5.79, '今天 09:00', fontsize=8, color='#98a2b3', ha='left')

    # title line
    ax.text(2.35, 5.32, '支付平台 · 2026-11-03', fontsize=14, fontweight='bold',
            color='#101828', ha='left')
    ax.plot([2.35, 10.65], [5.13, 5.13], color='#e4e7ec', lw=1.2)

    # summary chips
    chips = [('进行中 9', '#eff8ff', '#175cd3'),
             ('已完成 17', '#ecfdf3', '#027a48'),
             ('阻塞 2', '#fef3f2', '#b42318')]
    x = 2.35
    for label, bgc, fgc in chips:
        ax.add_patch(FancyBboxPatch((x, 4.55), 1.45, 0.42,
                                    boxstyle='round,pad=0.03,rounding_size=0.12',
                                    facecolor=bgc, edgecolor='none', linewidth=0))
        ax.text(x + 0.725, 4.76, label, fontsize=8.5, fontweight='bold', color=fgc,
                ha='center', va='center')
        x += 1.6

    # per-person table header
    ax.text(2.35, 4.12, '按人统计', fontsize=9, fontweight='bold', color='#344054', ha='left')
    ax.plot([2.35, 10.65], [3.98, 3.98], color='#e4e7ec', lw=1)

    headers = [('姓名', 2.35), ('进行中', 5.0), ('已完成', 6.6), ('阻塞', 8.2), ('超期', 9.65)]
    for h, hx in headers:
        ax.text(hx, 3.78, h, fontsize=8, fontweight='bold', color='#667085', ha='left')

    people = [
        ('张三', '2', '6', '0', '1'),
        ('李四', '3', '5', '1', '0'),
        ('王五', '4', '6', '1', '0'),
    ]
    y = 3.42
    for p in people:
        for i, val in enumerate(p):
            color = '#b42318' if (i == 4 and val != '0') else '#344054'
            weight = 'bold' if (i == 4 and val != '0') else 'regular'
            ax.text([2.35, 5.0, 6.6, 8.2, 9.65][i], y, val, fontsize=8.5,
                    color=color, fontweight=weight, ha='left')
        y -= 0.42

    ax.plot([2.35, 10.65], [2.28, 2.28], color='#e4e7ec', lw=1)

    # changes section
    ax.text(2.35, 2.05, '今日变更 3 条', fontsize=9, fontweight='bold', color='#344054', ha='left')
    changes = [
        ('+', 'PAY-3412 代扣重试上线，状态 → 已完成', '#027a48'),
        ('!', 'PAY-3420 对账任务超期 2 天，负责人已变更', '#b42318'),
        ('+', 'PAY-3433 新增需求：支持分账到子商户', '#175cd3'),
    ]
    cy = 1.68
    for mark, txt, color in changes:
        ax.text(2.42, cy, mark, fontsize=10, fontweight='bold', color=color, ha='left')
        ax.text(2.72, cy, txt, fontsize=8.5, color='#344054', ha='left')
        cy -= 0.38

    ax.text(6.5, 0.2, '卡片右上角永远带一个「查看全部」链接',
            fontsize=9, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'report_card.png')


# ── 4：路由表 + 投递机制 ──────────────────────────────────────────────────
def draw_routing():
    fig, ax = plt.subplots(figsize=(13, 7), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis('off')

    ax.text(6.5, 6.55, '一个项目一个群，各看各的', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.05, '路由表写在一个 YAML 里，加项目只加一行', fontsize=12, color=DIM, ha='center')

    # left: unified json
    ax.add_patch(FancyBboxPatch((0.5, 2.5), 3.3, 3.0,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=INDIGO, linewidth=1.8))
    ax.text(2.15, 5.2, 'status.json', fontsize=12, fontweight='bold',
            color=INDIGO, ha='center', va='center')
    ax.text(2.15, 4.55, 'projects[]', fontsize=9, color=TEXT, ha='center', va='center',
            linespacing=1.6)
    ax.text(2.15, 4.0, '   key / name', fontsize=8, color=DIM, ha='center', va='center')
    ax.text(2.15, 3.7, '   platform', fontsize=8, color=DIM, ha='center', va='center')
    ax.text(2.15, 3.4, '   members[]', fontsize=8, color=DIM, ha='center', va='center')
    ax.text(2.15, 3.1, '   changes[]', fontsize=8, color=DIM, ha='center', va='center')

    # middle: router
    ax.add_patch(FancyBboxPatch((4.55, 3.6), 2.3, 1.3,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=AMBER, linewidth=2))
    ax.text(5.7, 4.45, '路由表', fontsize=12, fontweight='bold', color=AMBER,
            ha='center', va='center')
    ax.text(5.7, 4.0, 'project → webhook', fontsize=8, color=DIM, ha='center', va='center')

    ax.annotate('', xy=(4.5, 4.25), xytext=(3.85, 4.25),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.6))

    # right: three groups
    groups = [
        (5.05, '支付项目群', 'WECOM_WEBHOOK_PAY', GREEN),
        (3.85, '订单项目群', 'FEISHU_WEBHOOK_ORDER', TEAL),
        (2.65, '基础架构群', 'WECOM_WEBHOOK_INFRA', CORAL),
    ]
    for gy, name, env, color in groups:
        ax.add_patch(FancyBboxPatch((8.0, gy - 0.45), 4.3, 0.9,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(8.25, gy + 0.14, name, fontsize=10, fontweight='bold', color=TEXT, ha='left')
        ax.text(8.25, gy - 0.19, env, fontsize=8, color=color, ha='left', fontfamily='monospace')
        ax.annotate('', xy=(7.95, gy), xytext=(6.9, 4.25),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.3,
                                    connectionstyle='arc3,rad=0.06'))

    ax.text(6.5, 1.55, '同一个 JSON，三份不同的卡片 —— 内容互不串台',
            fontsize=10, color=DIM, ha='center', va='center')
    ax.add_patch(FancyBboxPatch((3.6, 0.55), 5.8, 0.72,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 0.91, '无变更 → 本轮不发  |  有变更 → 只发有变更的项目',
            fontsize=9, color=TEXT, ha='center', va='center')

    save(fig, 'routing.png')


if __name__ == '__main__':
    draw_arch(); draw_status_map(); draw_card(); draw_routing()
    print('done')
