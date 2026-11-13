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

BG = '#16121c'
PANEL = '#221a2b'
CARD = '#2d2238'
TEXT = '#f3eaf6'
DIM = '#8b7f96'
PINK = '#f472b6'
ORANGE = '#fb923c'
MINT = '#34d399'
SKY = '#38bdf8'
LILAC = '#c084fc'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：需求加工流水线 ───────────────────────────────────────────────────────
def draw_flow():
    fig, ax = plt.subplots(figsize=(13, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6.5, 6.35, '一场对话进来，一份 PRD 和原型出去', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.9, '六个节点，三段职责：喂料 → 煅烧 → 出件', fontsize=12, color=DIM, ha='center')

    steps = [
        ('摄入', '录音 / 纪要 / IM', PINK, '转写 + 去噪'),
        ('结构化', '角色·场景·痛点', ORANGE, '抽实体 + 标缺口'),
        ('检索', '内部三库 + 外部', MINT, '每条结论带出处'),
        ('追问', '边界·角色·时序·失败', SKY, '问到能回答为止'),
        ('出件', 'PRD + 原型四态', LILAC, '结构化 + 可点击'),
        ('回写', '禅道 / Jira / PingCode', PINK, '需求单 + 附件'),
    ]

    w = 1.85; h = 2.4; gap = 0.22
    total = w * 6 + gap * 5
    x0 = (13 - total) / 2
    yc = 3.55

    for i, (title, desc, color, note) in enumerate(steps):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.add_patch(plt.Circle((x + w / 2, yc + h / 2 - 0.3), 0.18,
                                facecolor=color, edgecolor='none', zorder=4))
        ax.text(x + w / 2, yc + h / 2 - 0.3, str(i + 1), fontsize=10.5, fontweight='bold',
                color=BG, ha='center', va='center', zorder=5)
        ax.text(x + w / 2, yc + 0.55, title, fontsize=13.5, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(x + w / 2, yc - 0.12, desc, fontsize=8.4, color=color,
                ha='center', va='center', linespacing=1.5)
        ax.text(x + w / 2, yc - 0.85, note, fontsize=7.6, color=DIM,
                ha='center', va='center')
        if i < 5:
            ax.annotate('', xy=(x + w + gap - 0.02, yc), xytext=(x + w + 0.02, yc),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))

    # 三段职责
    bands = [
        (x0, 2 * (w + gap) - gap, '喂料 · 产品经理只负责说清楚', PINK),
        (x0 + 2 * (w + gap), 2 * (w + gap) - gap, '煅烧 · 检索 + 追问，把含糊逼成明确', ORANGE),
        (x0 + 4 * (w + gap), 2 * (w + gap) - gap, '出件 · 文档、原型、需求单一次落地', MINT),
    ]
    for bx, bw, label, color in bands:
        ax.add_patch(FancyBboxPatch((bx, 1.5), bw, 0.55,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=CARD, edgecolor=color, linewidth=1.2))
        ax.text(bx + bw / 2, 1.775, label, fontsize=8.6, color=color,
                ha='center', va='center')

    ax.text(6.5, 0.72, '人做判断，机器做整理 —— 顺序反了就会得到一份很漂亮但没用的文档',
            fontsize=9.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'flow.png')


# ── 2：检索与证据分级 ───────────────────────────────────────────────────────
def draw_retrieval():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.0, '四路取料，先分级再落笔', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.55, '没有出处的结论不叫结论，叫待确认假设', fontsize=12, color=DIM, ha='center')

    sources = [
        ('项目知识库', '历史 PRD / 需求单\n代码功能卡片 / 接口', MINT, '内部事实'),
        ('用户反馈库', '工单 / 客服记录\n业务群聊天 / 访谈库', SKY, '真实痛点'),
        ('术语与规则库', '领域名词 / 指标口径\n合规红线 / 计费规则', LILAC, '防歧义'),
        ('外部检索', '竞品功能 / 行业标准\n公开 API / 法规条款', ORANGE, '只做参考'),
    ]

    w = 2.9; gap = 0.2
    total = w * 4 + gap * 3
    x0 = (13 - total) / 2
    top = 6.05; h = 2.0

    for i, (name, desc, color, tag) in enumerate(sources):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, top - h), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.6))
        ax.text(x + 0.22, top - 0.38, name, fontsize=11.5, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + 0.22, top - 1.05, desc, fontsize=8.6, color=TEXT,
                ha='left', va='center', linespacing=1.65)
        ax.text(x + w - 0.2, top - 0.38, tag, fontsize=8, color=DIM,
                ha='right', va='center')

    ax.annotate('', xy=(6.5, 3.55), xytext=(6.5, 3.98),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.6))

    # 证据分级
    ax.add_patch(FancyBboxPatch((0.5, 0.55), 12.0, 2.9,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor='#3a2f47', linewidth=1))
    ax.text(0.9, 3.15, '证据分级（写进 PRD 的每一条都要挂一级）', fontsize=10,
            fontweight='bold', color=TEXT, ha='left')

    levels = [
        ('E1', '内部事实', '知识库里的原文、线上数据、已上线功能', MINT),
        ('E2', '内部推断', '从工单和反馈里归纳出的模式，附样本量', SKY),
        ('E3', '外部参考', '竞品做法、行业标准，必须标来源与日期', ORANGE),
        ('E4', '模型常识', '通用最佳实践，只能写进建议区，不进正文', DIM),
    ]
    y = 2.70
    for code, name, desc, color in levels:
        ax.add_patch(FancyBboxPatch((0.9, y - 0.19), 0.62, 0.38,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.21, y, code, fontsize=8.5, fontweight='bold', color=BG,
                ha='center', va='center')
        ax.text(1.72, y, name, fontsize=9.5, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(3.35, y, desc, fontsize=8.8, color=TEXT, ha='left', va='center')
        y -= 0.48

    ax.text(6.5, 0.78, 'E3 / E4 混进正文是 PRD 最常见的翻车点 —— 评审一问出处就露馅',
            fontsize=8.8, color=DIM, ha='center', va='center')

    save(fig, 'retrieval.png')


# ── 3：四类追问 ─────────────────────────────────────────────────────────────
def draw_grill():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.35, '好 PM 不是写得多，是问得狠', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.9, 'Hermes 扮演的不是打字员，是那个不客气的评审', fontsize=12, color=DIM, ha='center')

    cards = [
        ('边界', PINK,
         '余额刚好等于手续费时，能扣还是不能扣？\n并发两笔同时到达，先锁哪个？',
         '极端值 · 空值 · 并发 · 上限'),
        ('角色', ORANGE,
         '这个按钮谁能看见？谁审批？谁承担后果？\n子账号被删了，他创建的单归谁？',
         '权限 · 归属 · 责任 · 可见性'),
        ('时序', SKY,
         '先签合同还是先冻结额度？\n退款到账前，订单状态该显示什么？',
         '先后顺序 · 中间态 · 回滚'),
        ('失败', LILAC,
         '第三方接口超时，走重试还是走人工？\n重试三次都失败，用户看到什么？',
         '异常 · 兜底 · 补偿 · 提示'),
    ]

    w = 5.9; h = 1.95
    xs = [0.55, 6.55]
    ys = [4.55, 2.35]
    for i, (name, color, q, tag) in enumerate(cards):
        x = xs[i % 2]; y = ys[i // 2]
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.6))
        ax.add_patch(FancyBboxPatch((x + 0.22, y + h - 0.62), 0.75, 0.38,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.595, y + h - 0.43, name, fontsize=10, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(x + 1.12, y + h - 0.43, tag, fontsize=8.2, color=DIM,
                ha='left', va='center')
        ax.text(x + 0.24, y + 0.72, q, fontsize=8.6, color=TEXT,
                ha='left', va='center', linespacing=1.75)

    # 五个逻辑缺陷
    ax.add_patch(FancyBboxPatch((0.55, 0.55), 11.9, 1.45,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=CARD, edgecolor=PINK, linewidth=1.4))
    ax.text(0.85, 1.66, '顺带扫一遍五个致命逻辑缺陷', fontsize=9.5, fontweight='bold',
            color=PINK, ha='left')
    flaws = ['循环依赖', '状态机没有终态', '指标不可度量', '需求自相矛盾', '没有失败路径']
    x = 0.9
    for f in flaws:
        ax.add_patch(FancyBboxPatch((x, 0.85), 2.05, 0.42,
                                    boxstyle='round,pad=0.02,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=PINK, linewidth=1))
        ax.text(x + 1.025, 1.06, f, fontsize=7.8, color=TEXT, ha='center', va='center')
        x += 2.22

    save(fig, 'grill.png')


# ── 4：PRD 骨架 + 原型四态 ─────────────────────────────────────────────────
def draw_produce():
    fig, ax = plt.subplots(figsize=(13, 8.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 8.0); ax.axis('off')

    ax.text(6.5, 7.6, '出件：一份能评审的 PRD，一张能点开的原型', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.15, '文档给人看，原型给研发看，两者必须能对上', fontsize=12, color=DIM, ha='center')

    # 左：PRD 目录
    ax.add_patch(FancyBboxPatch((0.5, 0.6), 5.2, 6.2,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=MINT, linewidth=1.6))
    ax.text(0.8, 6.44, 'PRD · 十章骨架', fontsize=11.5, fontweight='bold',
            color=MINT, ha='left')
    chapters = [
        '01 背景与要解决的问题',
        '02 目标与非目标',
        '03 用户角色与场景',
        '04 功能清单与优先级',
        '05 主流程与状态机',
        '06 字段、规则与校验',
        '07 权限与数据可见性',
        '08 异常、边界与兜底',
        '09 非功能与合规约束',
        '10 验收标准（给定/当/则）',
    ]
    y = 5.95
    for c in chapters:
        ax.text(0.82, y, c, fontsize=8.7, color=TEXT, ha='left', va='center')
        y -= 0.52

    ax.text(0.82, 0.78, '每条验收标准必须可测，否则研发只能猜',
            fontsize=7.8, color=DIM, ha='left', va='center')

    # 右：原型四态
    ax.add_patch(FancyBboxPatch((5.95, 0.6), 6.55, 6.2,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=LILAC, linewidth=1.6))
    ax.text(6.25, 6.44, '原型 · 四态齐全的 HTML 线框', fontsize=11.5, fontweight='bold',
            color=LILAC, ha='left')

    states = [('正常', MINT, '有数据'), ('空态', SKY, '没数据'), ('错误', ORANGE, '失败了'), ('加载', DIM, '等待中')]
    sw = 1.4; sgap = 0.16
    sx0 = 6.25
    sy = 3.05; sh = 2.6

    for i, (label, color, note) in enumerate(states):
        sx = sx0 + i * (sw + sgap)
        ax.add_patch(FancyBboxPatch((sx, sy), sw, sh,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=color, linewidth=1.3))
        # 顶部栏
        ax.add_patch(Rectangle((sx + 0.1, sy + sh - 0.32), sw - 0.2, 0.16,
                               facecolor=color, edgecolor='none', alpha=0.55))
        # 内容线
        if label != '空态':
            ax.add_patch(Rectangle((sx + 0.12, sy + sh - 0.78), 0.34, 0.26,
                                   facecolor='#4a3d57', edgecolor='none'))
            ax.plot([sx + 0.55, sx + sw - 0.12], [sy + sh - 0.65, sy + sh - 0.65],
                    color='#4a3d57', lw=2)
            ax.plot([sx + 0.55, sx + sw - 0.2], [sy + sh - 0.85, sy + sh - 0.85],
                    color='#4a3d57', lw=1.2)
        for j, ly in enumerate([1.55, 1.28, 1.01]):
            if label == '空态' and j > 0:
                continue
            ax.plot([sx + 0.12, sx + sw - 0.2], [sy + ly, sy + ly],
                    color='#4a3d57', lw=1)
        # 底部按钮
        ax.add_patch(Rectangle((sx + 0.12, sy + 0.28), sw - 0.24, 0.26,
                               facecolor=color, edgecolor='none', alpha=0.75))
        ax.text(sx + sw / 2, sy - 0.3, label, fontsize=9.5, fontweight='bold',
                color=color, ha='center', va='center')
        ax.text(sx + sw / 2, sy - 0.62, note, fontsize=7.4, color=DIM,
                ha='center', va='center')

    ax.text(9.2, 1.55, '四态缺一个，评审现场就会被问住', fontsize=8.2,
            color=DIM, ha='center', va='center')
    ax.text(9.2, 1.15, 'HTML 原型可版本化、可直接交给前端、可当验收基线',
            fontsize=8.2, color=TEXT, ha='center', va='center')

    save(fig, 'produce.png')


# ── 5：三平台字段映射 ───────────────────────────────────────────────────────
def draw_platforms():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.8, '同一个需求，三种平台的落法', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.35, '字段名不同，语义要对齐 —— 映射表写死在配置里', fontsize=12,
            color=DIM, ha='center')

    headers = ['PRD 字段', '禅道', 'Jira', 'PingCode']
    hx = [0.75, 3.55, 6.55, 9.65]
    ax.add_patch(Rectangle((0.5, 5.4), 12.0, 0.62, facecolor=CARD, edgecolor='#3a2f47', lw=1))
    for h, x in zip(headers, hx):
        ax.text(x, 5.71, h, fontsize=9.5, fontweight='bold', color=SKY, ha='left', va='center')

    rows = [
        ('需求标题', 'title', 'summary', 'name'),
        ('需求描述', 'spec（HTML）', 'description', 'description'),
        ('验收标准', 'verify', 'customfield_10106', 'acceptance_criteria'),
        ('优先级', 'pri', 'priority', 'priority_id'),
        ('负责人', 'assignedTo', 'assignee', 'assignee_id'),
        ('迭代', 'execution', 'sprint', 'iteration_id'),
        ('附件', 'file / 附件', 'attachment', 'attachment'),
        ('初始状态', 'status = wait', 'status = To Do', 'state = unstarted'),
    ]

    y = 5.4
    for i, (field, zentao, jira, pingcode) in enumerate(rows):
        bg = PANEL if i % 2 == 0 else '#1b1523'
        ax.add_patch(Rectangle((0.5, y - 0.58), 12.0, 0.58, facecolor=bg,
                               edgecolor='#2e2438', lw=0.8))
        ax.text(0.75, y - 0.29, field, fontsize=8.8, fontweight='bold', color=TEXT,
                ha='left', va='center')
        ax.text(3.55, y - 0.29, zentao, fontsize=8.4, color=MINT, ha='left', va='center')
        ax.text(6.55, y - 0.29, jira, fontsize=8.4, color=SKY, ha='left', va='center')
        ax.text(9.65, y - 0.29, pingcode, fontsize=8.4, color=LILAC, ha='left', va='center')
        y -= 0.58

    ax.text(6.5, 0.34, '建成「待评审」而不是「已确认」 —— 需求单是讨论的起点，不是结论',
            fontsize=9.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'platforms.png')


if __name__ == '__main__':
    draw_flow()
    draw_retrieval()
    draw_grill()
    draw_produce()
    draw_platforms()
    print('✓ 全部生成完毕')
