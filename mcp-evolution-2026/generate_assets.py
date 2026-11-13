#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import matplotlib.patches as mpatches

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

# 字体
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 统一配色
BG = '#0f1115'
PANEL = '#181b21'
TEXT = '#e8eaed'
TEXT_DIM = '#9aa0a6'
ACCENT = '#4ea1f7'
ACCENT2 = '#34d399'
ACCENT3 = '#f59e0b'
ACCENT4 = '#f87171'
GRID = '#2a2e36'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 图 1：演进时间线 ──────────────────────────────────────────────────────
def draw_evolution():
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(6, 6.5, 'MCP 协议演进时间线', fontsize=22, fontweight='bold',
            color=TEXT, ha='center', va='center')
    ax.text(6, 5.9, '从 Function Calling 到通用连接层，只用了一年半', fontsize=13,
            color=TEXT_DIM, ha='center', va='center')

    # 主线
    ax.plot([1.5, 10.5], [4, 4], color=ACCENT, linewidth=3, alpha=0.6)

    events = [
        (2.5, '2023 Q4', 'Function Calling\n各家大模型自己定义\n工具调用格式'),
        (5.0, '2024 Q4', 'MCP 首秀\nAnthropic 开源协议\n本地 stdio transport'),
        (7.5, '2025 Q2', 'MCP 1.0\nResources + Prompts\nSSE remote transport'),
        (10.0, '2026 现在', '网关与安全\nAuth / Registry /\n多 Agent 编排'),
    ]

    for x, t, desc in events:
        # 节点
        circle = Circle((x, 4), 0.16, color=ACCENT, zorder=5)
        ax.add_patch(circle)
        # 时间
        ax.text(x, 4.65, t, fontsize=13, fontweight='bold', color=ACCENT,
                ha='center', va='center')
        # 描述框
        ax.text(x, 3.0, desc, fontsize=11, color=TEXT, ha='center', va='top',
                linespacing=1.5,
                bbox=dict(boxstyle='round,pad=0.45', facecolor=PANEL,
                          edgecolor=GRID, linewidth=1.2))

    # 底部注
    ax.text(6, 1.0, '节点间距不是真实时间比例，而是阶段跃迁的象征。', fontsize=11,
            color=TEXT_DIM, ha='center', va='center', style='italic')

    save(fig, 'evolution.png')


# ── 图 2：架构三层模型 ─────────────────────────────────────────────────────
def draw_architecture():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(6, 7.4, 'MCP 的连接模型：三层解耦', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.8, 'Host 管生命周期，Client 管会话，Server 管能力', fontsize=13,
            color=TEXT_DIM, ha='center')

    layers = [
        (6, 5.6, 'Host', 'Claude / Cursor / OpenCode / Trae\n启动多个 Client，管理权限'),
        (6, 3.9, 'Client', '每个 Server 一个连接实例\n维护会话、路由请求'),
        (6, 2.2, 'Server', 'Database / Browser / Git / Slack\n暴露 tools / resources / prompts'),
    ]

    for x, y, title, desc in layers:
        w, h = 7.5, 1.1
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle='round,pad=0.05,rounding_size=0.15',
                              facecolor=PANEL, edgecolor=ACCENT, linewidth=2)
        ax.add_patch(rect)
        ax.text(x - w/2 + 0.4, y + 0.15, title, fontsize=16, fontweight='bold',
                color=ACCENT, ha='left', va='center')
        ax.text(x - w/2 + 0.4, y - 0.25, desc, fontsize=11,
                color=TEXT_DIM, ha='left', va='center', linespacing=1.4)

    # 双向箭头
    for y in [4.7, 3.0]:
        ax.annotate('', xy=(5.4, y - 0.5), xytext=(5.4, y + 0.5),
                    arrowprops=dict(arrowstyle='<->', color=ACCENT2, lw=2))

    # 两侧 Transport & Capability
    ax.text(1.2, 4, 'Transport', fontsize=14, fontweight='bold', color=ACCENT3,
            ha='center', rotation=90, va='center')
    ax.text(1.2, 3.0, 'stdio · SSE · Streamable HTTP', fontsize=10,
            color=TEXT_DIM, ha='center', rotation=90, va='center')

    ax.text(10.8, 4, 'Capability', fontsize=14, fontweight='bold', color=ACCENT4,
            ha='center', rotation=90, va='center')
    ax.text(10.8, 3.0, 'tools · resources · prompts', fontsize=10,
            color=TEXT_DIM, ha='center', rotation=90, va='center')

    save(fig, 'architecture.png')


# ── 图 3：生态矩阵 ─────────────────────────────────────────────────────────
def draw_ecosystem():
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(6, 7.4, 'MCP 生态支持矩阵', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.8, '不是谁「支持」了 MCP，而是谁不想被排除在 Agent 生态外', fontsize=13,
            color=TEXT_DIM, ha='center')

    categories = [
        ('IDE / 编辑器', ['Claude Desktop', 'Cursor', 'Trae', 'OpenCode', 'Cline']),
        ('框架 / SDK', ['LangChain', 'LlamaIndex', 'Pydantic AI', 'FastMCP', 'mcp-go']),
       ('平台 / 云', ['Cloudflare', 'Smithery', 'OpenRouter', 'Pulsemcp', 'Zapier']),
    ]

    y_start = 5.8
    box_h = 1.0
    for i, (cat, items) in enumerate(categories):
        y = y_start - i * 1.65
        ax.text(0.8, y, cat, fontsize=14, fontweight='bold', color=ACCENT,
                ha='left', va='center')
        x = 3.5
        for item in items:
            rect = FancyBboxPatch((x, y - box_h/2), 1.5, box_h,
                                  boxstyle='round,pad=0.02,rounding_size=0.1',
                                  facecolor=PANEL, edgecolor=GRID, linewidth=1)
            ax.add_patch(rect)
            ax.text(x + 0.75, y, item, fontsize=10, color=TEXT, ha='center', va='center')
            x += 1.75

    # 底部图例
    ax.text(6, 1.3, '支持度说明：深色块 = 已原生集成或提供官方 SDK，浅色块 = 通过社区实现。',
            fontsize=10, color=TEXT_DIM, ha='center', va='center')

    save(fig, 'ecosystem.png')


# ── 图 4：趋势四象限 ──────────────────────────────────────────────────────
def draw_roadmap():
    fig, ax = plt.subplots(figsize=(11, 9), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # 轴
    ax.axhline(5, color=GRID, linewidth=1.5)
    ax.axvline(5, color=GRID, linewidth=1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 标题
    ax.text(5, 9.5, 'MCP 下一阶段：四象限趋势', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(5, 8.9, '横轴：成熟度；纵轴：对开发者的影响力', fontsize=13,
            color=TEXT_DIM, ha='center')

    # 轴标签
    ax.text(1.2, 5.2, '低成熟度', fontsize=11, color=TEXT_DIM, ha='center')
    ax.text(8.8, 5.2, '高成熟度', fontsize=11, color=TEXT_DIM, ha='center')
    ax.text(5.2, 1.0, '低影响力', fontsize=11, color=TEXT_DIM, ha='left')
    ax.text(5.2, 9.0, '高影响力', fontsize=11, color=TEXT_DIM, ha='left')

    quadrants = [
        # (x, y, 标题, 说明, 颜色)
        (2.5, 7.5, '安全与权限', 'OAuth / Scope / 审计\nAgent 调用前的身份边界', ACCENT4),
        (7.5, 7.5, '网关与发现', 'MCP Router / Registry\n像 npm 一样发现 server', ACCENT),
        (2.5, 2.5, '多模态与状态', '图片/音频资源、长会话状态\n标准还在早期', ACCENT3),
        (7.5, 2.5, '编排与自动化', '多 Agent 协作、工作流引擎\n2026 年落地最快', ACCENT2),
    ]

    for x, y, title, desc, color in quadrants:
        circle = Circle((x, y), 1.15, color=color, alpha=0.18)
        ax.add_patch(circle)
        ax.text(x, y + 0.25, title, fontsize=15, fontweight='bold', color=color,
                ha='center', va='center')
        ax.text(x, y - 0.35, desc, fontsize=10, color=TEXT, ha='center', va='center',
                linespacing=1.5)

    # 中心标注
    ax.text(5, 5, '协议核心\n稳定', fontsize=12, color=TEXT_DIM, ha='center', va='center')

    save(fig, 'roadmap.png')


if __name__ == '__main__':
    draw_evolution()
    draw_architecture()
    draw_ecosystem()
    draw_roadmap()
    print('4 张配图已生成到', ASSETS)
