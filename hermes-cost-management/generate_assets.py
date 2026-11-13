#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#100d0a'
PANEL = '#1c1712'
CARD = '#282018'
TEXT = '#f0e8dc'
DIM = '#8a7d70'
GOLD = '#e8b04b'
COPPER = '#d97757'
GREEN = '#4ade80'
RED = '#f87171'
BLUE = '#60a5fa'
PURPLE = '#c084fc'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：四个过程的 ITTO ─────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.0); ax.axis('off')

    ax.text(6.5, 6.72, '成本管理只有四个过程，但每一步都在改数字', fontsize=21, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.38, '十大领域里过程最少的一个，却是数据最脏的一个', fontsize=11.5,
            color=DIM, ha='center')

    procs = [
        ('规划成本管理', '定规则', GOLD),
        ('估算成本', '给数字', COPPER),
        ('制定预算', '立基准', GREEN),
        ('控制成本', '盯偏差', RED),
    ]

    cols = [
        ['项目章程', '项目管理计划', '事业环境因素', '组织过程资产'],
        ['范围基准 · 进度基准', '资源需求 · 资源单价', '风险登记册', '历史项目数据'],
        ['成本估算', '项目进度网络图', '风险登记册', '协议 · 资金限制'],
        ['成本基准', '实际支出 · 承诺成本', '工作绩效数据', '变更请求'],
    ]
    techs = [
        ['专家判断', '数据分析', '会议'],
        ['类比估算', '参数估算', '自下而上 · 三点'],
        ['成本汇总', '储备分析', '资金限制平衡'],
        ['挣值分析', '偏差 · 趋势分析', '完工尚需绩效'],
    ]
    outs = [
        ['成本管理计划', '', '', ''],
        ['成本估算', '估算依据', '', ''],
        ['成本基准', '项目资金需求', '', ''],
        ['工作绩效信息', '成本预测', '变更请求', ''],
    ]

    x0 = 1.62; w = 2.6; gap = 0.12
    for i, (name, tag, color) in enumerate(procs):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 5.45), w, 0.73,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2, 5.93, name, fontsize=10.5, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(x + w / 2, 5.63, tag, fontsize=7.4, color=BG,
                ha='center', va='center')

    row_labels = ['输入', '技术', '输出']
    row_y = [4.62, 3.42, 2.22]
    row_h = [1.5, 1.0, 1.0]

    for label, y, h in zip(row_labels, row_y, row_h):
        ax.text(0.85, y, label, fontsize=10, fontweight='bold', color=GOLD,
                ha='center', va='center', rotation=0)

    for i in range(4):
        x = x0 + i * (w + gap)
        for row, (data, y, h) in enumerate(zip([cols[i], techs[i], outs[i]], row_y, row_h)):
            color = [GOLD, COPPER, GREEN][row]
            ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h,
                                        boxstyle='round,pad=0.03,rounding_size=0.07',
                                        facecolor=PANEL if row != 1 else CARD,
                                        edgecolor='#33291f', linewidth=1))
            lines = [d for d in data if d]
            if row == 0:
                txt = '\n'.join(lines)
                ax.text(x + 0.14, y + h / 2 - 0.22, txt, fontsize=6.8, color=TEXT,
                        ha='left', va='top', linespacing=1.75)
            else:
                txt = '\n'.join(lines)
                ax.text(x + w / 2, y, txt, fontsize=6.9,
                        color=TEXT if row == 2 else color,
                        ha='center', va='center', linespacing=1.8,
                        fontweight='bold' if row == 2 else 'normal')

    # 箭头
    for i in range(3):
        x = x0 + i * (w + gap) + w
        ax.annotate('', xy=(x + gap + 0.01, 4.62), xytext=(x + 0.01, 4.62),
                    arrowprops=dict(arrowstyle='->', color=DIM, lw=1.3))

    ax.add_patch(FancyBboxPatch((1.0, 0.55), 11.0, 0.72,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 0.91, '唯一的闭环在第四步：控制成本产出的变更请求，回到估算和预算重新走一遍',
            fontsize=8.8, color=TEXT, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：估算精度 + 预算堆叠 ────────────────────────────────────────────────
def draw_estimate():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 6.95, '估算先说清精度，再谈数字', fontsize=21, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.5, '同样是「50 万」，粗略估算和确定估算的可信度差一个量级', fontsize=11.5,
            color=DIM, ha='center')

    # ── 左：三种精度
    ax.add_patch(FancyBboxPatch((0.45, 0.75), 6.1, 5.45,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GOLD, linewidth=1.6))
    ax.text(0.75, 5.85, '三种精度等级（AACE 口径）', fontsize=10, fontweight='bold',
            color=GOLD, ha='left', va='center')

    def px(pct):
        return 2.45 + (pct + 60) / 175.0 * 3.05

    # 轴线
    ax.plot([2.35, 5.62], [2.15, 2.15], color='#3d3226', lw=1.2)
    for p in (-50, 0, 25, 100):
        ax.plot([px(p), px(p)], [2.05, 2.25], color='#5a4a38', lw=1)
        ax.text(px(p), 1.92, f'{p:+d}%', fontsize=6.8, color=DIM, ha='center', va='center')
    ax.plot([px(0), px(0)], [2.2, 5.5], color='#5a4a38', lw=1, linestyle='--')

    rows = [
        ('粗略估算 ROM', -50, 100, '项目启动 · 要不要做', RED, 5.1),
        ('预算估算', -10, 25, '批准预算 · 立项用', GOLD, 4.05),
        ('确定估算', -5, 10, '招标签约 · 承诺用', GREEN, 3.0),
    ]
    for name, lo, hi, use, color, y in rows:
        ax.add_patch(FancyBboxPatch((px(lo), y - 0.2), px(hi) - px(lo), 0.4,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0, alpha=0.9))
        ax.text(0.68, y + 0.12, name, fontsize=8.4, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(0.68, y - 0.2, use, fontsize=6.8, color=DIM, ha='left', va='center')
        ax.text(px(hi) + 0.07, y, f'{lo:+d}~{hi:+d}%', fontsize=6.9, color=color,
                ha='left', va='center')

    ax.text(0.68, 1.05, '同一份需求，越往后精度越高 —— 但越往后改主意的代价也越大',
            fontsize=7.4, color=DIM, ha='left', va='center')

    # ── 右：预算堆叠
    ax.add_patch(FancyBboxPatch((6.75, 0.75), 5.8, 5.45,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.6))
    ax.text(7.05, 5.85, '成本基准是怎么堆出来的', fontsize=10, fontweight='bold',
            color=GREEN, ha='left', va='center')

    bx = 7.3; bw = 2.4
    blocks = [
        ('直接成本', '人日 · 采购 · 云资源 · 外包', 2.6, '#3b2f22', TEXT, 1.0),
        ('应急储备', '已知的未知 · 通常 10–15%', 0.7, COPPER, BG, 0),
        ('管理储备', '未知的未知 · 高层掌握', 0.65, PURPLE, BG, 0),
    ]
    y = 1.0
    for name, note, h, color, tcolor, _ in blocks:
        ax.add_patch(FancyBboxPatch((bx, y), bw, h,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(bx + bw / 2, y + h / 2 + 0.12, name, fontsize=9.2, fontweight='bold',
                color=tcolor if tcolor != BG or name == '直接成本' else BG,
                ha='center', va='center')
        ax.text(bx + bw / 2, y + h / 2 - 0.22, note, fontsize=6.8,
                color=tcolor if tcolor != BG else BG, ha='center', va='center')
        y += h + 0.08

    # 括号说明
    ax.annotate('', xy=(bx + bw + 0.15, 0.95), xytext=(bx + bw + 0.15, 4.33),
                arrowprops=dict(arrowstyle='|-|', color=GOLD, lw=1.4))
    ax.text(bx + bw + 0.3, 2.62, '成本基准\n= 直接成本\n+ 应急储备', fontsize=7.4,
            color=GOLD, ha='left', va='center', linespacing=1.6)

    ax.annotate('', xy=(bx + bw + 1.55, 0.95), xytext=(bx + bw + 1.55, 5.06),
                arrowprops=dict(arrowstyle='|-|', color=GREEN, lw=1.4))
    ax.text(bx + bw + 1.68, 3.0, '项目预算\n= 成本基准\n+ 管理储备', fontsize=7.4,
            color=GREEN, ha='left', va='center', linespacing=1.6)

    ax.text(7.05, 5.52, '基准一立，动它就要走变更', fontsize=7.4, color=DIM,
            ha='left', va='center')

    save(fig, 'estimate.png')


# ── 3：挣值四组指标 ───────────────────────────────────────────────────────
def draw_evm():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '四个量、四个比值、四个预测', fontsize=21, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.7, '挣值不是财务指标，是「花了钱，换回多少计划中的活」', fontsize=11.5,
            color=DIM, ha='center')

    cards = [
        ('基础三个量', GOLD, [
            ('PV 计划价值', '到今天应该完成多少'),
            ('EV 挣值', '实际完成的工作值多少'),
            ('AC 实际成本', '实际花了多少钱'),
        ]),
        ('两个偏差', COPPER, [
            ('CV = EV - AC', '成本偏差，负数是超支'),
            ('SV = EV - PV', '进度偏差，负数是落后'),
            ('注意', 'CV 为正也可能是少干了活'),
        ]),
        ('两个指数', BLUE, [
            ('CPI = EV / AC', '花 1 块换回多少价值，<1 超支'),
            ('SPI = EV / PV', '干一天的活值多少天，<1 落后'),
            ('组合判读', 'CPI<1 且 SPI<1：又慢又贵'),
        ]),
        ('四个预测', PURPLE, [
            ('EAC = BAC / CPI', '完工总成本预测'),
            ('ETC = EAC - AC', '还需要花多少'),
            ('VAC = BAC - EAC', '完工偏差，负数为超支'),
            ('TCPI', '剩余工作需要的成本效率'),
        ]),
    ]

    positions = [(0.45, 3.85), (6.65, 3.85), (0.45, 0.55), (6.65, 0.55)]
    sizes = [(5.9, 2.75), (5.9, 2.75), (5.9, 2.9), (5.9, 2.9)]

    for (title, color, items), (cx, cy), (cw, ch) in zip(cards, positions, sizes):
        ax.add_patch(FancyBboxPatch((cx, cy), cw, ch,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.add_patch(FancyBboxPatch((cx + 0.22, cy + ch - 0.62), 1.72, 0.4,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(cx + 1.08, cy + ch - 0.42, title, fontsize=8.6, fontweight='bold',
                color=BG, ha='center', va='center')

        iy = cy + ch - 0.95
        for name, desc in items:
            ax.text(cx + 0.25, iy, name, fontsize=8.4,
                    fontweight='bold' if '=' not in name else 'normal',
                    color=color if '=' not in name else TEXT,
                    ha='left', va='center')
            ax.text(cx + 2.05, iy, desc, fontsize=7.4, color=DIM, ha='left', va='center')
            iy -= 0.53

    save(fig, 'evm.png')


# ── 4：成本曲线 + 燃尽 ────────────────────────────────────────────────────
def draw_monitor():
    fig, ax = plt.subplots(figsize=(13, 6.9), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.9); ax.axis('off')

    ax.text(6.5, 6.5, '超支不是突然发生的，是慢慢裂开的', fontsize=21, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.05, '看三条线的间距，比看一个百分比有用得多', fontsize=11.5,
            color=DIM, ha='center')

    # 左：S 曲线
    ax.add_patch(FancyBboxPatch((0.45, 0.65), 7.3, 5.0,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GOLD, linewidth=1.5))
    ax.text(0.75, 5.28, '成本 S 曲线 · 第 6 周超支、进度也落后', fontsize=9.2,
            fontweight='bold', color=GOLD, ha='left', va='center')

    ax_in = fig.add_axes([0.192, 0.245, 0.383, 0.43])
    ax_in.set_facecolor(PANEL)
    weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    pv = [0, 4, 10, 20, 34, 50, 66, 81, 93, 102, 108, 112, 114]
    ev = [0, 3, 8, 16, 27, 40, 53, 65, 76, 85, 92, 97, 100]
    ac = [0, 5, 12, 23, 39, 56, 73, 88, 99, 107, 112, 115, 117]
    ax_in.plot(weeks, pv, color=BLUE, lw=2, label='PV 计划')
    ax_in.plot(weeks, ev, color=GREEN, lw=2, label='EV 挣值')
    ax_in.plot(weeks, ac, color=RED, lw=2, label='AC 实际')
    ax_in.fill_between(weeks, ev, ac, color=RED, alpha=0.16)
    ax_in.fill_between(weeks, ev, pv, color=GOLD, alpha=0.14)
    ax_in.axvline(6, color='#5a4a38', lw=1, linestyle='--')
    ax_in.annotate('CV=-20\n超支', xy=(6, 63), xytext=(6.9, 96),
                   fontsize=7, color=RED, ha='left',
                   arrowprops=dict(arrowstyle='->', color=RED, lw=1))
    ax_in.annotate('SV=-13\n落后', xy=(6, 46.5), xytext=(2.6, 78),
                   fontsize=7, color=GOLD, ha='left',
                   arrowprops=dict(arrowstyle='->', color=GOLD, lw=1))
    ax_in.set_xlim(0, 12.4); ax_in.set_ylim(0, 125)
    ax_in.tick_params(colors=DIM, labelsize=7)
    ax_in.set_xlabel('周', color=DIM, fontsize=7.5)
    ax_in.set_ylabel('万元', color=DIM, fontsize=7.5)
    for s in ax_in.spines.values():
        s.set_color('#3d3226')
    ax_in.grid(color='#2a2118', lw=0.8)
    leg = ax_in.legend(loc='upper left', fontsize=7, frameon=False)
    for t in leg.get_texts():
        t.set_color(TEXT)

    # 右：指标
    ax.add_patch(FancyBboxPatch((8.0, 0.65), 4.55, 5.0,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=RED, linewidth=1.5))
    ax.text(8.3, 5.28, '第 6 周判读', fontsize=9.2, fontweight='bold',
            color=RED, ha='left', va='center')

    metrics = [
        ('BAC 总预算', '114 万', DIM),
        ('CPI', '0.73', RED),
        ('EAC', '156 万', RED),
        ('VAC', '-42 万', RED),
        ('TCPI', '1.63', PURPLE),
    ]
    y = 4.85
    for name, val, color in metrics:
        ax.text(8.3, y, name, fontsize=8.2, color=TEXT, ha='left', va='center')
        ax.text(12.2, y, val, fontsize=10.5, fontweight='bold', color=color,
                ha='right', va='center')
        y -= 0.58

    ax.plot([8.3, 12.2], [1.62, 1.62], color='#3d3226', lw=1)
    ax.text(8.3, 1.35, 'TCPI 1.63 → 剩 41 万预算要干 67 万的活', fontsize=7.2,
            color=PURPLE, ha='left', va='center')
    ax.text(8.3, 1.0, '不砍范围，这个数字压不下来', fontsize=7.2,
            color=DIM, ha='left', va='center')

    save(fig, 'monitor.png')


# ── 5：四种群消息 ─────────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '成本消息只发四种，且都要带一个动作', fontsize=21, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.7, '只报数字的群消息，两周后没人看', fontsize=11.5, color=DIM, ha='center')

    cards = [
        ('成本预警', '每周一 09:30', RED, [
            'CPI 0.73，EAC 156 万，超支 42 万',
            '· 主因：联调返工 18 人日（原估 6）',
            '· 次要：云资源 3 台闲置未释放',
            '请 @张明 周三前确认砍哪些范围',
        ]),
        ('估算评审', '估算提交时', GOLD, [
            '本次估算 68 人日 · 52 万（区间 42–94）',
            '· 类比 3 个相似需求：41 / 55 / 78 万',
            '· 含 15% 应急储备，未含管理储备',
            '请确认按 68 万立项还是压到 52 万',
        ]),
        ('预算变更', '变更单提交时', COPPER, [
            'CN-018：新增对账模块，+12.5 万',
            '· 影响：成本基准 114 → 126.5 万',
            '· 对应范围：RTM 新增 4 条需求',
            '请 @李总 周五前审批，逾期按原基线执行',
        ]),
        ('成本健康度', '每月 1 日', GREEN, [
            '本月成本健康度 61 分（上月 68）',
            '· 预算消耗 38% · 工作量完成 31%',
            '· 不合理支出 2 笔，合计 1.8 万',
            '下月动作：压测环境改按量付费',
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
                color=BG, ha='center', va='center')
        ax.text(cx + 1.85, cy + ch - 0.47, freq, fontsize=7.0, color=DIM,
                ha='left', va='center')

        iy = cy + ch - 1.05
        for j, line in enumerate(lines):
            ax.text(cx + 0.28, iy, line, fontsize=7.4,
                    color=TEXT if j == 0 else '#c9bcac',
                    ha='left', va='center',
                    fontweight='bold' if j == 0 else 'normal')
            iy -= 0.42

    ax.text(6.5, 0.28, '每条消息四行以内：结论 / 依据 / 影响 / 要谁做什么',
            fontsize=8.2, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_estimate()
    draw_evm()
    draw_monitor()
    draw_message()
    print('✓ 全部生成完毕')
