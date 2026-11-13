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

BG = '#101322'
PANEL = '#1a1f33'
CARD = '#242b45'
TEXT = '#e8ecf5'
DIM = '#7c88a6'
SKY = '#38bdf8'
TEAL = '#2dd4bf'
GREEN = '#4ade80'
AMBER = '#fbbf24'
ROSE = '#fb7185'
PURPLE = '#c084fc'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：三个过程的 ITTO ─────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.0); ax.axis('off')

    ax.text(6.5, 6.72, '质量管理只有三个过程，但口径只定一次', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.38, '计划定口径、管理保过程、控制证结果——三者必须共用同一套度量',
            fontsize=11.5, color=DIM, ha='center')

    procs = [
        ('规划质量管理', '定口径', SKY),
        ('管理质量', '保过程', TEAL),
        ('控制质量', '证结果', GREEN),
    ]

    cols = [
        ['项目章程', '项目管理计划', '干系人登记册', '需求文件', '风险登记册', '事业环境因素'],
        ['质量管理计划', '质量度量指标', '质量报告', '组织过程资产'],
        ['项目管理计划', '质量度量指标', '测试与评估文件', '可交付成果', '批准的变更请求'],
    ]
    techs = [
        ['成本效益分析', '质量成本 COQ', '七种基本质量工具', '标杆对照 · 实验设计', '会议'],
        ['核对单', '根本原因分析', '过程分析', '质量审计', '问题解决'],
        ['检查', '统计抽样', '绩效审查', '根本原因分析'],
    ]
    outs = [
        ['质量管理计划', '质量度量指标'],
        ['质量报告', '测试与评估文件', '变更请求'],
        ['质量控制测量结果', '核实的可交付成果', '工作绩效信息', '变更请求'],
    ]

    x0 = 0.95; w = 3.62; gap = 0.15
    for i, (name, tag, color) in enumerate(procs):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 5.45), w, 0.68,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2 - 0.28, 5.79, name, fontsize=10.5, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(x + w - 0.28, 5.79, tag, fontsize=7.6, color=BG,
                ha='right', va='center')

    row_labels = ['输入', '技术', '输出']
    row_y = [4.62, 3.33, 2.16]
    row_h = [1.42, 0.94, 0.94]

    for label, y in zip(row_labels, row_y):
        ax.text(0.45, y, label, fontsize=10, fontweight='bold', color=SKY,
                ha='center', va='center')

    for i in range(3):
        x = x0 + i * (w + gap)
        for row, (data, y, h) in enumerate(zip([cols[i], techs[i], outs[i]], row_y, row_h)):
            color = [SKY, TEAL, GREEN][row]
            ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h,
                                        boxstyle='round,pad=0.03,rounding_size=0.07',
                                        facecolor=PANEL if row != 1 else CARD,
                                        edgecolor='#2e3852', linewidth=1))
            lines = [d for d in data if d]
            txt = '\n'.join(lines)
            if row == 0:
                ax.text(x + 0.16, y + h / 2 - 0.18, txt, fontsize=6.6, color=TEXT,
                        ha='left', va='top', linespacing=1.35)
            else:
                ax.text(x + w / 2, y, txt, fontsize=6.7,
                        color=TEXT if row == 2 else color,
                        ha='center', va='center', linespacing=1.45,
                        fontweight='bold' if row == 2 else 'normal')

    for i in range(2):
        x = x0 + i * (w + gap) + w
        ax.annotate('', xy=(x + gap + 0.01, 4.62), xytext=(x + 0.01, 4.62),
                    arrowprops=dict(arrowstyle='->', color=DIM, lw=1.3))

    ax.add_patch(FancyBboxPatch((1.0, 0.52), 11.0, 0.68,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 0.86, '唯一的闭环在第三步：控制质量产出的变更请求，回到管理质量与计划重新校准口径',
            fontsize=8.8, color=TEXT, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：质量成本四象限 + 1-10-100 ──────────────────────────────────────────
def draw_coq():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 6.95, '质量不是免费的，但省质量的代价更贵', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.50, '把质量成本记成四类，才知道钱该从哪挪到哪',
            fontsize=11.5, color=DIM, ha='center')

    # ── 左：四类质量成本
    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.1, 5.65,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=SKY, linewidth=1.6))
    ax.text(0.75, 5.92, '质量成本 COQ · 四类支出', fontsize=10, fontweight='bold',
            color=SKY, ha='left', va='center')

    rows = [
        ('预防成本', 'Prevention', '培训 · 评审 · 自动化 · 编码规范', '最便宜', GREEN),
        ('评估成本', 'Appraisal', '测试 · 审计 · 检查 · 度量', '必要支出', TEAL),
        ('内部失败', 'Internal failure', '返工 · 缺陷修复 · 重新测试', '已变贵', AMBER),
        ('外部失败', 'External failure', '线上事故 · 赔付 · 口碑流失', '最昂贵', ROSE),
    ]
    for idx, (name, en, ex, tag, color) in enumerate(rows):
        y = 4.55 - idx * 1.10
        ax.add_patch(FancyBboxPatch((0.75, y), 5.5, 0.95,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=CARD, edgecolor='#2e3852', linewidth=1))
        ax.add_patch(FancyBboxPatch((0.75, y + 0.08), 0.09, 0.79,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(0.99, y + 0.63, name, fontsize=9.4, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(0.99, y + 0.30, en, fontsize=6.6, color=DIM, ha='left', va='center')
        ax.text(2.35, y + 0.63, ex, fontsize=7.0, color='#c3ccdd', ha='left', va='center')
        ax.text(6.05, y + 0.48, tag, fontsize=8.2, fontweight='bold', color=color,
                ha='right', va='center')

    ax.text(0.75, 0.82, '前两类是「把钱花在前面」，后两类是「为没花前面的钱买单」',
            fontsize=7.6, color=DIM, ha='left', va='center')

    # ── 右：1-10-100 法则
    ax.add_patch(FancyBboxPatch((6.75, 0.55), 5.8, 5.65,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ROSE, linewidth=1.6))
    ax.text(7.05, 5.92, '1-10-100 法则', fontsize=10, fontweight='bold',
            color=ROSE, ha='left', va='center')
    ax.text(7.05, 5.56, '同一个缺陷，越晚发现，代价越贵', fontsize=7.6,
            color=DIM, ha='left', va='center')

    bars = [
        ('需求评审阶段发现', 1.15, '1x', GREEN, 4.55),
        ('开发与测试阶段发现', 2.55, '10x', AMBER, 3.35),
        ('上线之后才被发现', 4.50, '100x', ROSE, 2.15),
    ]
    for label, width, mult, color, y in bars:
        ax.text(7.05, y + 0.72, label, fontsize=8.2, color=TEXT, ha='left', va='center')
        ax.add_patch(FancyBboxPatch((7.05, y), width, 0.58,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0, alpha=0.92))
        ax.text(7.05 + width - 0.12, y + 0.29, mult, fontsize=9.6, fontweight='bold',
                color=BG, ha='right', va='center')

    ax.plot([7.05, 12.2], [1.55, 1.55], color='#2e3852', lw=1)
    ax.text(7.05, 1.28, '评审多花的一小时，抵得上线上修一天', fontsize=8.4,
            color=ROSE, ha='left', va='center')
    ax.text(7.05, 0.95, '质量预算该往左边挪，而不是往右边补', fontsize=7.6,
            color=DIM, ha='left', va='center')

    save(fig, 'coq.png')


# ── 3：控制图 + 四层度量 ──────────────────────────────────────────────────
def draw_control():
    fig, ax = plt.subplots(figsize=(13, 6.9), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.9); ax.axis('off')

    ax.text(6.5, 6.50, '控制图看的不是单点，是过程有没有偏移', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.05, '两种失控形态：点越界、点在中心线同侧连成串',
            fontsize=11.5, color=DIM, ha='center')

    # ── 左：控制图
    ax.add_patch(FancyBboxPatch((0.45, 0.65), 7.1, 5.00,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=SKY, linewidth=1.5))
    ax.text(0.75, 5.28, '控制图 · 缺陷数 / 千行代码（连续 20 个批次）', fontsize=9.0,
            fontweight='bold', color=SKY, ha='left', va='center')

    gx0, gx1 = 1.05, 6.95
    gy0, gy1 = 1.55, 4.45
    vals = [4.8, 5.2, 4.5, 5.6, 4.9, 5.1, 4.6, 5.1, 5.2, 5.4,
            5.5, 5.7, 5.6, 5.8, 8.2, 5.3, 4.7, 5.0, 4.9, 5.1]
    n = len(vals)
    UCL, CL, LCL = 7.6, 5.0, 2.4

    def mx(i):
        return gx0 + i / (n - 1.0) * (gx1 - gx0)

    def my(v):
        return gy0 + (v - 2.0) / 7.0 * (gy1 - gy0)

    xs = [mx(i) for i in range(n)]
    ys = [my(v) for v in vals]

    ax.add_patch(FancyBboxPatch((gx0 - 0.12, gy0 - 0.12),
                                (gx1 - gx0) + 0.24, (gy1 - gy0) + 0.24,
                                boxstyle='round,pad=0.01,rounding_size=0.05',
                                facecolor='#151a2b', edgecolor='#2e3852', linewidth=1))
    ax.fill_between([gx0, gx1], my(LCL), my(UCL), color='#1d2a44', alpha=0.55)

    ax.plot([gx0, gx1], [my(UCL), my(UCL)], color=ROSE, lw=1.3, linestyle='--')
    ax.plot([gx0, gx1], [my(LCL), my(LCL)], color=ROSE, lw=1.3, linestyle='--')
    ax.plot([gx0, gx1], [my(CL), my(CL)], color=TEAL, lw=1.3)
    ax.text(gx1 + 0.10, my(UCL), 'UCL', fontsize=7.0, color=ROSE, ha='left', va='center')
    ax.text(gx1 + 0.10, my(CL), 'CL', fontsize=7.0, color=TEAL, ha='left', va='center')
    ax.text(gx1 + 0.10, my(LCL), 'LCL', fontsize=7.0, color=ROSE, ha='left', va='center')

    ax.plot(xs, ys, color=SKY, lw=1.6, zorder=3)
    for i, (xv, yv) in enumerate(zip(xs, ys)):
        c = ROSE if (vals[i] > UCL or vals[i] < LCL) else (AMBER if 7 <= i <= 13 else SKY)
        ax.plot([xv], [yv], marker='o', markersize=4.6, color=c, zorder=4)

    ax.annotate('越界', xy=(xs[14], ys[14]), xytext=(4.55, 4.62),
                fontsize=7.4, color=ROSE, ha='right', va='center',
                arrowprops=dict(arrowstyle='->', color=ROSE, lw=1.1))

    ax.text(gx0, 1.13, '判读 1  连续 7 点在中心线同侧 → 过程已偏移，查变更与人员',
            fontsize=7.1, color=AMBER, ha='left', va='center')
    ax.text(gx0, 0.85, '判读 2  单点超出 UCL / LCL → 异常，立即定位当批产出',
            fontsize=7.1, color=ROSE, ha='left', va='center')

    # ── 右：四层度量
    ax.add_patch(FancyBboxPatch((7.85, 0.65), 4.7, 5.00,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.5))
    ax.text(8.15, 5.28, '质量度量要分四层', fontsize=9.0, fontweight='bold',
            color=GREEN, ha='left', va='center')

    layers = [
        ('过程度量', '评审覆盖率 · 缺陷注入率 · 评审通过率', SKY),
        ('产出度量', '缺陷密度 · 用例通过率 · 需求覆盖度', TEAL),
        ('逃逸度量', '缺陷逃逸率 · 线上事故数 · 平均修复时长', AMBER),
        ('体验度量', 'NPS · 可用性 · 投诉量 · 首次解决率', PURPLE),
    ]
    for idx, (name, ex, color) in enumerate(layers):
        y = 4.25 - idx * 0.95
        ax.add_patch(FancyBboxPatch((8.15, y), 4.1, 0.85,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=CARD, edgecolor='#2e3852', linewidth=1))
        ax.text(8.32, y + 0.58, name, fontsize=8.6, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(8.32, y + 0.26, ex, fontsize=6.7, color='#c3ccdd', ha='left', va='center')

    ax.text(8.15, 1.02, '四层缺一层，质量就只剩一句「差不多」', fontsize=7.4,
            color=DIM, ha='left', va='center')

    save(fig, 'control.png')


# ── 4：缺陷来源 + 逃逸率与 DoD ────────────────────────────────────────────
def draw_defect():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.80, '缺陷的根因，大多不在写代码那一步', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.35, '先按来源归因，再决定改哪里——否则修完还会再来',
            fontsize=11.5, color=DIM, ha='center')

    # ── 左：缺陷来源分布
    ax.add_patch(FancyBboxPatch((0.45, 0.65), 6.2, 5.30,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ROSE, linewidth=1.5))
    ax.text(0.75, 5.60, '缺陷来源分布', fontsize=9.6, fontweight='bold',
            color=ROSE, ha='left', va='center')
    ax.text(0.75, 5.30, '近三个月 41 个 P0 / P1 缺陷归因', fontsize=7.2,
            color=DIM, ha='left', va='center')

    items = [
        ('需求理解偏差', 38, ROSE),
        ('编码实现错误', 27, AMBER),
        ('接口 / 集成不一致', 19, SKY),
        ('测试环境差异', 11, TEAL),
        ('设计遗漏', 5, PURPLE),
    ]
    scale = 2.70 / 38.0
    for idx, (name, pct, color) in enumerate(items):
        y = 4.55 - idx * 0.77
        ax.text(0.78, y + 0.22, name, fontsize=7.8, color=TEXT, ha='left', va='center')
        ax.add_patch(FancyBboxPatch((2.62, y), 2.70, 0.44,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor='#151a2b', edgecolor='#2e3852', linewidth=0))
        ax.add_patch(FancyBboxPatch((2.62, y), pct * scale, 0.44,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor=color, edgecolor=color, linewidth=0, alpha=0.9))
        ax.text(2.62 + pct * scale + 0.10, y + 0.22, f'{pct}%', fontsize=7.8,
                fontweight='bold', color=color, ha='left', va='center')

    ax.text(0.78, 1.10, '38% 的根因在需求——这时候修代码，是在治症状', fontsize=7.6,
            color=ROSE, ha='left', va='center')

    # ── 右：两个口径
    ax.add_patch(FancyBboxPatch((6.85, 3.72), 5.7, 2.23,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=AMBER, linewidth=1.5))
    ax.text(7.15, 5.52, '缺陷逃逸率', fontsize=9.4, fontweight='bold', color=AMBER,
            ha='left', va='center')
    ax.text(7.15, 5.14, '逃逸率 = 上线后发现缺陷 / 全部缺陷', fontsize=7.8,
            color=TEXT, ha='left', va='center')
    ax.text(7.15, 4.76, '目标 < 15%；连续两月 > 25% 升级为专项', fontsize=7.2,
            color='#c3ccdd', ha='left', va='center')
    ax.text(7.15, 4.42, '只看缺陷总数看不出问题，这个比值才看得见「漏出去多少」',
            fontsize=6.9, color=DIM, ha='left', va='center')
    ax.text(7.15, 4.02, '禁止用于跨团队排名——口径不同，比出来没意义', fontsize=6.9,
            color=ROSE, ha='left', va='center')

    ax.add_patch(FancyBboxPatch((6.85, 0.65), 5.7, 2.85,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.5))
    ax.text(7.15, 3.14, 'DoD 完成定义 · 四条硬线', fontsize=9.4, fontweight='bold',
            color=GREEN, ha='left', va='center')
    dod = [
        '单元测试覆盖 >= 70%，关键路径 >= 90%',
        'P0 / P1 缺陷全部关闭，或已书面接受',
        '代码评审留痕，可回溯到需求编号',
        '验收标准可测，「良好 / 稳定」这类词不算',
    ]
    for idx, line in enumerate(dod):
        y = 2.80 - idx * 0.46
        ax.text(7.15, y, '-', fontsize=9, color=GREEN, ha='left', va='center')
        ax.text(7.38, y, line, fontsize=7.3, color=TEXT, ha='left', va='center')

    ax.text(7.15, 0.98, 'DoD 不是写给 QA 的，是写给「谁能说完成」的', fontsize=7.2,
            color=DIM, ha='left', va='center')

    save(fig, 'defect.png')


# ── 5：四种群消息 ─────────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '质量消息只发四种，都要落到一个动作', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.70, '只报「质量良好」的群消息，两周后没人看',
            fontsize=11.5, color=DIM, ha='center')

    cards = [
        ('质量预警', '每周一 09:30', ROSE, [
            '本周缺陷密度 4.2/KLOC，逃逸率 22%',
            '· 主因：需求评审缺口 7 条，未闭环',
            '· 次要：联调环境版本不一致',
            '请 @张明 周三前定评审补做计划',
        ]),
        ('验收评审', 'DoD 评审时', AMBER, [
            '迭代 3.2 验收：DoD 5 / 7 达成',
            '· 未达成：用例覆盖 62%（目标 70%）',
            '· 未达成：P1 缺陷 2 个未关闭',
            '请确认是延期一周还是降级发布',
        ]),
        ('质量审计', '每月一次', TEAL, [
            '审计发现 3 项过程偏差',
            '· 2 个模块未走代码评审',
            '· 1 次变更未同步更新测试用例',
            '请 @李工 两周内提交整改证据',
        ]),
        ('质量健康度', '每月 1 日', GREEN, [
            '本月质量健康度 74 分（上月 68）',
            '· 逃逸率 12% · 评审覆盖 91%',
            '· 外部失败成本 0',
            '下月动作：补自动化回归 30 条',
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
                    color=TEXT if j == 0 else '#c3ccdd',
                    ha='left', va='center',
                    fontweight='bold' if j == 0 else 'normal')
            iy -= 0.42

    ax.text(6.5, 0.28, '每条消息四行以内：结论 / 依据 / 影响 / 要谁做什么',
            fontsize=8.2, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_coq()
    draw_control()
    draw_defect()
    draw_message()
    print('✓ 全部生成完毕')
