#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0d1b16'
PANEL = '#152a22'
CARD = '#1e3a2f'
TEXT = '#e7f2ec'
DIM = '#6b8c7d'
MINT = '#5eead4'
LIME = '#a3e635'
AMBER = '#fbbf24'
CORAL = '#fb7185'
SKY = '#7dd3fc'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：从只读账号到 HTML 看板 ───────────────────────────────────────────────
def draw_flow():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.15, '没有报表服务，看板照样每天准时到', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.7, '五段全自动，只有第一段需要人配一次', fontsize=12, color=DIM, ha='center')

    steps = [
        ('只读账号', 'SELECT only\n指定 schema', MINT, '配一次，长期用'),
        ('语义层', '表 · 指标 · 同义词', LIME, '让 GMV 只有一个定义'),
        ('取数', 'NL → SQL → 执行', AMBER, '五道校验后才放行'),
        ('渲染', 'HTML + ECharts', CORAL, '单文件，可版本化'),
        ('分发', '群 / 网盘 / 门户', SKY, '链接 + 摘要'),
    ]

    w = 2.2; h = 2.35; gap = 0.28
    total = w * 5 + gap * 4
    x0 = (13 - total) / 2
    yc = 3.5

    for i, (title, desc, color, note) in enumerate(steps):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.add_patch(plt.Circle((x + w / 2, yc + h / 2 - 0.32), 0.19,
                                facecolor=color, edgecolor='none', zorder=4))
        ax.text(x + w / 2, yc + h / 2 - 0.32, str(i + 1), fontsize=11, fontweight='bold',
                color=BG, ha='center', va='center', zorder=5)
        ax.text(x + w / 2, yc + 0.5, title, fontsize=13, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(x + w / 2, yc - 0.22, desc, fontsize=8.6, color=color,
                ha='center', va='center', linespacing=1.55)
        ax.text(x + w / 2, yc - 0.92, note, fontsize=7.5, color=DIM,
                ha='center', va='center')
        if i < 4:
            ax.annotate('', xy=(x + w + gap - 0.015, yc), xytext=(x + w + 0.015, yc),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))

    ax.add_patch(FancyBboxPatch((2.2, 0.7), 8.6, 0.7,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 1.05, '日 / 周 / 月 / 季 / 年 五套定时，加一个随时可问的入口',
            fontsize=9.5, color=TEXT, ha='center', va='center')

    save(fig, 'flow.png')


# ── 2：SQL 安全链路 ─────────────────────────────────────────────────────────
def draw_guard():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '从一句话到一条 SQL，中间隔着五道闸', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.7, '模型可以写 SQL，但不能决定它能跑什么', fontsize=12, color=DIM, ha='center')

    # 第一行：问题 → 语义解析 → SQL
    row1 = [
        (0.7, '"上周各渠道 GMV 环比"', '业务问题', SKY),
        (4.6, '语义层解析', '渠道 · GMV · 上周 · 环比', LIME),
        (8.5, '生成候选 SQL', '只用白名单内的表', AMBER),
    ]
    for x, title, note, color in row1:
        w = 3.2 if x < 8 else 3.6
        ax.add_patch(FancyBboxPatch((x, 5.35), w, 0.95,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(x + 0.2, 6.03, title, fontsize=9.5, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(x + 0.2, 5.62, note, fontsize=8, color=TEXT, ha='left', va='center')
    ax.annotate('', xy=(4.5, 5.82), xytext=(3.95, 5.82),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))
    ax.annotate('', xy=(8.4, 5.82), xytext=(7.85, 5.82),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))

    # 第二行：五道校验
    ax.text(0.7, 4.85, '五道校验，任何一道不过就重写', fontsize=9.5, fontweight='bold',
            color=CORAL, ha='left')
    gates = [
        ('表权限白名单', '只允许 catalog 内的表'),
        ('只读关键字', '禁 insert/update/drop'),
        ('EXPLAIN 估行', '预计扫描 > 千万行拒绝'),
        ('超时 30 秒', '到点强制中断'),
        ('结果 ≤ 5000 行', '超限改为聚合或导出'),
    ]
    gx = 0.7
    for i, (name, note) in enumerate(gates):
        ax.add_patch(FancyBboxPatch((gx, 3.55), 2.25, 0.95,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=CARD, edgecolor=CORAL, linewidth=1.2))
        ax.text(gx + 0.16, 4.18, f'{i + 1}. {name}', fontsize=8.6, fontweight='bold',
                color=CORAL, ha='left', va='center')
        ax.text(gx + 0.16, 3.82, note, fontsize=7.4, color=TEXT,
                ha='left', va='center')
        gx += 2.42

    # 第三行：只读副本 → 脱敏 → 看板
    row3 = [
        (0.7, '只读副本执行', '独立连接 · 不影响主库', MINT),
        (4.75, '结果脱敏 + 打时间戳', '手机号遮蔽 · 数据截至 T+1', SKY),
        (8.8, '返回 HTML 看板', '图表 + 明细 + 口径脚注', CORAL),
    ]
    for x, title, note, color in row3:
        w = 3.4 if x < 8 else 3.5
        ax.add_patch(FancyBboxPatch((x, 1.55), w, 1.0,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(x + 0.2, 2.25, title, fontsize=9.5, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(x + 0.2, 1.85, note, fontsize=7.8, color=TEXT, ha='left', va='center')

    ax.annotate('', xy=(2.4, 2.62), xytext=(2.4, 3.45),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))
    ax.annotate('', xy=(8.75, 2.05), xytext=(8.2, 2.05),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))

    ax.text(6.5, 0.85, '每一道都有日志：谁问的、生成了什么 SQL、跑了多久、返回多少行',
            fontsize=9, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'guard.png')


# ── 3：五个周期 ─────────────────────────────────────────────────────────────
def draw_cadence():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.0, '五个周期，回答五个不同的问题', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.55, '日看异常，周看趋势，月看目标，季看结构，年看战略', fontsize=12,
            color=DIM, ha='center')

    cards = [
        ('日', '昨天有没有异常', MINT, ['GMV / 订单量', '支付成功率', '退款率突增', '库存告警'], '每天 08:00'),
        ('周', '这周好在哪差在哪', LIME, ['周环比', '履约时效', '渠道结构', '客诉分布'], '每周一 09:00'),
        ('月', '月度目标差多少', AMBER, ['目标达成率', '客单价 / 复购', '成本结构', '人效'], '每月 1 日 10:00'),
        ('季', '结构有没有变化', CORAL, ['季度 OKR', '营收构成', '留存分层', '区域对比'], '每季首日'),
        ('年', '今年做成了什么', SKY, ['同比增长', '市场份额', '投入产出', '明年预算'], '1 月 2 日'),
    ]

    w = 2.38; gap = 0.18
    total = w * 5 + gap * 4
    x0 = (13 - total) / 2
    yb = 1.15; h = 4.55

    for i, (name, question, color, metrics, when) in enumerate(cards):
        x = x0 + i * (w + gap)
        # 头部
        ax.add_patch(FancyBboxPatch((x, yb + h - 0.72), w, 0.62,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2, yb + h - 0.41, name, fontsize=14, fontweight='bold',
                color=BG, ha='center', va='center')
        # 卡片
        ax.add_patch(FancyBboxPatch((x, yb), w, h - 0.85,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(x + 0.16, yb + h - 1.15, question, fontsize=8.4, fontweight='bold',
                color=TEXT, ha='left', va='center')
        my = yb + h - 1.7
        for m in metrics:
            ax.add_patch(plt.Circle((x + 0.26, my + 0.08), 0.05,
                                    facecolor=color, edgecolor='none', zorder=4))
            ax.text(x + 0.42, my + 0.08, m, fontsize=7.6, color=TEXT,
                    ha='left', va='center')
            my -= 0.46
        # 底部时间
        ax.add_patch(FancyBboxPatch((x + 0.14, yb + 0.16), w - 0.28, 0.42,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=DIM, linewidth=1))
        ax.text(x + w / 2, yb + 0.37, when, fontsize=7.4, color=color,
                ha='center', va='center')

    ax.text(6.5, 0.6, '同一套语义层，五个周期只换时间窗口和指标组合',
            fontsize=9.2, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'cadence.png')


# ── 4：HTML 看板布局 ───────────────────────────────────────────────────────
def draw_dashboard():
    fig, ax = plt.subplots(figsize=(13, 8.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 8.0); ax.axis('off')

    ax.text(6.5, 7.6, '一张 HTML 看板，装下所有周期', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.15, '顶部切周期，中间看趋势，底部查明细 —— 一个文件，双击就能开',
            fontsize=11.8, color=DIM, ha='center')

    # 浏览器窗口
    ax.add_patch(FancyBboxPatch((0.5, 0.55), 12.0, 6.25,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=PANEL, edgecolor='#2e4d40', linewidth=1.4))

    # 顶部栏
    ax.add_patch(Rectangle((0.5, 6.15), 12.0, 0.65, facecolor=CARD,
                           edgecolor='#2e4d40', lw=1))
    for j, c in enumerate(['#fb7185', '#fbbf24', '#a3e635']):
        ax.add_patch(plt.Circle((0.78 + j * 0.22, 6.47), 0.06, facecolor=c,
                                edgecolor='none'))
    ax.text(1.55, 6.47, '经营看板 · 支付业务 · 2026-11-05', fontsize=8.6,
            fontweight='bold', color=TEXT, ha='left', va='center')

    # 周期切换
    tabs = ['日', '周', '月', '季', '年']
    tx = 9.55
    for i, t in enumerate(tabs):
        act = (i == 1)
        ax.add_patch(FancyBboxPatch((tx, 6.28), 0.5, 0.38,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=MINT if act else '#26443a',
                                    edgecolor='none'))
        ax.text(tx + 0.25, 6.47, t, fontsize=7.2, fontweight='bold',
                color=BG if act else DIM, ha='center', va='center')
        tx += 0.56

    # KPI 卡
    kpis = [('本周 GMV', '¥ 1,284 万', '+12.4%', MINT),
            ('支付成功率', '98.7%', '+0.9pt', LIME),
            ('新增用户', '12,408', '+8.1%', AMBER),
            ('退款率', '1.82%', '-0.3pt', CORAL)]
    kx = 0.75
    for label, value, delta, color in kpis:
        ax.add_patch(FancyBboxPatch((kx, 5.05), 2.75, 0.9,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=CARD, edgecolor='#2e4d40', linewidth=1))
        ax.text(kx + 0.18, 5.72, label, fontsize=7.4, color=DIM, ha='left', va='center')
        ax.text(kx + 0.18, 5.4, value, fontsize=13, fontweight='bold', color=TEXT,
                ha='left', va='center')
        ax.text(kx + 2.55, 5.4, delta, fontsize=7.4, color=color, ha='right', va='center')
        kx += 2.9

    # 左图：折线
    ax.add_patch(FancyBboxPatch((0.75, 2.95), 5.5, 1.9,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=CARD, edgecolor='#2e4d40', linewidth=1))
    ax.text(0.95, 4.62, 'GMV 近 7 日趋势', fontsize=8, fontweight='bold', color=TEXT,
            ha='left', va='center')
    xs = [1.15, 1.85, 2.55, 3.25, 3.95, 4.65, 5.35]
    ys = [3.45, 3.68, 3.55, 3.95, 3.82, 4.12, 4.3]
    ax.plot(xs, ys, color=MINT, lw=2, zorder=4)
    for x, y in zip(xs, ys):
        ax.add_patch(plt.Circle((x, y), 0.04, facecolor=MINT, edgecolor='none', zorder=5))
    ax.plot([1.05, 5.85], [3.3, 3.3], color='#2e4d40', lw=1)
    for i, d in enumerate(['周一', '周二', '周三', '周四', '周五', '周六', '周日']):
        ax.text(1.15 + i * 0.7, 3.18, d, fontsize=5.8, color=DIM, ha='center')

    # 右图：柱状
    ax.add_patch(FancyBboxPatch((6.45, 2.95), 5.75, 1.9,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=CARD, edgecolor='#2e4d40', linewidth=1))
    ax.text(6.65, 4.62, '渠道 GMV 占比', fontsize=8, fontweight='bold', color=TEXT,
            ha='left', va='center')
    bars = [('APP', 0.75, MINT), ('小程序', 0.55, LIME), ('H5', 0.35, AMBER),
            ('线下', 0.22, CORAL), ('其他', 0.12, SKY)]
    bx = 6.8
    for name, v, color in bars:
        ax.add_patch(Rectangle((bx, 3.35), 0.55, v * 1.15, facecolor=color,
                               edgecolor='none', alpha=0.9))
        ax.text(bx + 0.275, 3.22, name, fontsize=5.8, color=DIM, ha='center')
        ax.text(bx + 0.275, 3.4 + v * 1.15, f'{int(v * 100)}', fontsize=6,
                color=color, ha='center')
        bx += 1.02

    # 明细表
    ax.add_patch(FancyBboxPatch((0.75, 0.85), 11.45, 1.85,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=CARD, edgecolor='#2e4d40', linewidth=1))
    ax.text(0.95, 2.44, '渠道明细（可排序、可下钻）', fontsize=8, fontweight='bold',
            color=TEXT, ha='left', va='center')
    heads = ['渠道', 'GMV', '环比', '订单数', '客单价']
    hx = [1.0, 3.0, 5.0, 7.0, 9.4]
    for h, x in zip(heads, hx):
        ax.text(x, 2.12, h, fontsize=6.8, color=SKY, ha='left', va='center')
    rows = [('APP', '¥ 9,630,000', '+14.2%', '48,120', '¥ 200'),
            ('小程序', '¥ 1,930,000', '+9.8%', '12,400', '¥ 156'),
            ('H5', '¥ 860,000', '-3.1%', '6,020', '¥ 143')]
    ry = 1.84
    for r in rows:
        for v, x in zip(r, hx):
            ax.text(x, ry, v, fontsize=6.5, color=TEXT, ha='left', va='center')
        ax.plot([0.95, 12.0], [ry - 0.13, ry - 0.13], color='#2e4d40', lw=0.6)
        ry -= 0.28

    ax.text(0.8, 0.72, '口径：GMV 含退款前金额 · 数据截至 2026-11-05 08:00 · 数据源 pay_order',
            fontsize=6.4, color=DIM, ha='left', va='center')

    save(fig, 'dashboard.png')


if __name__ == '__main__':
    draw_flow()
    draw_guard()
    draw_cadence()
    draw_dashboard()
    print('✓ 全部生成完毕')
