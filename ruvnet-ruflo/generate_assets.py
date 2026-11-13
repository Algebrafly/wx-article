#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0f1115'; PANEL = '#181b21'; TEXT = '#e8eaed'; TEXT_DIM = '#9aa0a6'
ACC = '#4ea1f7'; ACC2 = '#34d399'; ACC3 = '#f59e0b'; ACC4 = '#f87171'
GRID = '#2a2e36'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# 1. 架构层
def draw_arch():
    fig, ax = plt.subplots(figsize=(11, 8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 11); ax.set_ylim(0, 8); ax.axis('off')

    ax.text(5.5, 7.4, 'Ruflo 架构', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(5.5, 6.8, '模型 + 基座（Harness），Rust 内核，围绕 Claude Code / Codex', fontsize=13, color=TEXT_DIM, ha='center')

    layers = [
        ('LLM Providers', 'Claude · GPT · Gemini · Cohere · Ollama\n(智能路由 + 故障转移)', ACC4, 5.2),
        ('Memory & Learning', 'AgentDB(HNSW) · SONA 自学习 · ReasoningBank · 轨迹学习', ACC3, 4.2),
        ('100+ Agents', 'coder · tester · reviewer · architect · security · trader …', ACC2, 3.2),
        ('Swarm Coordination', '蜂后 / Topology / Raft / 拜占庭 / Gossip', ACC, 2.2),
        ('Orchestration Layer', 'MCP Server · Router · 27 Hooks · 联邦通信', ACC, 1.2),
    ]

    for title, desc, color, y in layers:
        rect = FancyBboxPatch((1.0, y - 0.45), 9.0, 0.9,
                              boxstyle='round,pad=0.05,rounding_size=0.1',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(1.2, y + 0.15, title, fontsize=13, fontweight='bold', color=color, ha='left', va='center')
        ax.text(1.2, y - 0.2, desc, fontsize=10, color=TEXT, ha='left', va='center')

    # User 入口
    rect_top = FancyBboxPatch((3.5, 6.0), 4.0, 0.6,
                              boxstyle='round,pad=0.03,rounding_size=0.1',
                              facecolor=PANEL, edgecolor=TEXT_DIM, linewidth=1)
    ax.add_patch(rect_top)
    ax.text(5.5, 6.3, 'User → Claude Code / CLI / MCP', fontsize=11, color=TEXT, ha='center', va='center')

    # Learning loop 虚线
    ax.annotate('', xy=(10.2, 3.2), xytext=(10.2, 5.2),
                arrowprops=dict(arrowstyle='->', color=ACC2, lw=1.5, linestyle='--'))
    ax.text(10.7, 4.2, 'Learning\nLoop', fontsize=9, color=ACC2, ha='center', va='center', style='italic')

    save(fig, 'arch.png')


# 2. 插件分类
def draw_plugins():
    fig, ax = plt.subplots(figsize=(13, 7.5), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.5); ax.axis('off')

    ax.text(6.5, 7.0, '35 个插件 × 100+ Agent × 314 个 MCP 工具', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.4, '从编排、记忆、学习到安全、联邦、交易——全都有', fontsize=13, color=TEXT_DIM, ha='center')

    cats = [
        ('核心与编排', 6, ACC, 'swarm · autopilot · workflows · federation'),
        ('记忆与知识', 5, ACC2, 'AgentDB · RAG · RVF · ruvector · 图谱'),
        ('智能与学习', 5, ACC3, 'SONA · 图推理 · DAA · RuvLLM · Goals'),
        ('代码质量', 4, ACC4, 'testgen · browser · jujutsu(风险分析) · docs'),
        ('安全与合规', 2, ACC3, 'security-audit · AIDefence(提示词注入)'),
        ('架构方法论', 5, ACC, 'ADR · DDD · SPARC · MetaHarness · Arena'),
        ('DevOps', 3, ACC2, 'migrations · observability · cost-tracker'),
        ('领域专用', 3, ACC4, 'IoT · neural-trader · market-data'),
    ]

    cols = 4; rows = 2
    cell_w = 3.0; cell_h = 2.15
    for idx, (cat, count, color, sub) in enumerate(cats):
        col = idx % cols; row = idx // cols
        x = 0.6 + col * (cell_w + 0.12)
        y = 5.4 - row * (cell_h + 0.3)
        rect = FancyBboxPatch((x, y - cell_h), cell_w, cell_h,
                              boxstyle='round,pad=0.04,rounding_size=0.12',
                              facecolor=PANEL, edgecolor=color, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + 0.22, y - 0.4, cat, fontsize=12, fontweight='bold', color=color, ha='left', va='center')
        ax.text(x + 0.22, y - 1.0, f'{count} 个插件', fontsize=10, color=TEXT_DIM, ha='left', va='center')
        ax.text(x + 0.22, y - 1.65, sub, fontsize=8.5, color=TEXT, ha='left', va='center', linespacing=1.45)

    save(fig, 'plugins.png')


# 3. 对比表
def draw_compare():
    fig, ax = plt.subplots(figsize=(12.5, 6.5), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12.5); ax.set_ylim(0, 6.5); ax.axis('off')

    ax.text(6.25, 6.0, '只用 Claude Code  vs  加上 Ruflo', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6.25, 5.4, '把 harness 装上之后，智能体的能力边界大幅外扩', fontsize=13, color=TEXT_DIM, ha='center')

    rows = [
        ('智能体协作', '相互隔离，无共享上下文', '共享记忆 + 蜂群共识'),
        ('协调机制', '手动编排', '蜂后主导：Raft / 拜占庭 / Gossip'),
        ('记忆', '仅限会话内', 'HNSW 向量记忆，亚毫秒检索'),
        ('学习能力', '行为固定', 'SONA 自学习，ReasoningBank'),
        ('任务路由', '由你决定', '智能路由，准确率 89%'),
        ('后台工作者', '无', '12 个自动触发'),
        ('LLM 提供商', '仅 Anthropic', '5 家 + 故障转移'),
        ('安全性', '标准水平', 'CVE 加固 + AIDefence'),
    ]

    y = 4.75; h = 0.42
    ax.text(2.3, 5.1, '能力', fontsize=11, fontweight='bold', color=TEXT_DIM, ha='center', va='center')
    ax.text(6.25, 5.1, '仅用 Claude Code', fontsize=11, fontweight='bold', color=ACC4, ha='center', va='center')
    ax.text(10.2, 5.1, '+ Ruflo', fontsize=11, fontweight='bold', color=ACC2, ha='center', va='center')
    ax.plot([0.4, 12.1], [4.95, 4.95], color=GRID, lw=1.2)

    for cap, trad, ruf in rows:
        ax.text(0.6, y - h/2, cap, fontsize=10.5, color=TEXT, ha='left', va='center')
        ax.text(4.4, y - h/2, trad, fontsize=9.5, color=TEXT_DIM, ha='left', va='center')
        ax.text(8.4, y - h/2, ruf, fontsize=9.5, color=TEXT, ha='left', va='center', weight='bold' if False else 'normal')
        ax.plot([0.4, 12.1], [y - h - 0.02, y - h - 0.02], color=GRID, lw=0.5, alpha=0.5)
        y -= h + 0.05

    save(fig, 'compare.png')


# 4. 安装路径
def draw_paths():
    fig, ax = plt.subplots(figsize=(12.5, 6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12.5); ax.set_ylim(0, 6); ax.axis('off')

    ax.text(6.25, 5.5, '两条安装路径，覆盖范围差很多', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6.25, 4.9, '插件试用 / CLI 全装，根据需要选', fontsize=13, color=TEXT_DIM, ha='center')

    w = 5.3
    for col, (title, subtitle, color, items, path) in enumerate([
        ('路径 A · 插件', '轻量，只装斜杠命令', ACC4,
         ['每个插件各自有 agent 定义', '工作区零文件写入', '仅核心插件带 MCP', '适合先试用'],
         '/plugin marketplace add ruvnet/ruflo\n/plugin install ruflo-core@ruflo'),
        ('路径 B · CLI 全装', '生产级，完整循环', ACC2,
         ['98 个 agent · 60+ 命令', '30 个 skill · 全部 MCP', '自动装 .claude-flow/ · hooks', '适合生产'],
         'curl -fsSL https://... | bash\nnpx ruflo@latest init wizard'),
    ]):
        x = 0.7 + col * (w + 0.5)
        y = 3.9
        rect = FancyBboxPatch((x, y - 3.0), w, 3.8,
                              boxstyle='round,pad=0.05,rounding_size=0.12',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + 0.65, title, fontsize=14, fontweight='bold', color=color, ha='center', va='center')
        ax.text(x + w/2, y + 0.2, subtitle, fontsize=10, color=TEXT_DIM, ha='center', va='center')
        for i, it in enumerate(items):
            ax.text(x + 0.3, y - 0.35 - i * 0.32, f'•  {it}', fontsize=9.5, color=TEXT, ha='left', va='center')

        # path block
        rect2 = FancyBboxPatch((x + 0.25, y - 2.9), w - 0.5, 0.75,
                               boxstyle='round,pad=0.02,rounding_size=0.08',
                               facecolor='#12141a', edgecolor=GRID, linewidth=1)
        ax.add_patch(rect2)
        ax.text(x + w/2, y - 2.52, path, fontsize=8, color=TEXT_DIM, ha='center', va='center', linespacing=1.4, fontfamily='monospace')

    save(fig, 'paths.png')


if __name__ == '__main__':
    draw_arch(); draw_plugins(); draw_compare(); draw_paths()
    print('done')
