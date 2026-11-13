# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patheffects as pe

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0a0e18'
PANEL = '#121a2e'
CARD = '#1a2340'
CARD2 = '#242e54'
LINE = '#35416a'
INDIGO = '#6366f1'
VIOLET = '#a855f7'
CYAN = '#22d3ee'
EMERALD = '#34d399'
AMBER = '#fbbf24'
ROSE = '#fb7185'
TXT = '#e2e8f4'
SUB = '#8b98ba'
DIM = '#5a6a90'

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(OUT, exist_ok=True)


def canvas():
    fig, ax = plt.subplots(figsize=(10.8, 6.65))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    return fig, ax


def card(ax, x, y, w, h, fc=CARD, ec=LINE, lw=1.0, r=0.12, z=1):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f'round,pad=0,rounding_size={r}',
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z)
    ax.add_patch(p)
    return p


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=160, facecolor=BG,
                bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    print('  ->', name)


# ---------------------------------------------------------------- fig 1 philosophy
def fig_philosophy():
    fig, ax = canvas()

    ax.text(6.5, 7.60, 'dsh-superagent 的哲学：注意力经济学', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)

    # Large centered quote
    ax.text(6.5, 6.60, '"', ha='center', va='center',
            fontsize=52, color=INDIGO, fontweight='bold', style='italic', zorder=3)
    ax.text(6.5, 6.20, 'Take as little human attention as possible,\nand give as much value as possible.',
            ha='center', va='center', fontsize=12.5, color=TXT, linespacing=1.7, zorder=3)

    # Two side columns: Agent rules vs Design rules
    # Agent column
    ax.text(3.65, 5.32, '对 agent 的三条约束', ha='center', va='center',
            fontsize=11, fontweight='bold', color=CYAN)
    ax.plot([0.80, 6.50], [5.12, 5.12], color=LINE, lw=0.9, ls=(0, (4, 4)))

    agent_rules = [
        ('只在被 ask 或有 written rule 时才行动', '不做事先没人要的活'),
        ('确认一次、完成一次、回答一次', '中间静默、卡住才出声'),
        ('按 impact 停，不按 effort 停', '失败就是失败，不绕过边界'),
    ]
    ly = 4.78
    for title, desc in agent_rules:
        card(ax, 0.80, ly - 0.60, 5.65, 0.78, fc=CARD, ec=CYAN, lw=1.0)
        ax.text(1.00, ly - 0.12, title, ha='left', va='center',
                fontsize=9.4, fontweight='bold', color=TXT, zorder=3)
        ax.text(1.00, ly - 0.35, desc, ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        ly -= 0.98

    # Design column
    ax.text(9.15, 5.32, '对设计的三条约束', ha='center', va='center',
            fontsize=11, fontweight='bold', color=VIOLET)

    design_rules = [
        ('Few concepts，few settings', '业务需求变成属性或 prompt，不是新概念'),
        ('Panel 只展示需要人的部分', '健康状态不占空间'),
        ('文档编号顺序读', '每篇只依赖之前的知识'),
    ]
    ly = 4.78
    for title, desc in design_rules:
        card(ax, 6.90, ly - 0.60, 5.30, 0.78, fc=CARD, ec=VIOLET, lw=1.0)
        ax.text(7.10, ly - 0.12, title, ha='left', va='center',
                fontsize=9.4, fontweight='bold', color=TXT, zorder=3)
        ax.text(7.10, ly - 0.35, desc, ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        ly -= 0.98

    # Responsibility footer
    ax.text(6.5, 0.80, '每一次 agent 发消息，都在消耗同事的注意力——这是设计的第一约束',
            ha='center', va='center', fontsize=9.8, color=TXT)
    save(fig, 'philosophy.png')


# ---------------------------------------------------------------- fig 2 domain flow
def fig_domain():
    fig, ax = canvas()

    ax.text(6.5, 7.60, '域模型：Trigger → Eval → Ticket → Executor', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '五个核心概念 + 四种规则让 agent "合法" 地干活', ha='center', va='center',
            fontsize=10, color=SUB)

    # Flow boxes
    flow = [
        ('Source', 'GitHub / Feishu\n事件流 + 自己 bot 身份', INDIGO, 0.70),
        ('Trigger', '一个不可变事件\n带 actor + metadata', CYAN, 2.80),
        ('Thread', '时间序 Trigger 流\nEval 串行跑', VIOLET, 4.90),
        ('Eval', '两层判断\nGate + Assessment', EMERALD, 7.00),
        ('Ticket', '授权的工作单元\n持 Mandate + Channels', AMBER, 9.10),
        ('Executor', 'worker Session\n独立目录', ROSE, 11.05),
    ]
    h = 1.40
    y = 5.25
    for i, (name, desc, col, xc) in enumerate(flow):
        card(ax, xc - 1.75, y, 3.50, h, fc=CARD, ec=col, lw=1.3)
        ax.text(xc, y + h - 0.35, name, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color=col, zorder=3)
        ax.text(xc, y + h - 0.82, desc, ha='center', va='center',
                fontsize=8.5, color=TXT, linespacing=1.38, zorder=3)
        if i < len(flow) - 1:
            ax.annotate('', xy=(flow[i + 1][3] - 1.85, y + h / 2),
                        xytext=(xc + 1.75, y + h / 2),
                        arrowprops=dict(arrowstyle='-|>', color=LINE, lw=1.2))

    # Mandate card below Eval
    ax.plot([6.55, 7.45], [5.25, 5.25], color=LINE, lw=0.9)
    card(ax, 5.35, 3.65, 3.60, 0.85, fc=CARD2, ec=INDIGO, lw=1.2)
    ax.text(7.15, 4.175, 'Eval 通过后产出 Mandate（授权）', ha='center', va='center',
            fontsize=9.4, fontweight='bold', color=TXT, zorder=3)
    ax.text(7.15, 3.87, 'Policy version + scope + strength + sender identity',
            ha='center', va='center', fontsize=7.8, color=SUB, zorder=3)
    ax.annotate('', xy=(7.15, 4.50), xytext=(7.15, 5.25),
                arrowprops=dict(arrowstyle='-|>', color=INDIGO, lw=1.1))

    # Subscription fan-out to Ticket
    card(ax, 9.55, 3.65, 2.95, 0.85, fc=CARD2, ec=CYAN, lw=1.2)
    ax.text(11.025, 4.175, 'Subscription 订阅', ha='center', va='center',
            fontsize=9.4, fontweight='bold', color=TXT, zorder=3)
    ax.text(11.025, 3.87, '后续消息扇回 Ticket，无需 Eval',
            ha='center', va='center', fontsize=7.8, color=SUB, zorder=3)
    ax.annotate('', xy=(11.025, 4.50), xytext=(11.025, 5.25),
                arrowprops=dict(arrowstyle='-|>', color=CYAN, lw=1.1))

    ax.text(6.5, 2.35, 'Eval 两种结局', ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=SUB)
    ends = [('accept', '接单（带 Mandate）', EMERALD),
            ('stop', '停止', ROSE),
            ('ignore', '忽略', DIM),
            ('unavailable', '未完成（重排 Trigger）', AMBER)]
    ew, eh, egap = 2.10, 0.70, 0.18
    etotal = len(ends) * ew + (len(ends) - 1) * egap
    ex0 = (13 - etotal) / 2
    ey = 1.55
    for i, (label, desc, col) in enumerate(ends):
        ex = ex0 + i * (ew + egap)
        card(ax, ex, ey, ew, eh, fc=CARD, ec=col, lw=1.2)
        ax.text(ex + ew / 2, ey + eh / 2 + 0.13, label, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color=col, zorder=3)
        ax.text(ex + ew / 2, ey + eh / 2 - 0.14, desc, ha='center', va='center',
                fontsize=7.6, color=TXT, zorder=3)

    ax.text(6.5, 0.80, '一个 Thread 可有多个 Ticket；Eval 串行跑；Trigger 被过滤后不重放',
            ha='center', va='center', fontsize=9.5, color=TXT)
    save(fig, 'domain.png')


# ---------------------------------------------------------------- fig 3 ticket stages
def fig_ticket():
    fig, ax = canvas()

    ax.text(6.5, 7.60, 'Ticket 生命周期：先判断 "需要人吗"', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '六个 stage 互斥、覆盖所有情况、可被机器判定', ha='center', va='center',
            fontsize=10, color=SUB)

    stages = [
        ('person\n/answer', '等待人回答', '有 Attention', ROSE),
        ('person\n/review', '等待人 review', '最新 Report=ready', AMBER),
        ('person\n/blocked', '受阻，等消息', 'Report=blocked 或 failed', ROSE),
        ('working\n/queued', '排队中', '无 Assignment 或 pending', VIOLET),
        ('working', '执行中', '其他情况', INDIGO),
        ('idle', '等待下一个 Trigger', 'Report=waiting', SUB),
    ]

    w, gap, h = 1.62, 0.18, 2.75
    x0 = (13 - (w * 6 + gap * 5)) / 2
    y = 3.40

    for i, (name, label, cond, col) in enumerate(stages):
        cx = x0 + i * (w + gap)
        card(ax, cx, y, w, h, fc=CARD, ec=col, lw=1.3)
        lines = name.split('\n')
        for j, ln in enumerate(lines):
            ax.text(cx + w / 2, y + h - 0.35 - j * 0.30, ln, ha='center', va='center',
                    fontsize=9, fontweight='bold', color=col, zorder=3)
        ax.plot([cx + 0.15, cx + w - 0.15], [y + h - 1.05, y + h - 1.05],
                color=LINE, lw=0.8, zorder=2)
        ax.text(cx + w / 2, y + h - 1.30, label, ha='center', va='center',
                fontsize=8.2, fontweight='bold', color=TXT, zorder=3)
        ax.text(cx + w / 2, y + h - 1.65, cond, ha='center', va='center',
                fontsize=7.5, color=SUB, linespacing=1.3, zorder=3)

        if i < len(stages) - 1:
            ax.annotate('', xy=(cx + w + gap - 0.02, y + h / 2 - 0.15),
                        xytext=(cx + w + 0.02, y + h / 2 - 0.15),
                        arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    # Human stop badge
    card(ax, 5.15, 2.35, 2.70, 0.55, fc='#3a1f2e', ec=ROSE, lw=1.2)
    ax.text(6.50, 2.625, 'person / stop 是独立出口（撤销 Mandate）', ha='center', va='center',
            fontsize=9, fontweight='bold', color=ROSE, zorder=3)

    # Subscription resume
    card(ax, 8.30, 2.35, 3.20, 0.55, fc='#1f3a2f', ec=EMERALD, lw=1.2)
    ax.text(9.90, 2.625, '新 Trigger 扇入 / 人发消息 → idle 自动 resume',
            ha='center', va='center', fontsize=8.5, color=EMERALD, zorder=3)

    # Rule text at bottom
    card(ax, 1.05, 1.40, 10.90, 0.65, fc=CARD2, ec=LINE, lw=1.0)
    ax.text(6.5, 1.78, '判定顺序从上到下：第一个匹配的行获胜。person stage = Ticket 无法继续；新 human message 释放 blocked/failed。',
            ha='center', va='center', fontsize=8.6, color=TXT, zorder=3)

    ax.text(6.5, 0.78, '关键：Ticket 自己定义 state，不跟随 Executor Session 的状态',
            ha='center', va='center', fontsize=9.6, color=TXT)
    save(fig, 'ticket.png')


# ---------------------------------------------------------------- fig 4 authorization
def fig_auth():
    fig, ax = canvas()

    ax.text(6.5, 7.60, '两条授权路径：Eval vs Subscription', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '只有 Eval 能产生新授权；Subscription 只是上下文扇入，不加权',
            ha='center', va='center', fontsize=10, color=SUB)

    # Left path: Eval
    ax.text(3.50, 6.50, '路径 A · Eval（产生新授权）', ha='center', va='center',
            fontsize=11, fontweight='bold', color=INDIGO)
    card(ax, 0.60, 2.40, 5.80, 3.80, fc=CARD, ec=INDIGO, lw=1.2)

    steps_a = [
        ('Source 收到 Trigger', 'mention / direct / inferred'),
        ('Gate 准入（第一层，确定性）', 'Allowed person / admission table / bot list'),
        ('Assessment 研判（第二层，模型）', '接受 / 忽略 / 未完成'),
        ('Eval 接受 → 新建 Ticket', '带 Mandate（授权范围 + strength + policy version）'),
    ]
    ly = 5.85
    for i, (title, desc) in enumerate(steps_a):
        ax.text(0.85, ly, f'{i + 1}.  {title}', ha='left', va='center',
                fontsize=9.2, fontweight='bold', color=TXT, zorder=3)
        ax.text(0.85, ly - 0.30, desc, ha='left', va='center',
                fontsize=8.0, color=SUB, zorder=3)
        ly -= 0.68
        if i < len(steps_a) - 1:
            ax.annotate('', xy=(3.50, ly + 0.08), xytext=(3.50, ly + 0.28),
                        arrowprops=dict(arrowstyle='-|>', color=DIM, lw=0.9))

    # Right path: Subscription
    ax.text(9.00, 6.50, '路径 B · Subscription（不加权）', ha='center', va='center',
            fontsize=11, fontweight='bold', color=CYAN)
    card(ax, 6.55, 2.40, 5.70, 3.80, fc=CARD, ec=CYAN, lw=1.2)

    steps_b = [
        ('Ticket 已存在，订阅某 Thread', 'Executor 或 Main Session 订阅'),
        ('Thread 有新 Trigger', '任何人发消息（含 bot、CI）'),
        ('Trigger 扇出给所有订阅 Ticket', '不经过 Eval，不加新授权'),
        ('Executor 收到 Input', '在现有 Mandate 范围内处理，超出则 hand back'),
    ]
    ly = 5.85
    for i, (title, desc) in enumerate(steps_b):
        ax.text(6.80, ly, f'{i + 1}.  {title}', ha='left', va='center',
                fontsize=9.2, fontweight='bold', color=TXT, zorder=3)
        ax.text(6.80, ly - 0.30, desc, ha='left', va='center',
                fontsize=8.0, color=SUB, zorder=3)
        ly -= 0.68
        if i < len(steps_b) - 1:
            ax.annotate('', xy=(9.40, ly + 0.08), xytext=(9.40, ly + 0.28),
                        arrowprops=dict(arrowstyle='-|>', color=DIM, lw=0.9))

    ax.text(6.5, 1.95, '关键点：Subscription 覆盖整个 Thread，Mandate 分离了"授权"和"上下文"',
            ha='center', va='center', fontsize=9.4, color=TXT)

    # Strength badge
    card(ax, 3.55, 1.40, 5.90, 0.42, fc='#2a2748', ec=INDIGO, lw=1.0)
    ax.text(6.50, 1.61, 'strength: explicit（人直接要）> inferred（bot 推断）；不同 Source 身份从不互相映射',
            ha='center', va='center', fontsize=8.3, color=INDIGO, zorder=3)

    ax.text(6.5, 0.78, 'Policy 是版本化的；改规则不会 revoke 已存在的 Mandate',
            ha='center', va='center', fontsize=9.5, color=TXT)
    save(fig, 'authorization.png')


# ---------------------------------------------------------------- fig 5 architecture
def fig_arch():
    fig, ax = canvas()

    ax.text(6.5, 7.60, 'Engine 是大脑，Runtime 只负责装配', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '所有域规则在 Engine；外部边界通过 port 接口解耦', ha='center', va='center',
            fontsize=10, color=SUB)

    # Center Engine
    cx, cy, cw, ch = 4.40, 3.05, 4.20, 2.55
    card(ax, cx, cy, cw, ch, fc=CARD2, ec=INDIGO, lw=1.6)
    ax.text(cx + cw / 2, cy + ch - 0.40, 'Engine', ha='center', va='center',
            fontsize=14, fontweight='bold', color=INDIGO, zorder=3)
    ax.text(cx + cw / 2, cy + ch - 0.82, '所有域规则 · 决策中心', ha='center', va='center',
            fontsize=8.5, color=TXT, zorder=3)

    ports = [
        ('Store', 'Repositories', cx - 0.20, cy + ch / 2 - 0.10, DIM, 'left'),
        ('Policy', '版本化规则', cx + cw + 0.20, cy + ch - 0.50, VIOLET, 'right'),
        ('Assessor', 'Eval 研判', cx + cw + 0.20, cy + 0.80, EMERALD, 'right'),
        ('Executor', '执行交付', cx + cw + 0.20, cy + 0.25, ROSE, 'right'),
        ('Outbox', '输出事件', cx + cw / 2, cy - 0.40, CYAN, 'bottom'),
    ]
    for name, desc, px, py, col, side in ports:
        card(ax, px - 0.85, py - 0.30, 1.70, 0.60, fc=CARD, ec=col, lw=1.2)
        ax.text(px, py + 0.06, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color=col, zorder=3)
        ax.text(px, py - 0.15, desc, ha='center', va='center',
                fontsize=7.2, color=SUB, zorder=3)
        if side == 'left':
            ax.annotate('', xy=(cx, cy + ch / 2), xytext=(cx - 0.85, py),
                        arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0))
        elif side == 'right':
            ax.annotate('', xy=(cx + cw, py), xytext=(cx + cw + 0.85, py),
                        arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0))
        elif side == 'bottom':
            ax.annotate('', xy=(cx + cw / 2, cy), xytext=(cx + cw / 2, cy - 0.40 + 0.30),
                        arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0))

    # Top Sources and Sessions
    card(ax, 0.55, 5.65, 3.15, 0.60, fc=CARD, ec=INDIGO, lw=1.1)
    ax.text(2.125, 6.05, 'Source plugins', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=INDIGO, zorder=3)
    ax.annotate('', xy=(cx + 0.60, cy + ch), xytext=(2.125, 5.65),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    card(ax, 9.00, 5.65, 3.15, 0.60, fc=CARD, ec=CYAN, lw=1.1)
    ax.text(10.575, 6.05, 'Session tools', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=CYAN, zorder=3)
    ax.annotate('', xy=(cx + cw - 0.60, cy + ch), xytext=(10.575, 5.65),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    # Bottom Effects + Sessions + Runtime
    card(ax, 0.55, 1.55, 4.05, 0.60, fc=CARD, ec=AMBER, lw=1.1)
    ax.text(2.575, 1.95, 'Effects（统一异步）', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=AMBER, zorder=3)
    ax.annotate('', xy=(cx + 0.40, cy), xytext=(2.575, 2.15),
                arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0))

    card(ax, 7.00, 1.55, 3.75, 0.60, fc=CARD, ec=ROSE, lw=1.1)
    ax.text(8.875, 1.95, 'Sessions（Main + Executor）', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=ROSE, zorder=3)
    ax.annotate('', xy=(cx + cw - 0.40, cy), xytext=(8.875, 2.15),
                arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0))

    card(ax, 11.05, 1.55, 1.45, 0.60, fc=CARD2, ec=TXT, lw=1.0)
    ax.text(11.775, 1.95, 'Runtime', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=TXT, zorder=3)

    ax.text(6.5, 0.80, 'Runtime 只装配，不含域规则；Engine 自己构建内部 parts；Executor/Assessor 回调 Engine',
            ha='center', va='center', fontsize=9.5, color=TXT)
    save(fig, 'architecture.png')


if __name__ == '__main__':
    print('generating assets ...')
    fig_philosophy()
    fig_domain()
    fig_ticket()
    fig_auth()
    fig_arch()
    print('done.')
