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

BG = '#12161c'
PANEL = '#1b222c'
CARD = '#252e3b'
TEXT = '#e8edf5'
DIM = '#7d8998'
LIME = '#a3e635'
SKY = '#38bdf8'
AMBER = '#fbbf24'
CORAL = '#fb7185'
PURPLE = '#a78bfa'
MINT = '#5eead4'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：六个过程 2x3 ITTO ──────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.0); ax.axis('off')

    ax.text(6.5, 6.72, '资源管理有六个过程，比质量管理多一倍', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.38, '但真正的分歧只有一个：人和工时，到底算不算同一种东西',
            fontsize=11.5, color=DIM, ha='center')

    procs = [
        ('规划资源管理', '定角色', LIME,
         '章程 · 项目管理计划 · 项目文件',
         'RACI · OBS/RBS · 团队章程',
         '资源管理计划 · 团队章程'),
        ('估算活动资源', '算需求', SKY,
         'WBS · 进度基准 · 资源日历',
         '自下而上 · 类比 · 参数估算',
         '资源需求 · RBS · 估算依据'),
        ('获取资源', '争人头', AMBER,
         '资源管理计划 · 资源日历',
         '多标准决策 · 谈判 · 预分派',
         '派工单 · 实物资源单 · 资源日历'),
        ('建设团队', '提能力', MINT,
         '资源日历 · 团队章程',
         '培训 · 团队建设 · 认可与奖励',
         '团队绩效评价 · 变更请求'),
        ('管理团队', '解冲突', PURPLE,
         '工作绩效报告 · 团队绩效评价',
         '冲突管理 · 情商 · 领导力',
         '变更请求 · 计划与文件更新'),
        ('控制资源', '盯负荷', CORAL,
         '工作绩效数据 · 资源日历',
         '绩效审查 · 趋势分析 · 问题解决',
         '工作绩效信息 · 变更请求'),
    ]

    w, gap = 3.95, 0.22
    x0 = (13 - (3 * w + 2 * gap)) / 2
    rows_y = [3.62, 0.90]
    ch = 2.35

    for idx, (name, tag, color, inp, tech, out) in enumerate(procs):
        col = idx % 3
        row = idx // 3
        x = x0 + col * (w + gap)
        y = rows_y[row]

        ax.add_patch(FancyBboxPatch((x, y), w, ch,
                                    boxstyle='round,pad=0.03,rounding_size=0.09',
                                    facecolor=PANEL, edgecolor='#2c3644', linewidth=1.2))
        ax.add_patch(FancyBboxPatch((x, y + ch - 0.60), w, 0.60,
                                    boxstyle='round,pad=0.03,rounding_size=0.09',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.20, y + ch - 0.30, f'{idx + 1:02d}', fontsize=8.4,
                fontweight='bold', color=BG, ha='left', va='center')
        ax.text(x + 0.62, y + ch - 0.30, name, fontsize=9.6, fontweight='bold',
                color='#10151a', ha='left', va='center')
        ax.text(x + w - 0.20, y + ch - 0.30, tag, fontsize=7.4, color='#10151a',
                ha='right', va='center')

        lines = [('输入', inp, SKY), ('技术', tech, MINT), ('输出', out, AMBER)]
        for j, (label, body, lc) in enumerate(lines):
            ly = y + ch - 1.02 - j * 0.46
            ax.text(x + 0.20, ly, label, fontsize=6.5, fontweight='bold', color=lc,
                    ha='left', va='center')
            ax.text(x + 0.68, ly, body, fontsize=6.3, color='#c7d0dd',
                    ha='left', va='center')

    ax.text(6.5, 0.38, '前三个过程解决「要什么人」，后三个解决「这些人怎么用」',
            fontsize=8.4, color=DIM, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：能力 vs 需求 + 三种处理手法 ────────────────────────────────────────
def draw_demand():
    fig, ax = plt.subplots(figsize=(13, 6.9), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.9); ax.axis('off')

    ax.text(6.5, 6.62, '总量够、结构不对，是资源管理最常见的假象', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.28, '把每个人一周的需求工时除以产能，才看得见真正的缺口',
            fontsize=11.5, color=DIM, ha='center')

    # 左：负荷条
    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.30, 5.45,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=LIME, linewidth=1.5))
    ax.text(0.75, 5.62, '团队周负荷 · 5 人 · 第 45 周', fontsize=9.2,
            fontweight='bold', color=LIME, ha='left', va='center')
    ax.text(0.75, 5.32, '灰白虚线 = 100% 产能，超出即超配', fontsize=7.0,
            color=DIM, ha='left', va='center')

    bx = 2.40
    scale = 3.45 / 150.0
    people = [('张明', 132, CORAL), ('李工', 108, AMBER), ('王工', 86, LIME),
              ('赵工', 74, SKY), ('陈工', 45, '#54627a')]

    for idx, (name, pct, color) in enumerate(people):
        y = 4.55 - idx * 0.74
        ax.text(0.80, y + 0.25, name, fontsize=8.0, color=TEXT, ha='left', va='center')
        ax.add_patch(FancyBboxPatch((bx, y), 3.45, 0.50,
                                    boxstyle='round,pad=0.01,rounding_size=0.05',
                                    facecolor='#151b24', edgecolor='#2c3644', linewidth=0))
        ax.add_patch(FancyBboxPatch((bx, y), pct * scale, 0.50,
                                    boxstyle='round,pad=0.01,rounding_size=0.05',
                                    facecolor=color, edgecolor=color, linewidth=0, alpha=0.92))
        ax.text(bx + pct * scale + 0.10, y + 0.25, f'{pct}%', fontsize=7.8,
                fontweight='bold', color=color if pct >= 100 else '#c7d0dd',
                ha='left', va='center')

    line_x = bx + 100 * scale
    ax.plot([line_x, line_x], [1.42, 5.05], color='#d6dde8', lw=1.1, linestyle='--', alpha=0.75)
    ax.text(line_x, 5.10, '100%', fontsize=6.8, color='#d6dde8', ha='center', va='bottom')

    ax.text(0.78, 1.10, '两人超配、一人半空 —— 平均值永远合格，个体永远不够',
            fontsize=7.6, color=CORAL, ha='left', va='center')

    # 右：三种手法
    ax.add_patch(FancyBboxPatch((6.95, 0.55), 5.60, 5.45,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=AMBER, linewidth=1.5))
    ax.text(7.25, 5.62, '三种处理手法，别混着用', fontsize=9.2, fontweight='bold',
            color=AMBER, ha='left', va='center')

    tricks = [
        ('资源平衡 Leveling', '调整任务的起止时间，可能改动关键路径', '目标：彻底消除超配，工期优先让步', CORAL),
        ('资源平滑 Smoothing', '只在浮动时间内削峰填谷，不动关键路径', '目标：削平波动，超配可能仍然存在', AMBER),
        ('解除关键资源瓶颈', '一个人卡住多条链路时，先解依赖再谈优化', '目标：把单点变成可替换的两点', MINT),
    ]
    for idx, (name, line1, line2, color) in enumerate(tricks):
        y = 4.35 - idx * 1.42
        ax.add_patch(FancyBboxPatch((7.25, y), 5.05, 1.24,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=CARD, edgecolor='#2c3644', linewidth=1))
        ax.add_patch(FancyBboxPatch((7.25, y + 0.10), 0.08, 1.04,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(7.48, y + 0.94, name, fontsize=8.6, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(7.48, y + 0.58, line1, fontsize=6.8, color='#c7d0dd', ha='left', va='center')
        ax.text(7.48, y + 0.26, line2, fontsize=6.6, color=DIM, ha='left', va='center')

    ax.text(7.25, 0.92, '先判断要不要改工期，再决定用哪一手', fontsize=7.4,
            color=DIM, ha='left', va='center')

    save(fig, 'demand.png')


# ── 3：负荷热力 + 四个监控指标 ────────────────────────────────────────────
def draw_heat():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.32, '负荷不是一个数字，是一张会动的热力图', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.98, '同一个平均利用率，可以是平稳推进，也可以是连续三周崩盘',
            fontsize=11.5, color=DIM, ha='center')

    # 左：热力图
    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.70, 5.20,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=CORAL, linewidth=1.5))
    ax.text(0.75, 5.45, '五周负荷热力 · 颜色越暖越危险', fontsize=9.0,
            fontweight='bold', color=CORAL, ha='left', va='center')

    x_start, cw, cgap = 2.05, 0.74, 0.06
    for j in range(6):
        ax.text(x_start + j * (cw + cgap) + cw / 2, 5.12, f'W{j + 41}',
                fontsize=6.6, color=DIM, ha='center', va='center')

    data = [
        ('张明', [95, 118, 132, 126, 104, 88]),
        ('李工', [78, 92, 108, 112, 96, 74]),
        ('王工', [64, 72, 86, 90, 82, 70]),
        ('赵工', [88, 74, 62, 58, 74, 96]),
        ('陈工', [40, 45, 48, 44, 38, 42]),
    ]

    def cell_color(v):
        if v >= 110:
            return CORAL
        if v >= 95:
            return AMBER
        if v >= 75:
            return LIME
        if v >= 50:
            return SKY
        return '#2b3644'

    for i, (name, vals) in enumerate(data):
        y = 4.40 - i * 0.70
        ax.text(1.88, y + 0.29, name, fontsize=7.4, color=TEXT, ha='right', va='center')
        for j, v in enumerate(vals):
            x = x_start + j * (cw + cgap)
            c = cell_color(v)
            ax.add_patch(FancyBboxPatch((x, y), cw, 0.58,
                                        boxstyle='round,pad=0.01,rounding_size=0.05',
                                        facecolor=c, edgecolor=c, linewidth=0,
                                        alpha=0.92 if c != '#2b3644' else 1))
            ax.text(x + cw / 2, y + 0.29, str(v), fontsize=6.6, fontweight='bold',
                    color=BG if c != '#2b3644' else DIM, ha='center', va='center')

    ax.text(0.78, 1.22, '张明连续三周 118-132%，这是排班问题，不是态度问题',
            fontsize=7.6, color=CORAL, ha='left', va='center')
    ax.text(0.78, 0.90, '陈工长期 40%，不是闲，是没被排进关键路径',
            fontsize=7.2, color=DIM, ha='left', va='center')

    # 右：四个指标
    ax.add_patch(FancyBboxPatch((7.35, 0.55), 5.20, 5.20,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=SKY, linewidth=1.5))
    ax.text(7.65, 5.42, '控制资源只看四个数', fontsize=9.0, fontweight='bold',
            color=SKY, ha='left', va='center')

    metrics = [
        ('资源利用率', '68%', '目标 75-85%，过高过低都失真', LIME),
        ('超配工时', '21 h/周', '红线 8h，超过即需调度', CORAL),
        ('单点依赖度', '3 个模块', '只挂一个人，等于没有备份', AMBER),
        ('上下文切换', '4 次/周', '每次约 2h，隐形成本没人报', PURPLE),
    ]
    for idx, (name, val, note, color) in enumerate(metrics):
        y = 4.28 - idx * 1.02
        ax.add_patch(FancyBboxPatch((7.65, y), 4.60, 0.84,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=CARD, edgecolor='#2c3644', linewidth=1))
        ax.text(7.85, y + 0.58, name, fontsize=7.8, color='#c7d0dd', ha='left', va='center')
        ax.text(12.05, y + 0.58, val, fontsize=8.6, fontweight='bold', color=color,
                ha='right', va='center')
        ax.text(7.85, y + 0.25, note, fontsize=6.6, color=DIM, ha='left', va='center')

    ax.text(7.65, 0.85, '这四个数都要按周采，按项目平均就等于没看', fontsize=7.2,
            color=DIM, ha='left', va='center')

    save(fig, 'heat.png')


# ── 4：团队阶梯 + 冲突处理 ────────────────────────────────────────────────
def draw_conflict():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.32, '没有震荡期的团队，不是成熟，是没人说真话', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.98, '团队效能有固定节奏，冲突是必经环节，不是管理失败',
            fontsize=11.5, color=DIM, ha='center')

    # 左：塔克曼曲线
    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.15, 5.20,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=PURPLE, linewidth=1.5))
    ax.text(0.75, 5.42, '团队发展的五个阶段', fontsize=9.0, fontweight='bold',
            color=PURPLE, ha='left', va='center')

    gx0, gx1 = 1.10, 6.20
    gy0, gy1 = 1.65, 4.70
    perf = [0.36, 0.14, 0.56, 0.92, 0.62]
    names = ['形成', '震荡', '规范', '执行', '解散']

    def px(i):
        return gx0 + i / 4.0 * (gx1 - gx0)

    def py(p):
        return gy0 + p * (gy1 - gy0)

    xs = [px(i) for i in range(5)]
    ys = [py(p) for p in perf]

    ax.add_patch(FancyBboxPatch((gx0 - 0.15, gy0 - 0.15), (gx1 - gx0) + 0.30,
                                (gy1 - gy0) + 0.30,
                                boxstyle='round,pad=0.01,rounding_size=0.05',
                                facecolor='#151b24', edgecolor='#2c3644', linewidth=1))
    ax.plot(xs, ys, color=PURPLE, lw=2.0, zorder=3)
    for i, (xv, yv) in enumerate(zip(xs, ys)):
        c = CORAL if i == 1 else PURPLE
        ax.plot([xv], [yv], marker='o', markersize=7,
                markerfacecolor=c, markeredgecolor=BG, markeredgewidth=1.2, zorder=4)
        ax.text(xv, yv + 0.22, f'{perf[i] * 100:.0f}', fontsize=6.4,
                color=c if i == 1 else DIM, ha='center', va='bottom')

    for i, name in enumerate(names):
        ax.text(px(i), 1.30, name, fontsize=7.6, fontweight='bold' if i == 1 else 'normal',
                color=CORAL if i == 1 else '#c7d0dd', ha='center', va='center')

    ax.text(0.75, 0.98, '震荡期效能最低，却是团队真正成形的时刻 —— 跳过它，问题会延后爆发',
            fontsize=7.2, color=DIM, ha='left', va='center')

    # 右：五种冲突方式
    ax.add_patch(FancyBboxPatch((6.80, 0.55), 5.75, 5.20,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=MINT, linewidth=1.5))
    ax.text(7.10, 5.45, '冲突处理五种方式 · 按场景选', fontsize=9.0,
            fontweight='bold', color=MINT, ha='left', va='center')

    styles = [
        ('合作', 'Collaborate', '双方诉求都纳入方案，最慢但最持久', LIME, '首选'),
        ('妥协', 'Compromise', '各让一步，临时可用，别当常态', SKY, '过渡'),
        ('强迫', 'Force', '紧急止损时用，事后要复盘', AMBER, '慎用'),
        ('迁就', 'Accommodate', '保关系，长期用会积累怨气', PURPLE, '少用'),
        ('回避', 'Avoid', '只适合小摩擦，重大分歧不能躲', CORAL, '禁用于关键'),
    ]
    for idx, (name, en, note, color, tag) in enumerate(styles):
        y = 4.52 - idx * 0.90
        ax.add_patch(FancyBboxPatch((7.10, y), 5.15, 0.76,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=CARD, edgecolor='#2c3644', linewidth=1))
        ax.text(7.30, y + 0.52, name, fontsize=8.0, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(7.30, y + 0.22, note, fontsize=6.6, color='#c7d0dd', ha='left', va='center')
        ax.text(12.05, y + 0.52, tag, fontsize=6.6, color=color, ha='right', va='center')

    ax.text(7.10, 0.72, '方式没有对错，只有合不合适 —— 写进团队章程才算约定',
            fontsize=7.2, color=DIM, ha='left', va='center')

    save(fig, 'conflict.png')


# ── 5：四种群消息 ────────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '资源消息只发四种，都要落到一个人', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.72, '不带名字的资源消息，等于没发',
            fontsize=11.5, color=DIM, ha='center')

    cards = [
        ('资源预警', '每周一 09:30', CORAL, [
            '本周 2 人超配，累计缺口 21h',
            '· 张明 132%，支付重构 + 对账并行',
            '· 李工 108%，联调支持未计入计划',
            '请 @王经理 周三前定借调或砍范围',
        ]),
        ('资源调度', '需求变更时', AMBER, [
            '下迭代缺 1.5 人月，现有 3 人可动',
            '· 可释放：赵工 40%，测试已收尾',
            '· 需补入：Android 1 人，共 4 周',
            '请确认走内部借调还是外部采购',
        ]),
        ('团队健康', '每月 1 日', PURPLE, [
            '负荷指数 82，离职风险 2 人',
            '· 连续加班 3 周：2 人',
            '· 单点依赖：3 个模块只挂一人',
            '请 @李明 本周内各做一次一对一',
        ]),
        ('资源释放', '阶段收尾', LIME, [
            '支付模块收尾，可释放 2.5 人',
            '· 张明 100% 降至 20%（只做支持）',
            '· 赵工 80% 直接归零',
            '请确认释放日期与交接清单',
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
                    color=TEXT if j == 0 else '#c7d0dd',
                    ha='left', va='center',
                    fontweight='bold' if j == 0 else 'normal')
            iy -= 0.42

    ax.text(6.5, 0.28, '每条消息四行以内：判断 / 依据 / 影响 / 要谁做什么',
            fontsize=8.2, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_demand()
    draw_heat()
    draw_conflict()
    draw_message()
    print('✓ 全部生成完毕')
