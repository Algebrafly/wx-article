# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Polygon, Circle
import matplotlib.patheffects as pe

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0c0e14'
PANEL = '#151823'
CARD = '#1c2130'
CARD2 = '#242b3d'
LINE = '#2f384d'
VIOLET = '#a78bfa'
CYAN = '#22d3ee'
GREEN = '#34d399'
AMBER = '#fbbf24'
ROSE = '#fb7185'
TXT = '#e6e9f0'
SUB = '#8b93a7'
DIM = '#5d667d'

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


# ---------------------------------------------------------------- fig 1
def fig_pipeline():
    fig, ax = canvas()

    ax.text(6.5, 7.60, '同一张 SDLC，两种驱动方式', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)

    # top band
    ax.text(0.60, 7.02, '现在：每一步都要人去推', ha='left', va='center',
            fontsize=10.5, color=SUB)

    steps = ['需求', '设计', '开发', '测试', '评审', '上线']
    w, gap, h = 1.78, 0.22, 0.85
    x0 = (13 - (w * 6 + gap * 5)) / 2
    y = 5.45
    for i, s in enumerate(steps):
        cx = x0 + i * (w + gap)
        card(ax, cx, y, w, h, fc=CARD, ec=LINE)
        ax.text(cx + w / 2, y + 0.55, s, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color=TXT, zorder=3)
        ax.text(cx + w / 2, y + 0.22, '人工推进', ha='center', va='center',
                fontsize=8.5, color=ROSE, zorder=3)
        if i < 5:
            ax.annotate('', xy=(cx + w + gap - 0.02, y + h / 2),
                        xytext=(cx + w + 0.02, y + h / 2),
                        arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.1))

    ax.text(6.5, 4.92, '差别不在工具，而在"谁负责推进"', ha='center', va='center',
            fontsize=10.5, color=VIOLET, style='italic')

    # bottom band
    ax.text(0.60, 4.30, 'AI-native：agent 连续推进，人只在 4 个闸口点头',
            ha='left', va='center', fontsize=10.5, color=SUB)

    agents = ['Issue', 'Spec', 'Design', 'Tasks', 'Build', 'Test', 'Review', 'Release']
    bw, bgap, bh = 1.30, 0.20, 0.88
    bx0 = (13 - (bw * 8 + bgap * 7)) / 2
    by = 1.82
    gates = {0: ('立项', GREEN), 1: ('规格冻结', CYAN), 6: ('合并', AMBER), 7: ('上线', ROSE)}
    for i, s in enumerate(agents):
        cx = bx0 + i * (bw + bgap)
        is_gate = i in gates
        ec = gates[i][1] if is_gate else LINE
        card(ax, cx, by, bw, bh, fc=CARD2 if is_gate else CARD, ec=ec, lw=1.4 if is_gate else 1.0)
        ax.text(cx + bw / 2, by + bh / 2 + 0.08, s, ha='center', va='center',
                fontsize=10, fontweight='bold', color=TXT, zorder=3)
        ax.text(cx + bw / 2, by + 0.22, 'agent', ha='center', va='center',
                fontsize=8, color=SUB, zorder=3)
        if i < 7:
            ax.annotate('', xy=(cx + bw + bgap - 0.01, by + bh / 2),
                        xytext=(cx + bw + 0.01, by + bh / 2),
                        arrowprops=dict(arrowstyle='-|>', color=VIOLET, lw=1.1))
        if is_gate:
            gx = cx + bw / 2
            ax.add_patch(Circle((gx, 3.42), 0.17, facecolor=ec, edgecolor='none', zorder=4))
            ax.text(gx, 3.42, '人', ha='center', va='center', fontsize=9,
                    fontweight='bold', color='#0c0e14', zorder=5)
            ax.text(gx, 3.83, gates[i][0], ha='center', va='center',
                    fontsize=8.5, color=ec, zorder=5)

    ax.text(6.5, 1.02, '人的工作从"操作每一步"变成"判断关键时刻"',
            ha='center', va='center', fontsize=10.2, color=TXT)
    save(fig, 'pipeline.png')


# ---------------------------------------------------------------- fig 2
def fig_landscape():
    fig, ax = canvas()

    ax.text(6.5, 7.58, '市面上的产品，已经分成四条路线', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)

    L, R, B, T = 1.75, 12.35, 1.55, 6.55
    midx, midy = (L + R) / 2, (B + T) / 2

    ax.annotate('', xy=(R + 0.25, B), xytext=(L - 0.15, B),
                arrowprops=dict(arrowstyle='-|>', color=LINE, lw=1.4))
    ax.annotate('', xy=(L, T + 0.25), xytext=(L, B - 0.15),
                arrowprops=dict(arrowstyle='-|>', color=LINE, lw=1.4))
    ax.plot([midx, midx], [B, T], color=LINE, lw=0.9, ls=(0, (4, 4)), zorder=1)
    ax.plot([L, R], [midy, midy], color=LINE, lw=0.9, ls=(0, (4, 4)), zorder=1)

    ax.text(midx, 1.10, '单任务  →  覆盖整条流水线', ha='center', va='center',
            fontsize=10, color=SUB)
    ax.text(1.28, midy, '开放可编排  →', ha='center', va='center',
            fontsize=10, color=SUB, rotation=90)

    for qx, qy, qs in [(L + 0.18, T - 0.22, '开放 · 单点'),
                       (R - 0.18, T - 0.22, '开放 · 全流程'),
                       (L + 0.18, B + 0.18, '封闭 · 单点'),
                       (R - 0.18, B + 0.18, '封闭 · 全流程')]:
        ax.text(qx, qy, qs, ha='left' if qx < midx else 'right', va='center',
                fontsize=8.5, color=DIM)

    pts = [
        ('Devin', '单实例接完整 ticket', 3.35, 2.55, ROSE),
        ('Amazon Kiro', '规格驱动 IDE', 5.30, 3.30, ROSE),
        ('Factory Droids', '托管式软件工厂', 9.75, 2.55, ROSE),
        ('Claude Code / Codex', 'subagent 自行编排', 3.50, 5.45, CYAN),
        ('GitHub Copilot + Spec Kit', '自定义 agent + 规格', 8.70, 5.72, CYAN),
        ('Warp Factories', '自建工厂基建', 10.95, 4.68, CYAN),
    ]
    for name, desc, px, py, col in pts:
        card(ax, px - 1.25, py - 0.33, 2.50, 0.66, fc=CARD, ec=col, lw=1.2, r=0.10)
        fs = 8.6 if len(name) > 18 else 9.4
        ax.text(px, py + 0.12, name, ha='center', va='center',
                fontsize=fs, fontweight='bold', color=TXT, zorder=3)
        ax.text(px, py - 0.16, desc, ha='center', va='center',
                fontsize=8.2, color=SUB, zorder=3)

    card(ax, 10.25, 6.02, 2.50, 0.55, fc='#2a2140', ec=VIOLET, lw=1.4, r=0.10)
    ax.text(11.50, 6.295, 'Hermes（本文）', ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=VIOLET, zorder=3)

    ax.text(6.5, 0.72, '横轴看"覆盖多长"，纵轴看"能不能自己改"——没有最优，只有匹配',
            ha='center', va='center', fontsize=9.5, color=SUB)
    save(fig, 'landscape.png')


# ---------------------------------------------------------------- fig 3
def fig_handoff():
    fig, ax = canvas()

    ax.text(6.5, 7.58, '交接的不是消息，是工件', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '每个工位只认上一个工位落盘的文件，不认聊天记录',
            ha='center', va='center', fontsize=10, color=SUB)

    rows = [
        ('triage', 'issue.md', '原始诉求 + 复现步骤 + 影响面', '可复现', GREEN),
        ('spec', 'spec.md', '用户故事 + EARS 验收标准 + 范围外', '每条可测', CYAN),
        ('architect', 'design.md', '架构 / 接口 / 数据 / 取舍记录', '无未决项', CYAN),
        ('planner', 'tasks.yaml', '任务拆到 1 天内 + 依赖图', '可并行', VIOLET),
        ('coder', 'feat/*.patch', '最小 diff + 本地自测', 'CI 全绿', AMBER),
        ('verifier', 'evidence.json', '测试 / 扫描 / 基准 原始输出', '证据齐全', AMBER),
        ('release', 'release.md', '变更说明 + 灰度 + 回滚预案', '可回滚', ROSE),
    ]

    top = 6.60
    rh, step = 0.70, 0.845
    for i, (agent, fname, desc, check, col) in enumerate(rows):
        y = top - i * step - rh
        cy = y + rh / 2
        card(ax, 0.45, y, 1.95, rh, fc=CARD2, ec=LINE)
        ax.text(1.425, cy, agent, ha='center', va='center',
                fontsize=9.2, color=TXT, zorder=3)
        ax.annotate('', xy=(2.92, cy), xytext=(2.48, cy),
                    arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))
        card(ax, 2.96, y, 6.20, rh, fc=CARD, ec=LINE)
        ax.text(3.15, cy + 0.13, fname, ha='left', va='center',
                fontsize=9.8, fontweight='bold', color=TXT, zorder=3)
        ax.text(3.15, cy - 0.16, desc, ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        card(ax, 9.40, y, 3.15, rh, fc='#182033', ec=col, lw=1.1)
        ax.text(9.58, cy, '校验', ha='left', va='center',
                fontsize=8, color=SUB, zorder=3)
        ax.text(10.55, cy, check, ha='left', va='center',
                fontsize=9.6, fontweight='bold', color=col, zorder=3)

    ax.text(6.5, 0.55, '工件即协议：格式稳定，agent 才能替换；文件落盘，人才能审计',
            ha='center', va='center', fontsize=9.8, color=TXT)
    save(fig, 'handoff.png')


# ---------------------------------------------------------------- fig 4
def fig_gates():
    fig, ax = canvas()

    ax.text(6.5, 7.58, '人只在这四个闸口出现', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '其余时间 agent 自己推进，卡住才上报', ha='center', va='center',
            fontsize=10, color=SUB)

    gates = [
        ('01', '立项', '这件事值不值得做？\n有没有更便宜的解法？', '最低', 1, GREEN, '30 秒'),
        ('02', '规格冻结', '验收标准能不能测？\n边界写清楚没有？', '偏低', 2, CYAN, '10 分钟'),
        ('03', '合并', 'diff 和证据对得上吗？\n有没有偷偷改范围？', '偏高', 3, AMBER, '15 分钟'),
        ('04', '上线', '回滚预案是什么？\n今晚谁值班？', '最高', 4, ROSE, '5 分钟'),
    ]
    w, gap, h = 2.92, 0.22, 4.72
    x0 = (13 - (w * 4 + gap * 3)) / 2
    y = 1.50

    for i, (num, name, body, cost, lvl, col, sla) in enumerate(gates):
        cx = x0 + i * (w + gap)
        card(ax, cx, y, w, h, fc=CARD, ec=col, lw=1.3)
        ax.text(cx + 0.30, y + 4.42, f'GATE {num}', ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        ax.text(cx + 0.30, y + 3.85, num, ha='left', va='center',
                fontsize=25, fontweight='bold', color=col, zorder=3)
        ax.text(cx + 0.30, y + 3.36, name, ha='left', va='center',
                fontsize=14, fontweight='bold', color=TXT, zorder=3)
        ax.plot([cx + 0.30, cx + w - 0.30], [y + 3.10, y + 3.10],
                color=LINE, lw=0.9, zorder=2)
        ax.text(cx + 0.30, y + 2.80, '你只需要看', ha='left', va='center',
                fontsize=8.2, color=col, zorder=3)
        ax.text(cx + 0.30, y + 2.34, body, ha='left', va='center',
                fontsize=9.4, color=TXT, linespacing=1.55, zorder=3)
        ax.text(cx + 0.30, y + 1.42, '拒绝成本', ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        ax.text(cx + 1.34, y + 1.42, cost, ha='left', va='center',
                fontsize=10.5, fontweight='bold', color=col, zorder=3)
        for s in range(4):
            bx = cx + 0.30 + s * 0.48
            fc = col if s < lvl else '#2a3247'
            card(ax, bx, y + 0.92, 0.38, 0.20, fc=fc, ec='none', r=0.05, z=3)
        ax.text(cx + w - 0.30, y + 0.42, f'预计 {sla}', ha='right', va='center',
                fontsize=8.4, color=SUB, zorder=3)

    ax.text(6.5, 0.80, '闸口越往后，拒绝成本越高——所以要把判断尽量往前移',
            ha='center', va='center', fontsize=9.8, color=TXT)
    save(fig, 'gates.png')


# ---------------------------------------------------------------- fig 5
def fig_message():
    fig, ax = canvas()

    ax.text(6.5, 7.58, '把流程状态推到群里', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.20, '一个决策一个卡片，一句话说清要人做什么', ha='center', va='center',
            fontsize=10, color=SUB)

    # left card: approval request
    lx, ly, lw, lh = 0.55, 1.45, 6.85, 5.25
    card(ax, lx, ly, lw, lh, fc=CARD, ec=CYAN, lw=1.3)
    ax.text(lx + 0.32, ly + lh - 0.42, 'APPROVAL', ha='left', va='center',
            fontsize=8.5, fontweight='bold', color=CYAN, zorder=3)
    ax.text(lx + 1.55, ly + lh - 0.42, 'G3 合并 · 项目 Bluefin', ha='left', va='center',
            fontsize=8.5, color=SUB, zorder=3)
    ax.text(lx + 0.32, ly + lh - 0.95, 'PR #241 准备合并', ha='left', va='center',
            fontsize=15, fontweight='bold', color=TXT, zorder=3)

    lines = [
        ('改动', '订单状态机新增 refunded 分支，涉及 4 个文件'),
        ('证据', '单测 128/128，覆盖率 84%，无高危扫描项'),
        ('风险', '影响 3 个下游调用方，已加兼容层'),
        ('请你', '确认 diff 与回滚预案，预计 3 分钟'),
    ]
    ly0 = ly + lh - 1.55
    for i, (k, v) in enumerate(lines):
        yy = ly0 - i * 0.72
        ax.text(lx + 0.32, yy, k, ha='left', va='center',
                fontsize=8.6, color=CYAN if k == '请你' else SUB, zorder=3)
        ax.text(lx + 1.05, yy, v, ha='left', va='center',
                fontsize=9.4, color=TXT, zorder=3)

    card(ax, lx + 0.32, ly + 0.32, 1.55, 0.52, fc='#173a2c', ec=GREEN, lw=1.0, r=0.08)
    ax.text(lx + 1.095, ly + 0.58, '通过并合并', ha='center', va='center',
            fontsize=9.2, fontweight='bold', color=GREEN, zorder=4)
    card(ax, lx + 2.02, ly + 0.32, 1.55, 0.52, fc='#3a1b23', ec=ROSE, lw=1.0, r=0.08)
    ax.text(lx + 2.795, ly + 0.58, '打回并说明', ha='center', va='center',
            fontsize=9.2, fontweight='bold', color=ROSE, zorder=4)

    # right top: blocked
    rx, rw = 7.75, 4.70
    ry, rh = 4.05, 2.65
    card(ax, rx, ry, rw, rh, fc=CARD, ec=ROSE, lw=1.3)
    ax.text(rx + 0.28, ry + rh - 0.38, 'BLOCKED', ha='left', va='center',
            fontsize=8.5, fontweight='bold', color=ROSE, zorder=3)
    ax.text(rx + 1.28, ry + rh - 0.38, 'G2 规格冻结', ha='left', va='center',
            fontsize=8.5, color=SUB, zorder=3)
    ax.text(rx + 0.28, ry + rh - 0.85, 'R-118 验收标准冲突', ha='left', va='center',
            fontsize=11.5, fontweight='bold', color=TXT, zorder=3)
    ax.text(rx + 0.28, ry + rh - 1.28, 'A 方要 3 秒超时，B 方要 10 秒', ha='left', va='center',
            fontsize=9.2, color=TXT, zorder=3)
    ax.text(rx + 0.28, ry + rh - 1.66, '影响 4 个用例，卡住下游 2 个任务', ha='left', va='center',
            fontsize=9.2, color=SUB, zorder=3)
    ax.text(rx + 0.28, ry + 0.32, '@产品负责人  今日 18:00 前裁决', ha='left', va='center',
            fontsize=9.2, fontweight='bold', color=ROSE, zorder=3)

    # right bottom: done
    ry2, rh2 = 1.45, 2.30
    card(ax, rx, ry2, rw, rh2, fc=CARD, ec=GREEN, lw=1.3)
    ax.text(rx + 0.28, ry2 + rh2 - 0.38, 'DONE', ha='left', va='center',
            fontsize=8.5, fontweight='bold', color=GREEN, zorder=3)
    ax.text(rx + 1.28, ry2 + rh2 - 0.38, 'G4 上线 · v2.14.0', ha='left', va='center',
            fontsize=8.5, color=SUB, zorder=3)
    ax.text(rx + 0.28, ry2 + rh2 - 0.90, '已发布，灰度 5%', ha='left', va='center',
            fontsize=11.5, fontweight='bold', color=TXT, zorder=3)
    ax.text(rx + 0.28, ry2 + rh2 - 1.33, '错误率 0.21%  ·  P95 218ms', ha='left', va='center',
            fontsize=9.2, color=TXT, zorder=3)
    ax.text(rx + 0.28, ry2 + 0.34, '回滚指令已备，观察 30 分钟', ha='left', va='center',
            fontsize=9.2, color=SUB, zorder=3)

    save(fig, 'message.png')


if __name__ == '__main__':
    print('generating assets ...')
    fig_pipeline()
    fig_landscape()
    fig_handoff()
    fig_gates()
    fig_message()
    print('done.')
