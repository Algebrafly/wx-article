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
ACCENT = '#f87171'; ACCENT2 = '#fbbf24'; ACCENT3 = '#34d399'; ACCENT4 = '#4ea1f7'
GRID = '#2a2e36'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


def arrows_between(ax, xs, y, color=GRID, lw=2):
    for i in range(len(xs) - 1):
        ax.annotate('', xy=(xs[i+1] - 0.15, y), xytext=(xs[i] + 0.15, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw))


# ── 1：六阶段主流程 + artifact ──────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 6.5), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.5); ax.axis('off')

    ax.text(6.5, 6.0, '六阶段安全审计流水线', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.4, '每个阶段由独立 agent 执行，互不共用上下文', fontsize=13, color=TEXT_DIM, ha='center')

    stages = [
        ('Recon\n侦察', 'architecture.md\ncoverage-ledger.json', ACCENT4),
        ('Hunting\n狩猎', '孤立 hunters\ncoverage critics', ACCENT3),
        ('Validation\n验证', 'fresh verifiers\n独立 disprove', ACCENT2),
        ('Output\n输出', 'findings.json\n+ report-schema', ACCENT),
        ('Verification\n复核', 'fresh agents\nmaterial replacement', ACCENT4),
        ('Reporting\n报告', 'REPORT.md\nFINDINGS-DETAIL.md', ACCENT3),
    ]

    x = 0.6
    w = 1.8; h = 2.2
    for i, (title, artifact, color) in enumerate(stages):
        rect = FancyBboxPatch((x, 2.4), w, h,
                              boxstyle='round,pad=0.04,rounding_size=0.12',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, 4.15, title, fontsize=12, fontweight='bold',
                color=color, ha='center', va='center', linespacing=1.35)
        ax.text(x + w/2, 3.25, f'Phase {i+1}', fontsize=9, color=TEXT_DIM,
                ha='center', va='center')
        ax.text(x + w/2, 2.6, artifact, fontsize=8.5, color=TEXT,
                ha='center', va='center', linespacing=1.4)
        if i < len(stages) - 1:
            ax.annotate('', xy=(x + w + 0.1, 3.5), xytext=(x + w - 0.1, 3.5),
                        arrowprops=dict(arrowstyle='->', color=GRID, lw=2))
        x += w + 0.28

    # 底部：循环箭头（多次运行）
    ax.annotate('', xy=(0.6, 1.5), xytext=(12.0, 1.5),
                arrowprops=dict(arrowstyle='->', color=ACCENT2, lw=1.8,
                               connectionstyle='arc3,rad=-0.2'))
    ax.text(6.5, 1.2, '多次运行。新的 ledger 基于上一次的 findings，定向覆盖缺口。',
            fontsize=11, color=TEXT_DIM, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：攻击类别矩阵 ──────────────────────────────────────────────────────
def draw_attack_matrix():
    fig, ax = plt.subplots(figsize=(12.5, 7), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12.5); ax.set_ylim(0, 7); ax.axis('off')

    ax.text(6.25, 6.5, '10 类攻击向量', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6.25, 5.9, '按目标类型加载不同的 hunting prompts', fontsize=13, color=TEXT_DIM, ha='center')

    classes = [
        ('核心与通配攻击', 'common + wildcard prompts', ACCENT),
        ('内存安全与二进制', 'C / C++ / 内核 / 原生', ACCENT2),
        ('AI / LLM', 'prompt injection / agent / tool', ACCENT3),
        ('Web 协议与认证', 'HTTP framing / cache / auth', ACCENT4),
        ('客户端', 'DOM 注入 / 原型污染', ACCENT3),
        ('供应链与发布', '依赖 / CI / 签名 / 插件', ACCENT4),
        ('云与部署', 'IAM / IaC / serverless / ingress', ACCENT2),
        ('RPC 与消息协议', '序列化 / queue / broker', ACCENT),
        ('资源耗尽', 'quota / queue / worker / spend', ACCENT4),
        ('数据隔离与生命周期', 'tenant / backup / migration', ACCENT3),
    ]

    rows = 2; cols = 5
    cell_w = 2.3; cell_h = 1.7
    start_x = 0.8; start_y = 4.9

    for idx, (label, sub, color) in enumerate(classes):
        col = idx % cols
        row = idx // cols
        x = start_x + col * (cell_w + 0.1)
        y = start_y - row * (cell_h + 0.25)
        rect = FancyBboxPatch((x, y - cell_h), cell_w, cell_h,
                              boxstyle='round,pad=0.03,rounding_size=0.1',
                              facecolor=PANEL, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + cell_w/2, y - cell_h + 0.6, f'0{idx+1}', fontsize=10,
                fontweight='bold', color=TEXT_DIM, ha='center', va='center')
        ax.text(x + cell_w/2, y - cell_h + 1.1, label, fontsize=10.5,
                fontweight='bold', color=color, ha='center', va='center', linespacing=1.3)
        ax.text(x + cell_w/2, y - cell_h + 1.45, sub, fontsize=8,
                color=TEXT_DIM, ha='center', va='center', linespacing=1.3)

    save(fig, 'attack-matrix.png')


# ── 3：设计原则 ──────────────────────────────────────────────────────────
def draw_principles():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.axis('off')

    ax.text(6, 6.0, '六条核心设计原则', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6, 5.4, '每一条都是反直觉的 hardening 决策', fontsize=13, color=TEXT_DIM, ha='center')

    principles = [
        ('只确认已建立的边界失败', 'source-grounded blocked lead 一律归为 needs_validation，带 exact unresolved fact', ACCENT),
        ('对抗性验证', '发现漏洞的 agent 永远不是验证它的 agent。找 fresh verifier 去 disprove', ACCENT4),
        ('严重性需要 impact', 'likelihood × impact，不是偏离 checklist 的程度', ACCENT2),
        ('纵深防御缺口 ≠ 漏洞', 'Layer A 挡住了，Layer B 不存在只是 hardening note', ACCENT3),
        ('多次运行提高覆盖率', 'Cloudflare 测试里单次只能发现最终发现总数的一半', ACCENT),
        ('三段 verdicts', 'confirmed / needs_validation / rejected，各自有明确 schema', ACCENT4),
    ]

    for i, (title, desc, color) in enumerate(principles):
        col = i % 3; row = i // 3
        x = 0.6 + col * 3.9
        y = 4.6 - row * 2.3
        rect = FancyBboxPatch((x, y - 1.8), 3.6, 1.8,
                              boxstyle='round,pad=0.04,rounding_size=0.12',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + 0.25, y - 0.25, f'0{i+1}', fontsize=14, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + 0.25, y - 0.75, title, fontsize=12.5, fontweight='bold',
                color=TEXT, ha='left', va='center')
        ax.text(x + 0.25, y - 1.35, desc, fontsize=9, color=TEXT_DIM,
                ha='left', va='center', linespacing=1.45)

    save(fig, 'principles.png')


# ── 4：采纳路径 ──────────────────────────────────────────────────────────
def draw_adoption():
    fig, ax = plt.subplots(figsize=(12.5, 6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12.5); ax.set_ylim(0, 6); ax.axis('off')

    ax.text(6.25, 5.5, '三步跑起来', fontsize=22, fontweight='bold', color=TEXT, ha='center')
    ax.text(6.25, 4.9, '一个命令装，一句话启动，一份目录看全部产物', fontsize=13, color=TEXT_DIM, ha='center')

    steps = [
        ('1', '安装', 'npx skills add\nhttps://github.com/\ncloudflare/security-audit-skill', ACCENT4),
        ('2', '启动 agent\n并让它读代码库', 'security audit this codebase\nfind security vulnerabilities\nin ./src', ACCENT3),
        ('3', '读取产物目录', '~/.security-audit-skill/\n<repo>/run-<N>/\nREPORT.md + findings', ACCENT2),
    ]

    x = 1.0; w = 3.2
    for num, title, body, color in steps:
        rect = FancyBboxPatch((x, 1.0), w, 3.5,
                              boxstyle='round,pad=0.06,rounding_size=0.15',
                              facecolor=PANEL, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + 0.25, 4.1, num, fontsize=28, fontweight='bold', color=color, ha='left', va='center')
        ax.text(x + w/2, 3.3, title, fontsize=15, fontweight='bold', color=TEXT, ha='center', va='center', linespacing=1.3)
        ax.text(x + w/2, 2.1, body, fontsize=9.5, color=TEXT_DIM, ha='center', va='center', linespacing=1.5)
        ax.text(x + w/2, 1.25, '零外部依赖，schema 已内置', fontsize=8.5,
                color=color, ha='center', va='center', style='italic')
        if num != '3':
            ax.annotate('', xy=(x + w + 0.15, 2.75), xytext=(x + w - 0.15, 2.75),
                        arrowprops=dict(arrowstyle='->', color=GRID, lw=2))
        x += w + 0.55

    save(fig, 'adoption.png')


if __name__ == '__main__':
    draw_pipeline(); draw_attack_matrix(); draw_principles(); draw_adoption()
    print('4 张配图已生成到', ASSETS)
