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

BG = '#14110c'
PANEL = '#1f1a13'
CARD = '#2a231a'
TEXT = '#f2ede2'
DIM = '#9a8f7c'
GOLD = '#d9a441'
COPPER = '#c2703f'
TEAL = '#4fb3a5'
BLUE = '#5b8fd6'
ROSE = '#d9698a'
GREEN = '#7fb069'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：三个过程 ────────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 6.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.0)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 5.62, '采购管理只有三个过程，但最贵的错误在第一步', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.28, '合同类型选错了，后面所有管理动作都在补一个结构性的窟窿',
            fontsize=11.5, color=DIM, ha='center')

    procs = [
        ('01', '规划采购管理', '定策略', GOLD,
         ['章程 · 商业文件 · 需求文件', '风险登记册 · 干系人登记册', ''],
         ['自制或外购分析 · 专家判断', '市场调研 · 数据收集', '会议'],
         ['采购管理计划 · 采购策略', '招标文件 · 供方选择标准', '自制或外购决策']),
        ('02', '实施采购', '选供方', TEAL,
         ['采购管理计划 · 招标文件', '供方选择标准 · 卖方建议书', ''],
         ['投标人会议 · 建议书评估', '谈判 · 广告 · 数据分析', ''],
         ['选定的卖方 · 协议（合同）', '变更请求 · 项目文件更新', '']),
        ('03', '控制采购', '管履约', BLUE,
         ['合同 · 采购文档', '批准的变更 · 工作绩效数据', ''],
         ['绩效审查 · 索赔管理', '检查 · 审计 · 数据分析', ''],
         ['采购关闭 · 工作绩效信息', '变更请求 · 文件更新', '']),
    ]

    cw, gap = 4.02, 0.20
    x0 = (13 - (3 * cw + 2 * gap)) / 2
    for i, (num, name, verb, c, ins, techs, outs) in enumerate(procs):
        x = x0 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, 0.72), cw, 4.20,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=CARD, edgecolor=c + '66', linewidth=1.4))
        ax.add_patch(FancyBboxPatch((x, 4.28), cw, 0.64,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=c, edgecolor=c, linewidth=0))
        ax.text(x + 0.26, 4.60, num, fontsize=13, fontweight='bold',
                color='#14110c', ha='left', va='center')
        ax.text(x + 0.72, 4.60, name, fontsize=10.4, fontweight='bold',
                color='#14110c', ha='left', va='center')
        ax.text(x + cw - 0.24, 4.60, verb, fontsize=7.4,
                color='#14110c', ha='right', va='center', alpha=0.75)

        blocks = [('输入', ins, GOLD, 4.06, [3.78, 3.52, 3.26]),
                  ('技术', techs, TEAL, 2.94, [2.66, 2.40, 2.14]),
                  ('输出', outs, BLUE, 1.82, [1.54, 1.28, 1.02])]
        for label, lines, lc, ly, ys in blocks:
            ax.text(x + 0.24, ly, label, fontsize=7.0, fontweight='bold',
                    color=lc, ha='left', va='center')
            for txt, yy in zip(lines, ys):
                if txt:
                    ax.text(x + 0.86, yy, txt, fontsize=6.8, color='#c8bfae',
                            ha='left', va='center')

    ax.text(6.5, 0.40, '第 2、3 个过程可以外包给流程，第 1 个过程只能自己做决定',
            fontsize=7.6, color=DIM, ha='center', va='center')
    save(fig, 'pipeline.png')


# ── 2：合同类型与风险分配 ──────────────────────────────────────────────
def draw_contract():
    fig, ax = plt.subplots(figsize=(13, 7.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.4)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 6.05, '合同类型不是法律条文，是一张风险分配表', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.72, '往左走，不确定性留给买方；往右走，不确定性卖给卖方',
            fontsize=11.5, color=DIM, ha='center')

    items = [
        ('成本加酬金', 'CPPC', ROSE, '买方几乎全担', ['需求极不明确', '探索型研发'],
         '最灵活', ['成本不封顶', '越拖越贵']),
        ('成本加激励', 'CPIF', '#cf8a70', '买方为主', ['需求模糊', '长期合作'],
         '灵活', ['激励公式', '没定清楚']),
        ('工料合同', 'T&M', GOLD, '双方各半', ['人力增援', '短期救火'],
         '灵活需上限', ['没有封顶', '就是无底洞']),
        ('总价加激励', 'FPIF', '#7f9fc0', '卖方为主', ['需求较清晰', '有调整空间'],
         '受限', ['验收标准', '写虚就扯皮']),
        ('固定总价', 'FFP', BLUE, '卖方几乎全担', ['需求完全明确', '范围冻得住'],
         '最不灵活', ['卖方亏了', '会偷工减料']),
    ]

    cw, gap = 2.32, 0.24
    x0 = (13 - (5 * cw + 4 * gap)) / 2

    # 顶部风险谱
    band_y, band_h = 4.94, 0.26
    for i, (_, _, c, _, _, _, _) in enumerate(items):
        bx = x0 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((bx, band_y), cw, band_h,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor=c, edgecolor=c, linewidth=0, alpha=0.55))
    ax.text(x0 + 0.02, band_y + band_h + 0.20, '买方承担超支风险', fontsize=7.6,
            color=ROSE, ha='left', va='center', fontweight='bold')
    ax.text(13 - x0 - 0.02, band_y + band_h + 0.20, '卖方承担超支风险', fontsize=7.6,
            color=BLUE, ha='right', va='center', fontweight='bold')

    for i, (name, abbr, c, risk, scenes, flex, pits) in enumerate(items):
        x = x0 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, 0.85), cw, 3.85,
                                    boxstyle='round,pad=0.04,rounding_size=0.10',
                                    facecolor=CARD, edgecolor=c + '55', linewidth=1.2))
        ax.text(x + 0.20, 4.42, name, fontsize=9.2, fontweight='bold', color=c,
                ha='left', va='center')
        ax.text(x + 0.20, 4.12, abbr, fontsize=6.8, color=DIM, ha='left', va='center',
                fontfamily='monospace')

        ax.text(x + 0.20, 3.74, '风险归属', fontsize=6.6, color=DIM, ha='left', va='center')
        ax.text(x + 0.20, 3.48, risk, fontsize=7.2, fontweight='bold', color=TEXT,
                ha='left', va='center')

        ax.text(x + 0.20, 3.12, '适用场景', fontsize=6.6, color=DIM, ha='left', va='center')
        for j, s in enumerate(scenes):
            ax.text(x + 0.20, 2.88 - j * 0.24, s, fontsize=7.0, color='#c8bfae',
                    ha='left', va='center')

        ax.text(x + 0.20, 2.28, '变更灵活性', fontsize=6.6, color=DIM, ha='left', va='center')
        ax.text(x + 0.20, 2.02, flex, fontsize=7.2, fontweight='bold', color=TEXT,
                ha='left', va='center')

        ax.text(x + 0.20, 1.62, '常见坑', fontsize=6.6, color=DIM, ha='left', va='center')
        for j, p in enumerate(pits):
            ax.text(x + 0.20, 1.38 - j * 0.24, p, fontsize=7.0, color=ROSE,
                    ha='left', va='center')

    ax.text(6.5, 0.46, '选合同类型的本质：把不确定性交给更能承担它的一方 —— 但对方一定会收溢价',
            fontsize=8.0, color=DIM, ha='center', va='center')
    save(fig, 'contract.png')


# ── 3：自制或外购 ──────────────────────────────────────────────────────
def draw_makebuy():
    fig, ax = plt.subplots(figsize=(13, 6.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.4)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 6.05, '自制还是外购，答案是一条交叉线', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.72, '固定投入 vs 单件价格，交点就是决策点',
            fontsize=11.5, color=DIM, ha='center')

    # 左：成本曲线
    ax.add_patch(FancyBboxPatch((0.42, 0.62), 7.02, 4.80,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GOLD + '88', linewidth=1.4))
    ax.text(0.72, 5.10, '年总成本 · 按用量', fontsize=9.0, fontweight='bold',
            color=GOLD, ha='left', va='center')

    gx0, gx1 = 1.72, 7.02
    gy0, gy1 = 1.55, 4.72

    def mx(v):
        return gx0 + v / 1200.0 * (gx1 - gx0)

    def my(c):
        return gy0 + c / 900000.0 * (gy1 - gy0)

    # 网格
    for c in [0, 200000, 400000, 600000, 800000]:
        ax.plot([gx0, gx1], [my(c), my(c)], color='#3a3226', lw=0.7, zorder=1)
        ax.text(gx0 - 0.10, my(c), str(int(c / 10000)), fontsize=6.4, color=DIM,
                ha='right', va='center')
    ax.text(gx0 - 0.55, (gy0 + gy1) / 2, '万元', fontsize=6.6, color=DIM,
            rotation=90, ha='center', va='center')

    for v in [0, 300, 600, 900, 1200]:
        ax.text(mx(v), gy0 - 0.18, str(v), fontsize=6.4, color=DIM,
                ha='center', va='center')
    ax.text((gx0 + gx1) / 2, gy0 - 0.42, '年用量（件）', fontsize=6.8, color=DIM,
            ha='center', va='center')

    # 自制：30 万固定 + 250/件
    xs = list(range(0, 1201, 20))
    ax.plot([mx(v) for v in xs], [my(300000 + 250 * v) for v in xs],
            color=TEAL, lw=2.2, zorder=3)
    # 外购：650/件
    ax.plot([mx(v) for v in xs], [my(650 * v) for v in xs],
            color=COPPER, lw=2.2, zorder=3)

    # 交点 750
    ax.plot([mx(750), mx(750)], [gy0, my(487500)], color=GOLD, lw=1.1,
            linestyle='--', zorder=2)
    ax.scatter([mx(750)], [my(487500)], s=46, color=GOLD, zorder=5)
    ax.text(mx(750) + 0.14, my(487500) - 0.20, '平衡点 750 件', fontsize=7.2,
            color=GOLD, fontweight='bold', ha='left', va='top')

    ax.text(mx(1080), my(300000 + 250 * 1080) - 0.26, '自制', fontsize=7.6,
            color=TEAL, fontweight='bold', ha='center', va='top')
    ax.text(mx(1080), my(650 * 1080) + 0.16, '外购', fontsize=7.6,
            color=COPPER, fontweight='bold', ha='center', va='bottom')

    ax.text(0.72, 0.80, '用量越大，固定投入越划算；用量不足，外购更省',
            fontsize=7.0, color=DIM, ha='left', va='center')

    # 右：决策要点
    ax.add_patch(FancyBboxPatch((7.66, 0.62), 4.92, 4.80,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=TEAL + '88', linewidth=1.4))
    ax.text(7.96, 5.10, '但成本只是第一个问题', fontsize=9.0, fontweight='bold',
            color=TEAL, ha='left', va='center')

    points = [
        ('战略', '核心能力不外购', '今天为省钱外包，明天为拿回来付双倍', TEAL),
        ('口径', '算总成本不算单价', '管理成本、集成成本、切换成本都要算进去', GOLD),
        ('锁定', '切换成本等于议价权', '越难换供应商，越容易被涨价', ROSE),
        ('风险', '外购的风险要入册', '供应商风险不是采购的事，是项目的事', BLUE),
    ]
    for i, (tag, title, desc, c) in enumerate(points):
        y = 4.50 - i * 0.88
        ax.add_patch(FancyBboxPatch((7.92, y - 0.66), 4.40, 0.76,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=c + '44', linewidth=1.0))
        ax.text(8.08, y - 0.04, tag, fontsize=6.8, fontweight='bold', color=c,
                ha='left', va='center')
        ax.text(8.08 + 0.52, y - 0.04, title, fontsize=7.6, fontweight='bold',
                color=TEXT, ha='left', va='center')
        ax.text(8.08, y - 0.38, desc, fontsize=6.6, color=DIM, ha='left', va='center')

    ax.text(7.96, 0.86, '外购省下的是钱，付出的是控制权', fontsize=7.0,
            color=DIM, ha='left', va='center')
    save(fig, 'makebuy.png')


# ── 4：供方选择与绩效监控 ──────────────────────────────────────────────
def draw_vendor():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 6.25, '加权总分差不多时，要看单维度差在哪', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.92, '总分把差异平均掉了，而差异才是谈判筹码',
            fontsize=11.5, color=DIM, ha='center')

    # 左：加权评分
    ax.add_patch(FancyBboxPatch((0.42, 0.58), 6.90, 4.98,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GOLD + '88', linewidth=1.4))
    ax.text(0.72, 5.30, '供方选择标准 · 加权评分（0-100）', fontsize=9.0,
            fontweight='bold', color=GOLD, ha='left', va='center')

    ax.add_patch(FancyBboxPatch((5.22, 5.22), 0.16, 0.14,
                                boxstyle='round,pad=0.01,rounding_size=0.03',
                                facecolor=TEAL, edgecolor=TEAL, linewidth=0))
    ax.text(5.45, 5.29, 'A 供应商', fontsize=6.6, color=DIM, ha='left', va='center')
    ax.add_patch(FancyBboxPatch((6.10, 5.22), 0.16, 0.14,
                                boxstyle='round,pad=0.01,rounding_size=0.03',
                                facecolor=BLUE, edgecolor=BLUE, linewidth=0))
    ax.text(6.33, 5.29, 'B 供应商', fontsize=6.6, color=DIM, ha='left', va='center')

    rows = [('技术方案', 30, 88, 70), ('商务报价', 25, 62, 95), ('交付能力', 20, 75, 72),
            ('服务响应', 15, 80, 60), ('合规资质', 10, 90, 80)]
    bx0, bscale = 2.95, 0.042
    for i, (name, w, a, b) in enumerate(rows):
        y = 4.66 - i * 0.82
        ax.text(0.74, y + 0.06, name, fontsize=7.2, color='#c8bfae', ha='left', va='center')
        ax.text(0.74, y - 0.20, f'权重 {w}%', fontsize=6.2, color=DIM, ha='left', va='center')
        ax.add_patch(FancyBboxPatch((bx0, y + 0.02), a * bscale, 0.20,
                                    boxstyle='round,pad=0.01,rounding_size=0.02',
                                    facecolor=TEAL, edgecolor=TEAL, linewidth=0, alpha=0.92))
        ax.text(bx0 + a * bscale + 0.07, y + 0.12, str(a), fontsize=6.4, color=TEAL,
                ha='left', va='center')
        ax.add_patch(FancyBboxPatch((bx0, y - 0.24), b * bscale, 0.20,
                                    boxstyle='round,pad=0.01,rounding_size=0.02',
                                    facecolor=BLUE, edgecolor=BLUE, linewidth=0, alpha=0.92))
        ax.text(bx0 + b * bscale + 0.07, y - 0.14, str(b), fontsize=6.4, color=BLUE,
                ha='left', va='center')

    ax.text(0.74, 0.86, '加权总分：A 77.9 / B 76.2 —— 只差 1.7 分，但技术方案差 18 分',
            fontsize=7.2, color=GOLD, ha='left', va='center')

    # 右：履约监控
    ax.add_patch(FancyBboxPatch((7.52, 0.58), 5.06, 4.98,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=TEAL + '88', linewidth=1.4))
    ax.text(7.82, 5.30, '控制采购 · 四个履约指标', fontsize=9.0,
            fontweight='bold', color=TEAL, ha='left', va='center')

    metrics = [('交付准时率', '92%', '18 批中 2 批延迟', GREEN),
               ('质量合格率', '98.4%', '退回 3 件，均为包装', TEAL),
               ('平均响应时效', '6.2h', 'SLA 约定 4h，已连续两周超标', ROSE),
               ('成本偏差', '+3.1%', '汇率波动导致，可索赔', GOLD)]
    for i, (name, val, note, c) in enumerate(metrics):
        y = 4.66 - i * 0.96
        ax.add_patch(FancyBboxPatch((7.78, y - 0.74), 4.54, 0.86,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=c + '44', linewidth=1.0))
        ax.text(7.94, y - 0.10, name, fontsize=7.0, color='#c8bfae', ha='left', va='center')
        ax.text(12.14, y - 0.10, val, fontsize=9.0, fontweight='bold', color=c,
                ha='right', va='center')
        ax.text(7.94, y - 0.48, note, fontsize=6.4, color=DIM, ha='left', va='center')

    ax.text(7.82, 0.86, '两个指标连续两期越线 = 触发合同条款，不是再催一次',
            fontsize=7.0, color=DIM, ha='left', va='center')
    save(fig, 'vendor.png')


# ── 5：四类群消息 ──────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 7.15, '采购消息只有四类，其余都是过程噪音', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.72, '决策要授权、招标要进度、履约要预警、验收要付款',
            fontsize=11.5, color=DIM, ha='center')

    cards = [
        ('采购决策请求', '需要授权', GOLD, [
            '外购 CRM 三年 78 万，超项目预算 12 万',
            '· 自制方案 60 万，但需 2 名后端 3 个月',
            '· 外购可提前 6 周上线，含运维',
            '请 @张总 本周五前批复是否走外购']),
        ('招标进度同步', '流程节点', TEAL, [
            '支付网关选型：已收到 4 份建议书',
            '· 技术评审完成，商务评审周五',
            '· 预计 11-20 定标，12-01 签约',
            '请评委 @李工 @王工 周五 14:00 到场']),
        ('履约预警', '指标越线', ROSE, [
            '供应商 A 响应时效连续两周超标（6.2h / SLA 4h）',
            '· 交付准时率 92%，低于 95% 阈值',
            '· 已按合同第 8.2 条发出整改函',
            '请 @采购 周四前确认是否启用备选供应商']),
        ('验收与付款', '里程碑', BLUE, [
            '一期交付物验收通过，付款条件已满足',
            '· 验收单 VC-014 已签署，缺陷 0 遗留',
            '· 付款 32 万，账期 30 天',
            '请 @财务 本周内发起付款流程']),
    ]

    cw, ch = 6.06, 2.42
    for i, (title, tag, c, lines) in enumerate(cards):
        col, row = i % 2, i // 2
        x = 0.42 + col * (cw + 0.20)
        y = 3.90 - row * (ch + 0.22)
        ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=CARD, edgecolor=c + '66', linewidth=1.4))
        ax.add_patch(FancyBboxPatch((x + 0.24, y + ch - 0.62), 1.86, 0.40,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=c, edgecolor=c, linewidth=0))
        ax.text(x + 0.33, y + ch - 0.42, title, fontsize=8.0, fontweight='bold',
                color='#14110c', ha='left', va='center')
        ax.text(x + 2.24, y + ch - 0.42, tag, fontsize=6.6, color=DIM,
                ha='left', va='center')

        for j, ln in enumerate(lines):
            ax.text(x + 0.30, y + ch - 0.98 - j * 0.42, ln, fontsize=7.0,
                    color='#f2ede2' if j == 0 else '#c8bfae',
                    fontweight='bold' if j == 0 else 'normal',
                    ha='left', va='center')

    ax.text(6.5, 0.72, '每类都是四行：判断 / 依据 / 影响 / 要谁在什么时候做什么',
            fontsize=8.2, color=DIM, ha='center', va='center')
    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_contract()
    draw_makebuy()
    draw_vendor()
    draw_message()
    print('✓ 全部生成完毕')
