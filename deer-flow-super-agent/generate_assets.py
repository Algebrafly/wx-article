# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
import matplotlib.patheffects as pe

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0c0f17'
PANEL = '#141a2a'
CARD = '#1d2438'
CARD2 = '#262e48'
LINE = '#343d5c'
INDIGO = '#6366f1'
CYAN = '#06b6d4'
EMERALD = '#10b981'
AMBER = '#f59e0b'
ROSE = '#ef4444'
TXT = '#e5e9f0'
SUB = '#8b95aa'
DIM = '#5a6378'

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


# ---------------------------------------------------------------- fig 1 topology
def fig_topology():
    fig, ax = canvas()

    ax.text(6.5, 7.62, 'DeerFlow 2.0 的四层结构', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.22, '一个网关、一个 harness、一个前端、可选的 provisioner',
            ha='center', va='center', fontsize=10, color=SUB)

    # Top row: services
    services = [
        ('Nginx', '2026', '统一反向代理', INDIGO),
        ('Gateway API', '8001', 'FastAPI + LangGraph runtime', CYAN),
        ('Frontend', '3000', 'Next.js chat UI', EMERALD),
        ('Provisioner', '8002', 'K8s sandbox 可选', AMBER),
    ]
    w, gap, h = 2.55, 0.28, 1.30
    x0 = (13 - (w * 4 + gap * 3)) / 2
    sy = 5.25
    for i, (name, port, desc, col) in enumerate(services):
        cx = x0 + i * (w + gap)
        card(ax, cx, sy, w, h, fc=CARD, ec=col, lw=1.3)
        ax.text(cx + 0.18, sy + 0.98, name, ha='left', va='center',
                fontsize=12, fontweight='bold', color=TXT, zorder=3)
        ax.text(cx + 0.18, sy + 0.62, port, ha='left', va='center',
                fontsize=8.5, color=col, zorder=3)
        ax.text(cx + 0.18, sy + 0.32, desc, ha='left', va='center',
                fontsize=8.8, color=SUB, zorder=3)

    # Harness split
    ax.text(0.60, 4.25, 'Backend', ha='left', va='center',
            fontsize=11, fontweight='bold', color=TXT)
    ax.text(0.60, 3.85, '严格单向依赖：App 导入 Harness，Harness 永不导入 App',
            ha='left', va='center', fontsize=8.8, color=SUB)

    hy, hh = 1.45, 2.20
    hx0 = 1.95
    hw = 4.75
    card(ax, hx0, hy, hw, hh, fc=CARD2, ec=CYAN, lw=1.4)
    ax.text(hx0 + 0.20, hy + hh - 0.22, 'Harness（可发布）', ha='left', va='center',
            fontsize=11, fontweight='bold', color=CYAN, zorder=3)
    harness_items = [
        ('deerflow.*', '编排 / 工具 / 沙箱 / 模型 / MCP / Skills'),
        ('DeerFlowClient', '嵌入式 Python 客户端'),
    ]
    ly = hy + hh - 0.62
    for name, desc in harness_items:
        ax.text(hx0 + 0.20, ly, name, ha='left', va='center',
                fontsize=9.2, fontweight='bold', color=TXT, zorder=3)
        ax.text(hx0 + 2.05, ly, desc, ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        ly -= 0.40

    ax.text(hx0 + hw / 2, hy - 0.18, '导入方向', ha='center', va='center',
            fontsize=8.2, color=DIM, zorder=3)
    ax.annotate('', xy=(hx0 + hw / 2, hy - 0.52),
                xytext=(hx0 + hw / 2, hy - 0.02),
                arrowprops=dict(arrowstyle='-|>', color=INDIGO, lw=1.2))

    ax_w = 4.75
    ax_left = hx0 + hw + 0.55
    card(ax, ax_left, hy, ax_w, hh, fc=CARD2, ec=INDIGO, lw=1.4)
    ax.text(ax_left + 0.20, hy + hh - 0.22, 'App（不发布）', ha='left', va='center',
            fontsize=11, fontweight='bold', color=INDIGO, zorder=3)
    app_items = [
        ('app.*', 'Gateway FastAPI + IM 集成'),
        ('deerflow-ext-api', '扩展契约（MCP / Skills）'),
    ]
    ly = hy + hh - 0.62
    for name, desc in app_items:
        ax.text(ax_left + 0.20, ly, name, ha='left', va='center',
                fontsize=9.2, fontweight='bold', color=TXT, zorder=3)
        ax.text(ax_left + 2.30, ly, desc, ha='left', va='center',
                fontsize=8.2, color=SUB, zorder=3)
        ly -= 0.40

    ax.text(6.5, 0.85, 'Gateway 是唯一对外入口，默认 loopback；各会话 thread 数据隔离',
            ha='center', va='center', fontsize=9.5, color=TXT)
    save(fig, 'topology.png')


# ---------------------------------------------------------------- fig 2 harness internals
def fig_harness():
    fig, ax = canvas()

    ax.text(6.5, 7.62, 'Harness 内部：一个 lead agent，六件基础设施', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.22, 'Lead 在 LangGraph 上编排，middleware chain 在每次模型调用前运行',
            ha='center', va='center', fontsize=10, color=SUB)

    # Center lead agent
    cx, cy, cr = 6.5, 4.10, 1.18
    lead = FancyBboxPatch((cx - cr, cy - cr), cr * 2, cr * 2,
                           boxstyle='round,pad=0,rounding_size=0.18',
                           facecolor=CARD2, edgecolor=INDIGO, linewidth=1.8, zorder=3)
    ax.add_patch(lead)
    ax.text(cx, cy + 0.28, 'Lead Agent', ha='center', va='center',
            fontsize=13, fontweight='bold', color=INDIGO, zorder=4)
    ax.text(cx, cy - 0.12, '规划 / 委派', ha='center', va='center',
            fontsize=8.8, color=TXT, zorder=4)
    ax.text(cx, cy - 0.36, '合成 / 校验', ha='center', va='center',
            fontsize=8.8, color=TXT, zorder=4)

    # Six infrastructure cards around the lead
    cards_data = [
        ('Sub-Agents', '隔离上下文 / 工具\n独立 system prompt\n可 snapshot 继承',
         1.85, 5.50, ROSE),
        ('Memory', 'DeerMem 后端\n按 user/agent 防抖\n失败记忆独立保留',
         10.65, 5.50, AMBER),
        ('Sandbox', 'LocalSandbox / Docker\n虚拟路径 /mnt/user-data\n进程 / 资源边界',
         1.85, 2.65, CYAN),
        ('Skills', 'public + custom 目录\n按用户 scope 解析\nreview_skill 校验',
         10.65, 2.65, EMERALD),
        ('Tools', '内置（present / ask）\n配置（bash / read / search）\nMCP 合并注入',
         6.50, 1.55, INDIGO),
        ('Middleware', 'ThreadData → Uploads\n→ Sandbox → Summarization\n→ TodoList → Clarification',
         6.50, 6.72, '#a855f7'),
    ]
    for name, body, bx, by, col in cards_data:
        cw, ch = 2.55, 1.40
        card(ax, bx - cw / 2, by - ch / 2, cw, ch, fc=CARD, ec=col, lw=1.3)
        ax.text(bx, by + ch / 2 - 0.22, name, ha='center', va='center',
                fontsize=10, fontweight='bold', color=col, zorder=3)
        ax.text(bx, by - 0.05, body, ha='center', va='center',
                fontsize=7.8, color=TXT, linespacing=1.38, zorder=3)

        # Draw arrow from card center to lead edge
        dx = cx - bx
        dy = cy - by
        d = (dx ** 2 + dy ** 2) ** 0.5
        if d > 0:
            sx = bx + (cx - bx) / d * (cw / 2)
            sy = by + (cy - by) / d * (ch / 2)
            ex = cx - dx / d * cr
            ey = cy - dy / d * cr
            ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                        arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    # bottom note
    ax.text(6.5, 0.78, 'Sub-agent 不是默认行为：lead 只在并行/专业化/隔离确有净收益时才派活',
            ha='center', va='center', fontsize=9.6, color=TXT)
    save(fig, 'harness.png')


# ---------------------------------------------------------------- fig 3 subagent delegation
def fig_subagent():
    fig, ax = canvas()

    ax.text(6.5, 7.62, 'Lead 怎么派 sub-agent', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.22, '两种上下文模式 + 确定性 receipts + 可验证的验收条件',
            ha='center', va='center', fontsize=10, color=SUB)

    # Left: lead spawning sub-agents
    ax.text(0.60, 6.60, 'Lead Agent', ha='left', va='center',
            fontsize=11, fontweight='bold', color=INDIGO)

    lead_y, lead_h = 5.05, 1.28
    card(ax, 0.55, lead_y, 2.80, lead_h, fc=CARD2, ec=INDIGO, lw=1.3)
    items = ['判断是否需要委派', '拆任务 + termination cond.', '写 acceptance_criteria']
    ly = lead_y + lead_h - 0.22
    for t in items:
        ax.text(0.72, ly, '·  ' + t, ha='left', va='center',
                fontsize=8.4, color=TXT, zorder=3)
        ly -= 0.32

    # Arrow to context_mode choice
    ax.annotate('', xy=(5.35, 5.68), xytext=(3.48, 5.68),
                arrowprops=dict(arrowstyle='-|>', color=INDIGO, lw=1.4))
    ax.text(4.42, 6.06, 'context_mode ?', ha='center', va='center',
            fontsize=9, fontweight='bold', color=SUB)

    # Two context mode cards
    card(ax, 5.45, 5.20, 2.90, 0.95, fc='#1e2442', ec=INDIGO, lw=1.2)
    ax.text(6.90, 5.84, 'isolated', ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=INDIGO, zorder=3)
    ax.text(6.90, 5.50, '只拿委派 prompt', ha='center', va='center',
            fontsize=8.5, color=TXT, zorder=3)

    card(ax, 8.65, 5.20, 3.55, 0.95, fc='#251e33', ec=ROSE, lw=1.2)
    ax.text(10.425, 5.84, 'snapshot', ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=ROSE, zorder=3)
    ax.text(10.425, 5.50, '继承父对话 + compaction 摘要', ha='center', va='center',
            fontsize=8.5, color=TXT, zorder=3)

    # Arrow down
    ax.annotate('', xy=(6.90, 4.48), xytext=(6.90, 5.28),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))
    ax.annotate('', xy=(10.425, 4.48), xytext=(10.425, 5.28),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    # Sub-agent instances
    agents_data = [
        ('Sub-Agent A', 'model: Doubao-Seed', 'tools: bash,web', '独立 system prompt', CYAN, 6.90),
        ('Sub-Agent B', 'model: DeepSeek', 'tools: search', '独立 history', EMERALD, 10.425),
    ]
    for name, mdl, tls, iso, col, xc in agents_data:
        card(ax, xc - 1.50, 3.45, 3.00, 1.00, fc=CARD, ec=col, lw=1.3)
        ax.text(xc, 4.15, name, ha='center', va='center',
                fontsize=10.5, fontweight='bold', color=col, zorder=3)
        ax.text(xc, 3.82, mdl, ha='center', va='center',
                fontsize=8.2, color=TXT, zorder=3)
        ax.text(xc, 3.55, tls + '  |  ' + iso, ha='center', va='center',
                fontsize=7.8, color=SUB, zorder=3)

    # Return path
    ax.annotate('', xy=(6.90, 2.95), xytext=(6.90, 3.45),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))
    ax.annotate('', xy=(10.425, 2.95), xytext=(10.425, 3.45),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    # Verification bar
    card(ax, 5.05, 2.15, 6.75, 0.78, fc='#1a2230', ec=AMBER, lw=1.2)
    ax.text(8.425, 2.73, 'Lead 校验', ha='center', va='center',
            fontsize=9.8, fontweight='bold', color=AMBER, zorder=3)
    ax.text(8.425, 2.38, 'receipts 账本 / acceptance_criteria 自动判定 / 合成输出',
            ha='center', va='center', fontsize=8.2, color=TXT, zorder=3)

    # Cancel row
    ax.text(6.5, 1.40, '被中断的 sub-agent 保留 execution slot，cleanup 完成才释放',
            ha='center', va='center', fontsize=9.2, color=SUB)

    ax.text(6.5, 0.72, '规则：lead 只在并行/专业化/隔离确有净收益时派活，别为大任务硬拆',
            ha='center', va='center', fontsize=9.6, color=TXT)
    save(fig, 'subagent.png')


# ---------------------------------------------------------------- fig 4 context
def fig_context():
    fig, ax = canvas()

    ax.text(6.5, 7.62, '三大子系统怎么配合', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.22, '目标 → 上下文压缩 → 长期记忆，各自独立又互相补位',
            ha='center', va='center', fontsize=10, color=SUB)

    # 3 big cards
    cards = [
        ('Session Goals', EMERALD,
         '/goal 挂到线程，跨轮生效',
         'evaluator 每次 run 后评估',
         'blocker: needs_user_input / run_failed / ...',
         '隐藏 continuation 自动续跑，最多 8 次'),
        ('Context Compaction', CYAN,
         'token 逼近窗口时触发',
         '老消息压缩成摘要',
         '隐藏 durable context 注入',
         'sub-agent 独立 compact，系统指令保留'),
        ('Long-Term Memory', AMBER,
         'DeerMem + Mem0 后端',
         '按 conversation / user / agent 防抖',
         '30s 安静期，300s 硬上限',
         '紧急 snapshot 独立队列'),
    ]
    w, gap, h = 3.80, 0.25, 4.40
    x0 = (13 - (w * 3 + gap * 2)) / 2
    y = 1.30
    for i, (title, col, p1, p2, p3, p4) in enumerate(cards):
        cx = x0 + i * (w + gap)
        card(ax, cx, y, w, h, fc=CARD, ec=col, lw=1.4)
        ax.text(cx + 0.25, y + h - 0.38, title, ha='left', va='center',
                fontsize=12, fontweight='bold', color=col, zorder=3)
        ax.plot([cx + 0.25, cx + w - 0.25], [y + h - 0.62, y + h - 0.62],
                color=LINE, lw=0.9, zorder=2)
        points = [p1, p2, p3, p4]
        py = y + h - 1.05
        for pt in points:
            ax.text(cx + 0.25, py, '·  ' + pt, ha='left', va='center',
                    fontsize=8.7, color=TXT, linespacing=1.6, zorder=3)
            py -= 0.72

    ax.text(6.5, 0.82, '三者共同目标：让 lead 在 100k+ context 里持续聚焦、不丢用户意图',
            ha='center', va='center', fontsize=9.8, color=TXT)
    save(fig, 'context.png')


# ---------------------------------------------------------------- fig 5 bridge
def fig_bridge():
    fig, ax = canvas()

    ax.text(6.5, 7.62, 'Gateway 把 IM 接进同一个 agent', ha='center', va='center',
            fontsize=15.5, fontweight='bold', color=TXT)
    ax.text(6.5, 7.22, '飞书、Slack、Telegram、Discord、钉钉桥到同一套 runtime',
            ha='center', va='center', fontsize=10, color=SUB)

    # Left: IM channels
    channels = [
        ('Feishu', '飞书', '#00d6b9'),
        ('Slack', 'Slack', '#4a154b'),
        ('Telegram', 'Telegram', '#229ed9'),
        ('Discord', 'Discord', '#5865f2'),
        ('DingTalk', '钉钉', '#1677ff'),
    ]
    cw, ch = 1.90, 0.55
    cy = 5.75
    gap = 0.15
    total = len(channels) * cw + (len(channels) - 1) * gap
    cx0 = (13 - total) / 2
    for i, (en, zh, col) in enumerate(channels):
        cx = cx0 + i * (cw + gap)
        card(ax, cx, cy, cw, ch, fc=CARD, ec=col, lw=1.2)
        ax.text(cx + cw / 2, cy + 0.35, zh, ha='center', va='center',
                fontsize=9.8, fontweight='bold', color=TXT, zorder=3)
        ax.text(cx + cw / 2, cy + 0.13, en, ha='center', va='center',
                fontsize=7.6, color=SUB, zorder=3)

    # Arrow down to Gateway
    ax.annotate('', xy=(6.5, 4.92), xytext=(6.5, cy),
                arrowprops=dict(arrowstyle='-|>', color=INDIGO, lw=1.5))
    ax.text(6.5, 5.32, '统一协议', ha='center', va='center',
            fontsize=9, color=INDIGO)

    # Gateway card
    gw_x, gw_y, gw_w, gw_h = 2.80, 3.75, 7.40, 1.00
    card(ax, gw_x, gw_y, gw_w, gw_h, fc=CARD2, ec=INDIGO, lw=1.5)
    ax.text(6.5, gw_y + gw_h - 0.30, 'Gateway FastAPI', ha='center', va='center',
            fontsize=11, fontweight='bold', color=INDIGO, zorder=3)
    ax.text(6.5, gw_y + gw_h - 0.62, 'LangGraph runtime + Thread isolation + Sandbox 调度',
            ha='center', va='center', fontsize=9, color=TXT, zorder=3)

    # Arrow from Gateway down
    ax.annotate('', xy=(6.5, 3.20), xytext=(6.5, gw_y),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.0))

    # Harness run lifecycle
    ax.text(0.60, 2.80, 'Run lifecycle（同一条）', ha='left', va='center',
            fontsize=9.5, fontweight='bold', color=SUB)
    lifecycle = ['RunManager', 'run_agent()', 'StreamBridge', 'SSE 流式输出']
    lx = 0.60
    ly = 2.45
    for i, step in enumerate(lifecycle):
        card(ax, lx + i * 1.95, ly, 1.75, 0.50, fc=CARD, ec=CYAN, lw=1.0)
        ax.text(lx + i * 1.95 + 0.875, ly + 0.25, step, ha='center', va='center',
                fontsize=8.5, color=TXT, zorder=3)
        if i < len(lifecycle) - 1:
            ax.annotate('', xy=(lx + (i + 1) * 1.95, ly + 0.25),
                        xytext=(lx + i * 1.95 + 1.75, ly + 0.25),
                        arrowprops=dict(arrowstyle='-|>', color=DIM, lw=0.9))

    # Left-bottom: lessons
    ax.text(0.60, 1.55, '启发', ha='left', va='center',
            fontsize=11, fontweight='bold', color=AMBER)
    lessons = [
        '桥接层只管协议转换，不复制 agent 逻辑',
        '定时任务走同一条 run lifecycle，只是 scheduler 决定何时触发',
        'sub-agent execution_id 带 run 维度，provider tool_call_id 不唯一',
    ]
    ly2 = 1.25
    for l in lessons:
        ax.text(0.75, ly2, '·  ' + l, ha='left', va='center',
                fontsize=8.5, color=TXT, linespacing=1.55, zorder=3)
        ly2 -= 0.26

    save(fig, 'bridge.png')


if __name__ == '__main__':
    print('generating assets ...')
    fig_topology()
    fig_harness()
    fig_subagent()
    fig_context()
    fig_bridge()
    print('done.')
