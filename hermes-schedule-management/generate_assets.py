#!/usr/bin/env python3
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0b1a15'
PANEL = '#12261f'
CARD = '#1a3329'
TEXT = '#e6f2ec'
DIM = '#6b8579'
LIME = '#a3e635'
MINT = '#34d399'
SKY = '#38bdf8'
AMBER = '#fbbf24'
CORAL = '#fb7185'
VIOLET = '#a78bfa'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：六过程 ITTO 表 ───────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.0); ax.axis('off')

    ax.text(6.5, 6.68, '进度管理六个过程，一条时间轴', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.26, '从「有哪些活」到「今天该到哪」，每一步都在收紧口径', fontsize=11.8,
            color=DIM, ha='center')

    procs = [
        ('01', '规划进度管理', '计划 · 章程 · OPA', '专家判断 · 会议',
         '进度管理计划', MINT),
        ('02', '定义活动', '范围基准 · WBS', '分解 · 滚动式规划',
         '活动清单\n里程碑清单', SKY),
        ('03', '排列活动顺序', '活动清单\n里程碑清单', 'PDM · 依赖确定\n提前量与滞后量',
         '进度网络图', VIOLET),
        ('04', '估算持续时间', '资源日历\n风险登记册', '类比 · 参数 · 三点\n自下而上 · 储备',
         '持续时间估算\n估算依据', AMBER),
        ('05', '制定进度计划', '网络图\n持续时间估算', '关键路径法\n资源优化 · 进度压缩',
         '进度基准\n进度数据', LIME),
        ('06', '控制进度', '绩效数据\n进度计划', '偏差 · 趋势\n挣值 · 关键路径',
         '进度预测\n变更请求', CORAL),
    ]

    cw = 1.72; gap = 0.12
    total = cw * 6 + gap * 5
    x0 = (13 - total) / 2 + 0.42
    top = 5.95

    # 表头行
    ax.text(0.42, top - 0.24, '过程', fontsize=8.5, fontweight='bold', color=DIM, ha='left')
    for i, (num, name, inp, tech, out, color) in enumerate(procs):
        x = x0 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, top - 0.55), cw, 0.62,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + cw / 2, top - 0.14, num, fontsize=7.2, color=BG, ha='center', va='center')
        ax.text(x + cw / 2, top - 0.40, name, fontsize=8.6, fontweight='bold',
                color=BG, ha='center', va='center')

    rows = [
        ('输入', 1.38, TEXT, [p[2] for p in procs]),
        ('技术', 1.38, TEXT, [p[3] for p in procs]),
        ('输出', 1.60, None, [p[4] for p in procs]),
    ]
    y = top - 0.80
    for label, h, color, contents in rows:
        ax.text(0.42, y - h / 2, label, fontsize=8.5, fontweight='bold', color=DIM,
                ha='left', va='center')
        for i, content in enumerate(contents):
            x = x0 + i * (cw + gap)
            c = color or procs[i][5]
            ax.add_patch(FancyBboxPatch((x, y - h), cw, h,
                                        boxstyle='round,pad=0.02,rounding_size=0.06',
                                        facecolor=PANEL, edgecolor='#254036', linewidth=1))
            ax.text(x + cw / 2, y - h / 2, content, fontsize=7.6, color=c,
                    ha='center', va='center', linespacing=1.6)
        y -= h + 0.09

    ax.text(6.5, 0.30, '第 4 步的估算误差，会一路放大到第 6 步的偏差 —— 所以估算才是整个进度的地基',
            fontsize=9, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'pipeline.png')


# ── 2：四种估算 + PERT 曲线 ─────────────────────────────────────────────────
def draw_estimate():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.05, '估得准，不是因为经验多', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.63, '而是因为用了对的方法，并且给出了区间', fontsize=11.8, color=DIM, ha='center')

    methods = [
        ('类比估算', '参照历史相似任务', '数据要求：有可比的过去', '误差 ±50%', MINT),
        ('参数估算', '按单位量 × 单价/工时', '数据要求：有稳定参数', '误差 ±25%', SKY),
        ('三点估算', '乐观 / 最可能 / 悲观', '数据要求：能给出分布', '误差 ±15%', AMBER),
        ('自下而上', '逐工作包累加', '数据要求：WBS 拆得够细', '误差 ±10%', LIME),
    ]

    y = 5.82
    for name, desc, req, err, color in methods:
        ax.add_patch(FancyBboxPatch((0.5, y - 0.62), 5.85, 0.86,
                                    boxstyle='round,pad=0.03,rounding_size=0.09',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.4))
        ax.add_patch(FancyBboxPatch((0.5, y - 0.62), 0.1, 0.86,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(0.78, y + 0.02, name, fontsize=9.8, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(2.35, y + 0.02, desc, fontsize=8.0, color=TEXT, ha='left', va='center')
        ax.text(0.78, y - 0.38, req, fontsize=7.2, color=DIM, ha='left', va='center')
        ax.text(6.15, y - 0.38, err, fontsize=8.0, fontweight='bold', color=color,
                ha='right', va='center')
        y -= 1.0

    ax.text(0.5, 0.95, '四种方法不是四选一 —— 先自下而上算，再用类比校准', fontsize=8.6,
            color=DIM, ha='left', va='center')

    # 右：PERT 曲线（手工映射到卡片坐标）
    ax.add_patch(FancyBboxPatch((6.7, 0.85), 5.8, 5.3,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=AMBER, linewidth=1.6))
    ax.text(7.0, 5.85, '三点估算为什么比单点准', fontsize=10, fontweight='bold',
            color=AMBER, ha='left', va='center')

    O, M, P = 6.0, 9.0, 18.0
    E = (O + 4 * M + P) / 6

    def px(v):
        return 7.15 + (v - 4.0) / 16.0 * 5.0

    xs = np.linspace(O, P, 400)
    yv = ((xs - O) / (P - O)) ** 2.2 * ((P - xs) / (P - O)) ** 2.6
    yv = yv / yv.max()

    base = 2.35
    scale = 2.25
    ax.plot([px(v) for v in xs], base + yv * scale, color=AMBER, lw=2.2, zorder=3)
    ax.fill_between([px(v) for v in xs], base, base + yv * scale,
                    color=AMBER, alpha=0.16, zorder=2)
    ax.plot([px(4.0), px(20.0)], [base, base], color='#2b4a3c', lw=1.2)

    for val, label, color in [(O, f'乐观 {O:.0f}d', MINT),
                              (M, f'最可能 {M:.0f}d', SKY),
                              (P, f'悲观 {P:.0f}d', CORAL)]:
        ax.plot([px(val), px(val)], [base, base + 2.5], color=color, lw=1.2, ls='--', zorder=3)
        ax.text(px(val), base - 0.22, label, fontsize=7.6, color=color,
                ha='center', va='top')

    ax.plot([px(E), px(E)], [base, base + 2.62], color=LIME, lw=2.0, zorder=4)
    ax.text(px(E), base + 2.68, f'期望 {E:.1f}d', fontsize=8.6, fontweight='bold',
            color=LIME, ha='center', va='bottom')

    ax.text(7.0, 1.45, 'E = (O + 4M + P) / 6', fontsize=9.5, fontweight='bold',
            color=LIME, ha='left', va='center', fontfamily='monospace')
    ax.text(7.0, 1.12, 'σ = (P - O) / 6 → 能说出「85% 概率在 14 天内」', fontsize=7.6,
            color=DIM, ha='left', va='center')

    save(fig, 'estimate.png')


# ── 3：网络图与关键路径 ─────────────────────────────────────────────────────
def draw_cpm():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.85, '关键路径不是最长的那个，是最不能拖的那个', fontsize=22,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.42, '上面一行是早开始/早完成，下面一行是晚开始/晚完成 —— 上下相等就是关键活动',
            fontsize=10.8, color=DIM, ha='center')

    # 节点坐标
    pos = {
        'A': (1.6, 4.55), 'B': (4.15, 5.55), 'C': (4.15, 3.55),
        'D': (6.75, 4.55), 'E': (6.75, 2.55), 'F': (9.4, 4.55),
    }
    # 数据: (dur, ES, EF, LS, LF, critical)
    data = {
        'A': (2, 0, 2, 0, 2, True),
        'B': (4, 2, 6, 2, 6, True),
        'C': (3, 2, 5, 3, 6, False),
        'D': (3, 6, 9, 6, 9, True),
        'E': (2, 6, 8, 7, 9, False),
        'F': (2, 9, 11, 9, 11, True),
    }
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('B', 'E'), ('D', 'F'), ('E', 'F')]

    for s, t in edges:
        x1, y1 = pos[s]; x2, y2 = pos[t]
        crit = data[s][5] and data[t][5]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle='-|>', mutation_scale=12,
                                     color=CORAL if crit else '#3a5c4d',
                                     lw=2.2 if crit else 1.3,
                                     shrinkA=26, shrinkB=26, zorder=2))

    for name, (x, y) in pos.items():
        dur, es, ef, ls, lf, crit = data[name]
        color = CORAL if crit else SKY
        ax.add_patch(plt.Circle((x, y), 0.46, facecolor=CARD,
                                edgecolor=color, linewidth=2.4, zorder=4))
        ax.text(x, y + 0.08, name, fontsize=12, fontweight='bold', color=color,
                ha='center', va='center', zorder=5)
        ax.text(x, y - 0.24, f'{dur}d', fontsize=7.6, color=DIM,
                ha='center', va='center', zorder=5)
        ax.text(x, y + 0.66, f'{es} / {ef}', fontsize=7.6, color=TEXT,
                ha='center', va='center')
        ax.text(x, y - 0.72, f'{ls} / {lf}', fontsize=7.6,
                color=color if crit else DIM, ha='center', va='center')

    # 图例
    ax.add_patch(FancyBboxPatch((0.5, 0.55), 5.6, 1.35,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PANEL, edgecolor=CORAL, linewidth=1.2))
    ax.text(0.78, 1.62, '关键路径 A → B → D → F = 11 天', fontsize=9, fontweight='bold',
            color=CORAL, ha='left', va='center')
    ax.text(0.78, 1.3, 'C 的浮动 1 天，E 的浮动 1 天 —— 它们可以晚，但不能晚超过 1 天',
            fontsize=7.6, color=TEXT, ha='left', va='center')
    ax.text(0.78, 1.0, '浮动归零的那一刻，C 和 E 就变成了新的关键路径', fontsize=7.6,
            color=AMBER, ha='left', va='center')
    ax.text(0.78, 0.72, '监控要盯的是「浮动还剩多少」，不是「完成百分比」', fontsize=7.6,
            color=DIM, ha='left', va='center')

    ax.add_patch(FancyBboxPatch((6.5, 0.55), 6.0, 1.35,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=CARD, edgecolor=VIOLET, linewidth=1.2))
    ax.text(6.78, 1.62, '总浮动 vs 自由浮动', fontsize=9, fontweight='bold',
            color=VIOLET, ha='left', va='center')
    ax.text(6.78, 1.3, '总浮动：不影响项目完工的前提下能拖多久', fontsize=7.6,
            color=TEXT, ha='left', va='center')
    ax.text(6.78, 1.0, '自由浮动：不影响下一个活动最早开始的前提下能拖多久', fontsize=7.6,
            color=TEXT, ha='left', va='center')
    ax.text(6.78, 0.72, '自由浮动先归零，是更早的预警信号', fontsize=7.6,
            color=AMBER, ha='left', va='center')

    save(fig, 'cpm.png')


# ── 4：偏差监控 ─────────────────────────────────────────────────────────────
def draw_monitor():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.22, '完成百分比会说谎，累计曲线不会', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.8, 'S 曲线看的不是「做了多少」，是「差了多少、差得在加速还是收敛」',
            fontsize=11.5, color=DIM, ha='center')

    # 左：S 曲线（手工映射，避免与整图坐标系冲突）
    ax.add_patch(FancyBboxPatch((0.5, 1.0), 7.0, 5.35,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=SKY, linewidth=1.6))
    ax.text(0.8, 6.02, '进度 S 曲线 · 计划 vs 实际', fontsize=9.5, fontweight='bold',
            color=SKY, ha='left', va='center')

    # 图例
    ax.plot([5.5, 5.85], [6.02, 6.02], color=SKY, lw=2.2)
    ax.text(5.92, 6.02, '计划', fontsize=7.4, color=DIM, ha='left', va='center')
    ax.plot([6.55, 6.9], [6.02, 6.02], color=CORAL, lw=2.2)
    ax.text(6.97, 6.02, '实际', fontsize=7.4, color=DIM, ha='left', va='center')

    gx0, gx1 = 1.45, 7.10
    gy0, gy1 = 1.72, 5.35

    def mx(d):
        return gx0 + d / 20.0 * (gx1 - gx0)

    def my(p):
        return gy0 + p / 100.0 * (gy1 - gy0)

    days = np.arange(0, 21)
    plan = 100 / (1 + np.exp(-(days - 10) / 2.6))
    actual = 100 / (1 + np.exp(-(days - 12.6) / 3.0)) * np.linspace(0.86, 1.0, 21)

    for p in [25, 50, 75, 100]:
        ax.plot([gx0, gx1], [my(p), my(p)], color='#254036', lw=0.8, ls='--', alpha=0.7)
        ax.text(gx0 - 0.13, my(p), str(p), fontsize=6.6, color=DIM, ha='right', va='center')

    ax.plot([gx0, gx1 + 0.12], [gy0, gy0], color='#2b4a3c', lw=1)
    ax.plot([gx0, gx0], [gy0, gy1 + 0.12], color='#2b4a3c', lw=1)
    for d in [0, 5, 10, 15, 20]:
        ax.text(mx(d), gy0 - 0.16, str(d), fontsize=6.6, color=DIM, ha='center', va='top')

    ax.fill_between([mx(d) for d in days], [my(a) for a in actual],
                    [my(p) for p in plan], color=CORAL, alpha=0.16)
    ax.plot([mx(d) for d in days], [my(p) for p in plan], color=SKY, lw=2.2, zorder=4)
    ax.plot([mx(d) for d in days], [my(a) for a in actual], color=CORAL, lw=2.2, zorder=4)

    ax.annotate('', xy=(mx(14), my(plan[14])), xytext=(mx(14), my(actual[14])),
                arrowprops=dict(arrowstyle='<->', color=AMBER, lw=1.6, shrinkA=2, shrinkB=2))
    ax.text(mx(14) + 0.12, (my(plan[14]) + my(actual[14])) / 2, 'SV < 0', fontsize=7.8,
            color=AMBER, fontweight='bold', ha='left', va='center')

    ax.scatter([mx(14)], [my(actual[14])], s=28, color=CORAL, zorder=5)
    ax.text(mx(14), my(actual[14]) - 0.22, '今日 62%', fontsize=7.2, color=CORAL,
            ha='center', va='top')

    ax.text(0.8, 1.35, '↑ 关键路径工作完成率   → 时间（天）', fontsize=7.2, color=DIM,
            ha='left', va='center')

    # 右：三个指标
    ax.add_patch(FancyBboxPatch((7.8, 1.0), 4.7, 5.35,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=CORAL, linewidth=1.6))
    ax.text(8.1, 6.02, '三个指标，就够判断', fontsize=9.5, fontweight='bold',
            color=CORAL, ha='left', va='center')

    kpis = [
        ('SV  进度偏差', 'EV - PV', '-8.4 人日', '负值 = 落后', CORAL),
        ('SPI 进度绩效', 'EV / PV', '0.87', '< 0.9 要预警', AMBER),
        ('CP 漂移', 'CP drift (days)', '+3 天', '漂移比绝对值更危险', VIOLET),
    ]
    ky = 5.55
    for name, formula, val, note, color in kpis:
        ax.add_patch(FancyBboxPatch((8.1, ky - 1.28), 4.1, 1.2,
                                    boxstyle='round,pad=0.03,rounding_size=0.09',
                                    facecolor=CARD, edgecolor=color, linewidth=1.1))
        ax.text(8.32, ky - 0.28, name, fontsize=8.6, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(8.32, ky - 0.58, formula, fontsize=7.0, color=DIM,
                ha='left', va='center', fontfamily='monospace')
        ax.text(11.95, ky - 0.32, val, fontsize=10.5, fontweight='bold', color=color,
                ha='right', va='center')
        ax.text(8.32, ky - 0.94, note, fontsize=7.2, color=TEXT, ha='left', va='center')
        ky -= 1.38

    ax.text(8.1, 1.22, '三级预警：SPI < 0.95 观察 / < 0.9 预警 / < 0.8 升级',
            fontsize=7.2, color=DIM, ha='left', va='center')

    save(fig, 'monitor.png')


# ── 5：群消息四种格式 ───────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.42, '四种消息，只在必须打扰时打扰', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.0, '日常静默，异常才响 —— 这是进度群能活过三个月的唯一办法', fontsize=11.8,
            color=DIM, ha='center')

    msgs = [
        ('进度预警', '每天 09:00 · 有偏差才发', CORAL, [
            'SPI 0.87，关键路径漂移 +3 天',
            '· PAY-3401 联调延期，阻塞下游 4 个活动',
            '· 浮动已耗尽：D 节点剩余 0 天',
            '请 @张明 今日确认是否申请顺延',
        ]),
        ('估算评审', '估算提交时', AMBER, [
            '本次估算 18 人日（区间 14–26）',
            '· 类比历史 3 个相似需求：12 / 16 / 22 人日',
            '· 三点估算 σ=2.0，达成概率 85% 需 22 人日',
            '请确认是否按 22 人日排期',
        ]),
        ('里程碑达成', '里程碑完成时', MINT, [
            'M3「支付网关联调」已达成',
            '· 计划 11-08，实际 11-08，偏差 0 天',
            '· 4 个前置活动全部验收，无遗留缺陷',
            '下个里程碑 M4：11-22 生产灰度',
        ]),
        ('进度健康度', '每周五 17:30', SKY, [
            '本周进度健康度：72 分（上周 80）',
            '· 计划完成率 91% · 此处浮动余量 8%',
            '· 延期活动 3 个，集中在联调环节',
            '下周动作：联调提前 2 天启动，预置 mock',
        ]),
    ]

    w = 5.95; h = 2.52
    xs = [0.4, 6.65]
    ys = [4.1, 1.3]

    for i, (name, when, color, lines) in enumerate(msgs):
        x = xs[i % 2]; y = ys[i // 2]
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.6))
        ax.add_patch(FancyBboxPatch((x + 0.2, y + h - 0.62), 1.35, 0.38,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.875, y + h - 0.43, name, fontsize=8.2, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(x + 1.7, y + h - 0.43, when, fontsize=7.4, color=DIM,
                ha='left', va='center')

        ly = y + h - 0.95
        for j, ln in enumerate(lines):
            ax.text(x + 0.25, ly, ln, fontsize=7.7, color=TEXT if j else color,
                    ha='left', va='center', fontweight='bold' if j == 0 else 'normal')
            ly -= 0.38

    ax.text(6.5, 0.55, '三类事件驱动要快，一类定时汇总要稳 —— 但都只有四行',
            fontsize=9, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_estimate()
    draw_cpm()
    draw_monitor()
    draw_message()
    print('✓ 全部生成完毕')
