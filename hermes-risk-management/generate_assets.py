#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#131417'
PANEL = '#1d1e23'
CARD = '#282a31'
TEXT = '#eceef2'
DIM = '#8a8f99'
RED = '#ef4444'
ORANGE = '#f97316'
YELLOW = '#eab308'
GREEN = '#22c55e'
BLUE = '#3b82f6'
PURPLE = '#a855f7'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：七个过程 4+3 ────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.22, '风险管理有七个过程，数量最多，也最容易只做前两个', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.88, '识别和分析每年都做，应对和监督基本没人做', fontsize=11.5,
            color=DIM, ha='center')

    procs = [
        ('规划风险管理', '定制度', PURPLE,
         '章程 · 计划 · OPA', '专家判断 · 会议', '风险管理计划'),
        ('识别风险', '找全', BLUE,
         '计划 · 文件 · 采购文档', '头脑风暴 · 核对单 · SWOT', '风险登记册 · 风险报告'),
        ('定性分析', '排序', YELLOW,
         '登记册 · 概率影响矩阵', '概率影响评估 · 紧迫性', '登记册更新（等级）'),
        ('定量分析', '算钱', ORANGE,
         '登记册 · 进度成本基准', '蒙特卡洛 · 决策树 · EMV', '储备建议 · 概率分布'),
        ('规划风险应对', '定招', RED,
         '登记册 · 风险报告', '规避 · 转移 · 减轻 · 接受', '变更请求 · 应对计划'),
        ('实施风险应对', '落地', '#db2777',
         '应对计划 · 登记册', '影响力 · PMIS', '变更请求 · 登记册更新'),
        ('监督风险', '验效', GREEN,
         '绩效数据 · 登记册', '技术绩效分析 · 储备分析', '工作绩效信息 · 变更请求'),
    ]

    w, gap, ch = 2.92, 0.18, 2.00
    x0 = (13 - (4 * w + 3 * gap)) / 2
    rows = [(3.60, 4), (1.15, 3)]

    for idx, (name, tag, color, inp, tech, out) in enumerate(procs):
        if idx < 4:
            col, y = idx, rows[0][0]
        else:
            col, y = idx - 4, rows[1][0]
        x = x0 if idx < 4 else x0 + (w + gap) / 2
        x = x + col * (w + gap)

        ax.add_patch(FancyBboxPatch((x, y), w, ch,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=PANEL, edgecolor='#33353d', linewidth=1.2))
        ax.add_patch(FancyBboxPatch((x, y + ch - 0.52), w, 0.52,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.16, y + ch - 0.26, f'{idx + 1:02d}', fontsize=7.8,
                fontweight='bold', color='#131417', ha='left', va='center')
        ax.text(x + 0.56, y + ch - 0.26, name, fontsize=8.4, fontweight='bold',
                color='#131417', ha='left', va='center')
        ax.text(x + w - 0.16, y + ch - 0.26, tag, fontsize=6.4, color='#131417',
                ha='right', va='center')

        blocks = [('输入', inp, BLUE, y + 1.16), ('技术', tech, GREEN, y + 0.78),
                  ('输出', out, YELLOW, y + 0.40)]
        for label, body, lc, ly in blocks:
            ax.text(x + 0.16, ly, label, fontsize=6.0, fontweight='bold', color=lc,
                    ha='left', va='center')
            ax.text(x + 0.70, ly, body, fontsize=6.2, color='#c2c8d2',
                    ha='left', va='center')

    ax.text(6.5, 0.72, '七个过程里，只有第 6、7 个能证明「风险真的被管住了」—— 而它们最常缺席',
            fontsize=8.4, color=DIM, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：概率影响矩阵 ────────────────────────────────────────────────────
def draw_matrix():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.20, '风险分级不靠感觉，靠一张 5×5 的格子', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.86, '概率乘影响，落在哪个格子，就决定了多久看一次、谁来管',
            fontsize=11.5, color=DIM, ha='center')

    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.55, 5.05,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=RED, linewidth=1.5))
    ax.text(0.75, 5.30, '概率 · 影响矩阵（分值 = 概率 × 影响）', fontsize=9.0,
            fontweight='bold', color=RED, ha='left', va='center')

    gx0, gy0 = 1.62, 1.35
    cw, rh = 0.79, 0.71
    cgap, rgap = 0.06, 0.06

    def cell_color(score):
        if score >= 15:
            return RED
        if score >= 9:
            return ORANGE
        if score >= 4:
            return YELLOW
        return GREEN

    for pi in range(5):
        prob = 5 - pi
        yv = gy0 + (4 - pi) * (rh + rgap)
        ax.text(gx0 - 0.16, yv + rh / 2, str(prob), fontsize=7.6, color=DIM,
                ha='right', va='center')
        for im in range(5):
            impact = im + 1
            score = prob * impact
            c = cell_color(score)
            xv = gx0 + im * (cw + cgap)
            ax.add_patch(FancyBboxPatch((xv, yv), cw, rh,
                                        boxstyle='round,pad=0.01,rounding_size=0.05',
                                        facecolor=c, edgecolor=c, linewidth=0,
                                        alpha=0.88))
            ax.text(xv + cw / 2, yv + rh / 2, str(score), fontsize=7.2,
                    fontweight='bold', color='#131417', ha='center', va='center')

    for im in range(5):
        xv = gx0 + im * (cw + cgap) + cw / 2
        ax.text(xv, gy0 - 0.20, str(im + 1), fontsize=7.6, color=DIM,
                ha='center', va='center')
    ax.text(gx0 + 2 * (cw + cgap) + cw / 2, gy0 - 0.42, '影响程度', fontsize=7.4,
            color='#c2c8d2', ha='center', va='center')
    ax.text(gx0 - 0.58, gy0 + 2 * (rh + rgap) + rh / 2, '概率', fontsize=7.4,
            color='#c2c8d2', rotation=90, ha='center', va='center')

    # 图例
    legend = [('高风险 15-25', RED, '每周看，必须有触发条件'), ('中高 9-12', ORANGE, '每两周看'),
              ('中低 4-8', YELLOW, '每月看'), ('低风险 1-3', GREEN, '登记即可')]
    for idx, (name, c, note) in enumerate(legend):
        yv = 4.35 - idx * 0.95
        ax.add_patch(FancyBboxPatch((5.95, yv), 0.22, 0.22,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor=c, edgecolor=c, linewidth=0))
        ax.text(6.26, yv + 0.11, name, fontsize=6.6, fontweight='bold', color=c,
                ha='left', va='center')

    ax.text(0.75, 0.72, '同一个分数，处在不同阶段含义不同 —— 矩阵只是排序工具，不是结论',
            fontsize=7.0, color=DIM, ha='left', va='center')

    # 右：处理原则
    ax.add_patch(FancyBboxPatch((7.20, 0.55), 5.35, 5.05,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=YELLOW, linewidth=1.5))
    ax.text(7.50, 5.30, '等级决定三件事：谁管、多久看、何时触发', fontsize=9.0,
            fontweight='bold', color=YELLOW, ha='left', va='center')

    rules = [
        ('高', '项目经理 + 发起人', '每周评审，必须有应对计划和触发条件', RED),
        ('中高', '项目经理', '每两周评审，应对计划可合并', ORANGE),
        ('中低', '模块负责人', '每月评审，只需登记与观察', YELLOW),
        ('低', '不指定', '登记即可，季度扫一遍', GREEN),
    ]
    for idx, (lv, owner, rule, color) in enumerate(rules):
        yv = 4.30 - idx * 1.05
        ax.add_patch(FancyBboxPatch((7.50, yv), 4.75, 0.90,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=CARD, edgecolor='#34363f', linewidth=1))
        ax.add_patch(FancyBboxPatch((7.50, yv + 0.10), 0.42, 0.70,
                                    boxstyle='round,pad=0.01,rounding_size=0.05',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(7.71, yv + 0.45, lv, fontsize=8.6, fontweight='bold', color='#131417',
                ha='center', va='center')
        ax.text(8.10, yv + 0.62, owner, fontsize=7.0, fontweight='bold',
                color='#e2e6ec', ha='left', va='center')
        ax.text(8.10, yv + 0.28, rule, fontsize=6.3, color=DIM, ha='left', va='center')

    ax.text(7.50, 0.92, '没有「谁管、多久看」的分级，等于没分级', fontsize=7.2,
            color=DIM, ha='left', va='center')

    save(fig, 'matrix.png')


# ── 3：龙卷风图 + 五种应对策略 ─────────────────────────────────────────
def draw_tornado():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.20, '哪个变量最要命，龙卷风图一眼看出来', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.86, '同样算「影响工期多少天」，横条越长，越该优先投人力去控',
            fontsize=11.5, color=DIM, ha='center')

    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.65, 5.05,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ORANGE, linewidth=1.5))
    ax.text(0.75, 5.30, '敏感性分析 · 工期偏差区间（天）', fontsize=9.0,
            fontweight='bold', color=ORANGE, ha='left', va='center')

    items = [
        ('上游接口交付', -9, 14),
        ('需求变更频次', -3, 12),
        ('第三方支付通道', -6, 11),
        ('测试环境可用性', -5, 8),
        ('核心人员稳定', -4, 6),
    ]

    cx = 3.90
    scale = 0.195
    for idx, (name, lo, hi) in enumerate(items):
        yv = 4.55 - idx * 0.82
        ax.text(0.72, yv + 0.24, name, fontsize=7.0, color='#c2c8d2',
                ha='left', va='center')
        xl, xr = cx + lo * scale, cx + hi * scale
        ax.add_patch(FancyBboxPatch((xl, yv), xr - xl, 0.48,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor=ORANGE if idx == 0 else '#c2410c',
                                    edgecolor='none', linewidth=0, alpha=0.55 if idx else 0.85))
        ax.text(xl - 0.08, yv + 0.24, f'{lo}', fontsize=6.2, color=DIM,
                ha='right', va='center')
        ax.text(xr + 0.08, yv + 0.24, f'+{hi}', fontsize=6.4, fontweight='bold',
                color=ORANGE if idx == 0 else '#c2c8d2', ha='left', va='center')

    ax.plot([cx, cx], [1.05, 5.00], color=DIM, lw=1.0, linestyle='--', alpha=0.6)
    ax.text(cx, 5.12, '基准', fontsize=6.2, color=DIM, ha='center', va='center')

    ax.text(0.75, 0.80, '前两条占到总方差的一半以上 —— 资源就该压在这两件事上',
            fontsize=7.2, color=DIM, ha='left', va='center')

    ax.add_patch(FancyBboxPatch((7.30, 0.55), 5.25, 5.05,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.5))
    ax.text(7.60, 5.30, '威胁的五种应对：先想能不能不玩', fontsize=9.0,
            fontweight='bold', color=GREEN, ha='left', va='center')

    strategies = [
        ('上报', '超出项目权限，交项目集或 PMO', '#7c3aed'),
        ('规避', '改方案彻底消除威胁，如换选型', BLUE),
        ('转移', '买保险、外包、固定价合同', '#0891b2'),
        ('减轻', '降概率或降影响，加测试、双供应商', GREEN),
        ('接受', '主动留储备，或被动只登记', YELLOW),
    ]
    for idx, (name, note, color) in enumerate(strategies):
        yv = 4.35 - idx * 0.86
        ax.add_patch(FancyBboxPatch((7.60, yv), 4.65, 0.72,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=CARD, edgecolor='#34363f', linewidth=1))
        ax.text(7.80, yv + 0.48, name, fontsize=8.2, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(7.80, yv + 0.20, note, fontsize=6.5, color='#c2c8d2', ha='left', va='center')

    ax.text(7.60, 0.80, '顺序很重要：规避 > 转移 > 减轻 > 接受', fontsize=7.2,
            color=DIM, ha='left', va='center')

    save(fig, 'tornado.png')


# ── 4：风险敞口趋势 + 四个指标 ──────────────────────────────────────────
def draw_monitor():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.20, '监督风险不是数一数还剩几条，是看敞口往哪走', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.86, '条数在减少、敞口在上升，说明关掉的是小事，留下来的都是硬的',
            fontsize=11.5, color=DIM, ha='center')

    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.65, 5.05,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=1.5))
    ax.text(0.75, 5.30, '未关闭风险 · 按等级堆叠（每周）', fontsize=9.0,
            fontweight='bold', color=BLUE, ha='left', va='center')

    weeks = ['W41', 'W42', 'W43', 'W44', 'W45', 'W46']
    high = [2, 3, 3, 4, 3, 4]
    mid = [5, 6, 7, 6, 7, 8]
    low = [8, 7, 6, 6, 5, 4]

    y0, unit = 1.35, 0.215
    bx, bw, step = 1.55, 0.62, 0.78
    for i in range(6):
        x = bx + i * step
        h_low = low[i] * unit
        h_mid = mid[i] * unit
        h_high = high[i] * unit
        ax.add_patch(FancyBboxPatch((x, y0), bw, h_low,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=GREEN, edgecolor=GREEN, linewidth=0, alpha=0.85))
        ax.add_patch(FancyBboxPatch((x, y0 + h_low), bw, h_mid,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=YELLOW, edgecolor=YELLOW, linewidth=0, alpha=0.85))
        ax.add_patch(FancyBboxPatch((x, y0 + h_low + h_mid), bw, h_high,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=RED, edgecolor=RED, linewidth=0, alpha=0.9))
        ax.text(x + bw / 2, 1.10, weeks[i], fontsize=6.6, color=DIM, ha='center', va='center')
        ax.text(x + bw / 2, y0 + h_low + h_mid + h_high + 0.12, str(high[i] + mid[i] + low[i]),
                fontsize=6.6, fontweight='bold', color='#c2c8d2', ha='center', va='center')

    for val in [0, 5, 10, 15]:
        yy = y0 + val * unit
        ax.plot([1.40, 6.30], [yy, yy], color='#33353d', lw=0.8, alpha=0.8)
        ax.text(1.30, yy, str(val), fontsize=6.2, color=DIM, ha='right', va='center')

    legends = [('高', RED), ('中', YELLOW), ('低', GREEN)]
    for idx, (name, c) in enumerate(legends):
        lx = 4.55 + idx * 0.60
        ax.add_patch(FancyBboxPatch((lx, 5.02), 0.16, 0.16,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=c, edgecolor=c, linewidth=0))
        ax.text(lx + 0.22, 5.10, name, fontsize=6.4, color=DIM, ha='left', va='center')

    ax.text(0.75, 0.78, '总量在降，红色在涨 —— 这比「本轮关闭 12 条」有用得多',
            fontsize=6.9, color=RED, ha='left', va='center')

    ax.add_patch(FancyBboxPatch((7.30, 0.55), 5.25, 5.05,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.5))
    ax.text(7.60, 5.30, '监督风险只看四个数', fontsize=9.0, fontweight='bold',
            color=GREEN, ha='left', va='center')

    metrics = [
        ('风险敞口值', '42.5', '概率 × 影响 加权求和，环比 +6%', RED),
        ('触发命中率', '3 / 7', '登记的触发条件真的发生了几次', ORANGE),
        ('应对完成率', '64%', '到期的应对动作完成比例', YELLOW),
        ('储备消耗率', '38%', '应急储备已用比例，超 70% 要报警', BLUE),
    ]
    for idx, (name, val, note, color) in enumerate(metrics):
        yv = 4.10 - idx * 1.05
        ax.add_patch(FancyBboxPatch((7.60, yv), 4.65, 0.90,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=CARD, edgecolor='#34363f', linewidth=1))
        ax.text(7.80, yv + 0.62, name, fontsize=7.6, color='#c2c8d2', ha='left', va='center')
        ax.text(12.05, yv + 0.62, val, fontsize=8.6, fontweight='bold', color=color,
                ha='right', va='center')
        ax.text(7.80, yv + 0.26, note, fontsize=6.3, color=DIM, ha='left', va='center')

    ax.text(7.60, 0.80, '触发命中率低不一定是好事：可能是条件写得根本不会发生',
            fontsize=6.9, color=DIM, ha='left', va='center')

    save(fig, 'monitor.png')


# ── 5：四类群消息 ──────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '风险消息只有四类，其余都是噪音', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.72, '触发命中、需要升级、阶段复盘，加每周一次台账',
            fontsize=11.5, color=DIM, ha='center')

    cards = [
        ('风险预警', '触发条件命中', RED, [
            '上游接口延期 3 天，R-014 触发预警',
            '· 概率 40% 升至 75%，影响 +8 天',
            '· 已启动：切换备用供应商',
            '请 @李经理 今天确认切换窗口',
        ]),
        ('风险升级', '超出项目权限', ORANGE, [
            'R-021 供应商资质问题需上报 PMO',
            '· 已尝试：法务初审、备选比价',
            '· 若不处理：合规风险，阻塞上线',
            '请 @张总 牵头本周三方会议',
        ]),
        ('风险复盘', '阶段收尾', BLUE, [
            '本阶段关闭 9 条，失效 2 条，漏判 1 条',
            '· 命中：R-014 提前 3 周识别并备货',
            '· 失效：R-008 触发条件从未发生',
            '请各负责人补齐或下调触发条件',
        ]),
        ('登记册更新', '每周一 09:30', GREEN, [
            '新增 4 条，降级 2 条，关闭 3 条',
            '· 最高风险：R-021 供应商资质',
            '· 敞口值 42.5，环比上升 6%',
            '完整清单见 KB：PRJ-PAY / risk',
        ]),
    ]

    positions = [(0.45, 3.85), (6.65, 3.85), (0.45, 0.65), (6.65, 0.65)]
    for (title, freq, color, lines), (cx, cy) in zip(cards, positions):
        cw, ch = 5.9, 2.75
        ax.add_patch(FancyBboxPatch((cx, cy), cw, ch,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.add_patch(FancyBboxPatch((cx + 0.22, cy + ch - 0.68), 1.5, 0.42,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(cx + 0.97, cy + ch - 0.47, title, fontsize=8.4, fontweight='bold',
                color='#131417', ha='center', va='center')
        ax.text(cx + 1.85, cy + ch - 0.47, freq, fontsize=7.0, color=DIM,
                ha='left', va='center')

        iy = cy + ch - 1.05
        for j, line in enumerate(lines):
            ax.text(cx + 0.28, iy, line, fontsize=7.4,
                    color=TEXT if j == 0 else '#c2c8d2',
                    ha='left', va='center',
                    fontweight='bold' if j == 0 else 'normal')
            iy -= 0.42

    ax.text(6.5, 0.28, '每条四行：判断 / 依据 / 影响 / 要谁在什么时候做什么',
            fontsize=8.2, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_matrix()
    draw_tornado()
    draw_monitor()
    draw_message()
    print('✓ 全部生成完毕')
