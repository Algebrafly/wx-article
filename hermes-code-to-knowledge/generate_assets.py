#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0d1117'
PANEL = '#161b22'
CARD = '#21262d'
TEXT = '#e6edf3'
DIM = '#7d8590'
BLUE = '#58a6ff'
GREEN = '#3fb950'
ORANGE = '#d29922'
PURPLE = '#bc8cff'
RED = '#f85149'
CYAN = '#56d4dd'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：五段流水线 ─────────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 6.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.4); ax.axis('off')

    ax.text(6.5, 5.95, '提交 → 知识：五段流水线', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.45, '只有第三段需要 LLM，其余全是确定性脚本', fontsize=12, color=DIM, ha='center')

    steps = [
        ('01', '增量采集', 'GitLab / 云效\n按分支 + 时间窗', BLUE),
        ('02', '变更过滤', 'feature/ fix/\n前缀 + 体积阈值', CYAN),
        ('03', '代码理解', 'diff + 函数上下文\n+ commit / MR', ORANGE),
        ('04', '功能卡片', '结构化 JSON\n可校验可 diff', PURPLE),
        ('05', '写入知识库', 'retain + upsert\n带置信度分级', GREEN),
    ]

    w = 2.28; h = 2.1; gap = 0.22
    total = w * 5 + gap * 4
    x0 = (13 - total) / 2
    yc = 2.9

    for i, (num, title, desc, color) in enumerate(steps):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + 0.22, yc + h / 2 - 0.32, num, fontsize=15, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + w / 2, yc + 0.42, title, fontsize=12, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(x + w / 2, yc - 0.35, desc, fontsize=8.5, color=DIM,
                ha='center', va='center', linespacing=1.6)
        if i < 4:
            ax.annotate('', xy=(x + w + gap - 0.02, yc), xytext=(x + w + 0.02, yc),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))

    # 底部说明
    ax.text(6.5, 1.15, '第二段的过滤规则最关键 —— 决定知识库的噪音比',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')
    ax.add_patch(FancyBboxPatch((3.35, 0.45), 6.3, 0.55,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 0.725, 'cron 每 2h 跑一次，每日 02:00 做一次全量对账',
            fontsize=9, color=TEXT, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：分支与提交过滤漏斗 ─────────────────────────────────────────────────
def draw_scope():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.7, '哪些提交值得变成知识', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.2, '四道闸门，把 90% 的机械提交挡在门外', fontsize=12, color=DIM, ha='center')

    rows = [
        ('全部提交', 'main / develop / hotfix / 所有分支', '约 1000 条/月', DIM, '全量流入'),
        ('分支前缀', 'feature/ · feat/ · fix/ · refactor/', '约 320 条', BLUE, '业务分支'),
        ('提交类型', 'feat / fix / refactor（Conventional）', '约 210 条', CYAN, '有语义的类型'),
        ('变更体积', 'diff < 800 行 且 文件数 < 30', '约 180 条', ORANGE, '过大的拆批'),
        ('进入理解', '合并后 + 有 MR 描述 + 非纯格式化', '约 150 条', GREEN, '最终知识源'),
    ]

    y = 5.3
    for i, (label, cond, count, color, tag) in enumerate(rows):
        # label
        ax.add_patch(FancyBboxPatch((0.5, y - 0.42), 2.1, 0.84,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.55, y, label, fontsize=11.5, fontweight='bold', color=BG,
                ha='center', va='center') if color != DIM else \
            ax.text(1.55, y, label, fontsize=11.5, fontweight='bold', color=TEXT,
                    ha='center', va='center')
        # condition
        ax.add_patch(FancyBboxPatch((2.75, y - 0.42), 6.1, 0.84,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor='#30363d', linewidth=1))
        ax.text(2.95, y, cond, fontsize=9, color=TEXT, ha='left', va='center')
        # count
        ax.text(9.15, y, count, fontsize=10.5, fontweight='bold', color=color,
                ha='left', va='center')
        # tag
        ax.text(11.3, y, tag, fontsize=9, color=DIM, ha='left', va='center')
        y -= 0.95

    ax.text(6.5, 0.55, '150 条/月 × 每条一份功能卡片 ≈ 每月 150 个知识节点',
            fontsize=10, color=DIM, ha='center', va='center')

    save(fig, 'scope.png')


# ── 3：知识图谱 schema ────────────────────────────────────────────────────
def draw_schema():
    fig, ax = plt.subplots(figsize=(13, 8.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 8.2); ax.axis('off')

    ax.text(6.5, 7.7, '功能卡片落库后的图结构', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.22, '六个节点类型，五类关系 —— 智能体靠这张图做多跳检索',
            fontsize=12, color=DIM, ha='center')

    nodes = {
        'feature': (6.5, 5.7, 'Feature\n功能点', PURPLE),
        'module': (3.15, 4.1, 'Module\n代码模块', BLUE),
        'api': (1.25, 5.45, 'API\n对外接口', CYAN),
        'table': (1.25, 2.75, 'Table\n数据表', ORANGE),
        'commit': (6.5, 2.9, 'Commit\n提交记录', DIM),
        'owner': (9.85, 4.1, 'Owner\n研发负责人', GREEN),
    }

    edges = [
        (6.5, 5.7, 3.15, 4.1),
        (3.15, 4.1, 1.25, 5.45),
        (3.15, 4.1, 1.25, 2.75),
        (6.5, 5.7, 6.5, 2.9),
        (6.5, 5.7, 9.85, 4.1),
    ]
    for x1, y1, x2, y2 in edges:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle='-|>', mutation_scale=13,
                                     color=DIM, lw=1.4,
                                     shrinkA=46, shrinkB=46,
                                     zorder=2))

    for key, (x, y, label, color) in nodes.items():
        w, h = 1.52, 0.88
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2,
                                    zorder=3))
        ax.text(x, y, label, fontsize=10.5, fontweight='bold', color=color,
                ha='center', va='center', linespacing=1.5, zorder=4)

    # 关系图例（左下角）
    ax.add_patch(FancyBboxPatch((0.5, 0.35), 5.85, 1.75,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=1.2))
    ax.text(0.75, 1.82, '关系类型', fontsize=9.5, fontweight='bold', color=BLUE, ha='left')
    rels = ['implemented_by：功能由模块实现',
            'exposes：模块对外暴露接口',
            'reads / writes：模块读写数据表',
            'introduced_by：功能由哪次提交引入',
            'owned_by：功能归属哪位负责人']
    y = 1.52
    for r in rels:
        ax.text(0.75, y, r, fontsize=8.2, color=TEXT, ha='left', va='center')
        y -= 0.24

    # 关键字段卡片（右下角）
    ax.add_patch(FancyBboxPatch((6.6, 0.35), 5.9, 1.75,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=CARD, edgecolor=PURPLE, linewidth=1.2))
    ax.text(6.85, 1.82, 'Feature 节点关键字段', fontsize=9.5, fontweight='bold',
            color=PURPLE, ha='left')
    ax.text(6.85, 1.52, 'name / summary / repo / branch', fontsize=8.2, color=TEXT, ha='left')
    ax.text(6.85, 1.28, 'source_commit / confidence', fontsize=8.2, color=TEXT, ha='left')
    ax.text(6.85, 1.04, 'status: draft | verified', fontsize=8.2, color=GREEN, ha='left')
    ax.text(6.85, 0.78, 'ID 规则 feature:{repo}:{slug}', fontsize=8.2, color=DIM, ha='left')

    save(fig, 'schema.png')


# ── 4：配置全景 ───────────────────────────────────────────────────────────
def draw_config():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.75, '配置就是三个文件 + 一个 cron', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.28, '没有隐藏魔法，全部能看到、能改、能版本化', fontsize=12, color=DIM, ha='center')

    # 左侧文件树
    ax.add_patch(FancyBboxPatch((0.5, 1.1), 6.1, 4.75,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=1.6))
    ax.text(0.8, 5.55, '~/.hermes/', fontsize=10, fontweight='bold', color=BLUE, ha='left')

    tree = [
        ('config/', DIM, 5.2),
        ('├─ repos.yaml          # 仓库 · 分支 · 路径过滤', TEXT, 4.85),
        ('├─ schema.yaml         # 卡片字段与校验规则', TEXT, 4.5),
        ('└─ status_map.yaml     # 业务域 → 知识域', TEXT, 4.15),
        ('scripts/', DIM, 3.75),
        ('├─ collect_commits.py  # 采集 + 过滤', TEXT, 3.4),
        ('├─ extract_feature.py  # Agent 阅读理解', ORANGE, 3.05),
        ('└─ upsert_knowledge.py # 写库 + 去重', GREEN, 2.7),
        ('.env', DIM, 2.3),
        ('GITLAB_TOKEN / CODEUP_AK / HINDSIGHT_API_KEY', TEXT, 1.95),
        ('cron/jobs.json', DIM, 1.55),
        ('两个任务：incremental + daily-reconcile', TEXT, 1.25),
    ]
    for txt, color, y in tree:
        ax.text(0.8, y, txt, fontsize=9, color=color, ha='left', va='center')

    # 右侧 cron 卡片
    ax.add_patch(FancyBboxPatch((6.95, 3.6), 5.55, 2.25,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ORANGE, linewidth=1.6))
    ax.text(7.2, 5.55, '增量任务 · 每 2 小时', fontsize=11, fontweight='bold',
            color=ORANGE, ha='left')
    ax.text(7.2, 5.05,
            'hermes cron create "every 2h" \\', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 4.75,
            '  "...scan feature/fix commits..." \\', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 4.45,
            '  --workdir ~/repos/scanner \\', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 4.15,
            '  --name "code-to-knowledge"', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 3.8, '模式：Agent（需要读代码）', fontsize=8.5, color=DIM, ha='left')

    ax.add_patch(FancyBboxPatch((6.95, 1.1), 5.55, 2.2,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.6))
    ax.text(7.2, 3.0, '对账任务 · 每日 02:00', fontsize=11, fontweight='bold',
            color=GREEN, ha='left')
    ax.text(7.2, 2.55, 'hermes cron create "0 2 * * *" \\', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 2.25, '  "...rescan + mark stale..." \\', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 1.95, '  --skill code-to-knowledge \\', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 1.65, '  --name "knowledge-reconcile"', fontsize=8.5, color=TEXT,
            ha='left', va='center', fontfamily='monospace')
    ax.text(7.2, 1.3, '模式：Agent + Skill 注入', fontsize=8.5, color=DIM, ha='left')

    save(fig, 'config.png')


if __name__ == '__main__':
    draw_pipeline(); draw_scope(); draw_schema(); draw_config()
    print('done')
