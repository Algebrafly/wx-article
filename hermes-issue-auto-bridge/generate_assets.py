#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0f172a'
PANEL = '#1e293b'
TEXT = '#e2e8f0'
DIM = '#64748b'
RED = '#ef4444'
ORANGE = '#f97316'
GREEN = '#22c55e'
BLUE = '#3b82f6'
PURPLE = '#a855f7'
CYAN = '#06b6d4'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：7 步闭环流水线 ────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis('off')

    ax.text(6.5, 6.55, '业务群 → 项目管理平台：7 步自动闭环', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.05, 'Hermes Agent + MCP 桥接，把"这个功能不对"变成一条带责任人的 Bug',
            fontsize=12, color=DIM, ha='center')

    steps = [
        ('1', '群消息监听', '企微 / 飞书\nGateway 长连', BLUE),
        ('2', '语义检测', '识别 BUG / 优化\n过滤闲聊', ORANGE),
        ('3', '实体提取', '产品名 / 接口\n报错信息', CYAN),
        ('4', '责任人归属', '知识库 + Git\ncode-owner', PURPLE),
        ('5', '创建 Issue', 'Jira / Zentao\nPingCode / Yunxiao', RED),
        ('6', '通知回流', '推回业务群\n私信负责人', GREEN),
        ('7', '状态追踪', 'Issue 变更\n自动同步', BLUE),
    ]

    w = 1.55; h = 1.45; gap = 0.18
    total_w = w * 7 + gap * 6
    x_start = (13 - total_w) / 2
    y_center = 2.75

    for i, (num, title, desc, color) in enumerate(steps):
        x = x_start + i * (w + gap)
        # card
        ax.add_patch(FancyBboxPatch((x, y_center - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        # num badge
        ax.add_patch(FancyBboxPatch((x + w / 2 - 0.28, y_center + h / 2 - 0.52), 0.56, 0.48,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2, y_center + h / 2 - 0.28, num, fontsize=14, fontweight='bold',
                color=BG, ha='center', va='center')
        # title
        ax.text(x + w / 2, y_center + 0.25, title, fontsize=10, fontweight='bold',
                color=TEXT, ha='center', va='center')
        # desc
        ax.text(x + w / 2, y_center - 0.35, desc, fontsize=8, color=DIM,
                ha='center', va='center', linespacing=1.4)
        # arrow
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + w + gap - 0.03, y_center),
                        xytext=(x + w + 0.02, y_center),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))

    # loop-back arrow (step 7 → step 5)
    loop_x_start = x_start + w * 6 + gap * 5 + 0.02
    loop_x_end = x_start + w * 4 + gap * 3 - 0.02
    ax.annotate('', xy=(loop_x_end, y_center + h / 2 + 0.4),
                xytext=(loop_x_start, y_center + h / 2 + 0.4),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.8,
                                connectionstyle='arc3,rad=-0.15'))
    ax.text((loop_x_start + loop_x_end) / 2, y_center + h / 2 + 0.62,
            'Issue 状态变更 → 回写群', fontsize=8, color=GREEN, ha='center')

    save(fig, 'pipeline.png')


# ── 2：意图分类决策树 ────────────────────────────────────────────────────
def draw_intent():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.7, '意图分类：一条群消息怎么走', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.2, 'LLM + 关键词规则双层过滤，把噪音降到最低', fontsize=12, color=DIM, ha='center')

    # root: incoming message
    rx, ry = 6.5, 5.1
    ax.add_patch(FancyBboxPatch((rx - 1.6, ry - 0.45), 3.2, 0.9,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=2))
    ax.text(rx, ry, '群消息流入', fontsize=13, fontweight='bold',
            color=BLUE, ha='center', va='center')

    # layer 1: three intents
    layer1 = [
        (2.8, 3.6, 'BUG / 异常', RED, '"报错" "打不开"\n"乱码" "挂了"'),
        (6.5, 3.6, '优化 / 需求', ORANGE, '"能不能"\n"希望" "建议"'),
        (10.2, 3.6, '咨询 / 闲聊', DIM, '"怎么用"\n"@某人" 闲聊'),
    ]
    for lx, ly, label, color, desc in layer1:
        ax.add_patch(FancyBboxPatch((lx - 1.5, ly - 0.5), 3.0, 1.0,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.8))
        ax.text(lx, ly + 0.12, label, fontsize=12, fontweight='bold',
                color=color if color != DIM else TEXT, ha='center', va='center')
        ax.text(lx, ly - 0.25, desc, fontsize=7.5, color=DIM,
                ha='center', va='center', linespacing=1.35)
        # arrow from root
        ax.annotate('', xy=(lx, ly + 0.5), xytext=(rx, ry - 0.45),
                    arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2,
                                    connectionstyle='arc3,rad=0'))

    # layer 2: further processing
    layer2 = [
        (2.8, 2.1, '提取实体', '产品名 / 接口 / 报错', CYAN),
        (6.5, 2.1, '写 issue draft', '标题 + 描述 + 优先级', PURPLE),
        (10.2, 2.1, '丢弃 / 回复', '不进入工单系统', '#475569'),
    ]
    for lx, ly, label, desc, color in layer2:
        ax.add_patch(FancyBboxPatch((lx - 1.4, ly - 0.4), 2.8, 0.8,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(lx, ly + 0.05, label, fontsize=10, fontweight='bold',
                color=color, ha='center', va='center')
        ax.text(lx, ly - 0.22, desc, fontsize=7.5, color=DIM, ha='center')
        # arrow from layer1
        ly1_top = 3.6 + 0.5
        ax.annotate('', xy=(lx, ly + 0.4), xytext=(lx, ly1_top - 0.05),
                    arrowprops=dict(arrowstyle='->', color=DIM, lw=1.1))

    # layer 3
    ax.add_patch(FancyBboxPatch((4.7, 0.7), 3.6, 0.9,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=2))
    ax.text(6.5, 1.15, '进入"责任人归属"模块', fontsize=11, fontweight='bold',
            color=GREEN, ha='center', va='center')

    # arrows from layer2 items 1,2 → layer3
    for src_x in [2.8, 6.5]:
        ax.annotate('', xy=(6.5, 1.6), xytext=(src_x, 2.1 - 0.4),
                    arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.3,
                                    connectionstyle='arc3,rad=0'))

    save(fig, 'intent_engine.png')


# ── 3：责任人归属链路 ────────────────────────────────────────────────────
def draw_owner():
    fig, ax = plt.subplots(figsize=(13, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6.5, 6.3, '从产品名到研发负责人：归属链路', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.8, '三条路径互补，命中任何一条就能拿到 owner', fontsize=12, color=DIM, ha='center')

    # source
    sx, sy = 6.5, 4.6
    ax.add_patch(FancyBboxPatch((sx - 1.5, sy - 0.4), 3.0, 0.8,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=2))
    ax.text(sx, sy, '产品名 / 接口名', fontsize=11, fontweight='bold',
            color=BLUE, ha='center', va='center')

    # three paths
    paths = [
        (2.5, '知识库映射', 'Hermes Memory Provider\nHindsight / Neo4j\n业务域 → 团队 owner', PURPLE),
        (6.5, '代码仓库', 'MCP GitHub / GitLab\n按接口路径 grep\nGit blame 作者', CYAN),
        (10.5, '团队目录', '企业通讯录 MCP\n业务域 → 部门 → 人\nOrg chart lookup', ORANGE),
    ]
    for px, label, desc, color in paths:
        ax.add_patch(FancyBboxPatch((px - 1.55, 2.5), 3.1, 1.8,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.8))
        ax.text(px, 4.05, label, fontsize=12, fontweight='bold',
                color=color, ha='center', va='center')
        ax.text(px, 3.3, desc, fontsize=8.5, color=TEXT,
                ha='center', va='center', linespacing=1.45)
        # arrow from source
        ax.annotate('', xy=(px, 4.3), xytext=(sx, sy - 0.4),
                    arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))

    # convergence
    cx, cy = 6.5, 1.3
    ax.add_patch(FancyBboxPatch((cx - 2.2, cy - 0.5), 4.4, 1.0,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=2.5))
    ax.text(cx, cy, '命中 → owner = 张三 (zhangsan@corp.com)', fontsize=12, fontweight='bold',
            color=GREEN, ha='center', va='center')

    # three converging arrows
    for px in [2.5, 6.5, 10.5]:
        ax.annotate('', xy=(6.5, 1.8), xytext=(px, 2.5),
                    arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4,
                                    connectionstyle='arc3,rad=0'))

    ax.text(6.5, 0.35, '兜底策略：三条都没命中 → 标记"未归属"，推送给 PMO 人工分配',
            fontsize=9.5, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'owner_lookup.png')


# ── 4：四平台 API 对比卡 ──────────────────────────────────────────────────
def draw_platforms():
    fig, ax = plt.subplots(figsize=(13, 7), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis('off')

    ax.text(6.5, 6.55, '四个项目管理平台：MCP 桥接对比', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.05, 'Hermes 通过 MCP 连接，每个平台暴露 create_issue / update_issue 两个核心工具',
            fontsize=11.5, color=DIM, ha='center')

    platforms = [
        ('Jira', 'Postman 生态\nrest/api/3/issue\nBearer Token', RED,
         'atlassian-python-api\n已验证 MCP Server'),
        ('禅道 Zentao', 'HTTP API v1\nPOST /tasks\nToken Auth', ORANGE,
         '官方 REST API\n轻量自建 MCP'),
        ('PingCode', 'Open API v1\nPOST /v1/project/work_items\nOAuth2', BLUE,
         'Skill 社区已有\nlobehub pingcode'),
        ('阿里云效 Yunxiao', 'Open API\nCreateWorkitem\nRAM AK/SK', CYAN,
         '阿里云官方 SDK\nRAM 角色授权'),
    ]

    w = 2.8; gap = 0.17
    total_w = w * 4 + gap * 3
    x_start = (13 - total_w) / 2
    y_bottom = 1.15

    for i, (name, desc, color, extra) in enumerate(platforms):
        x = x_start + i * (w + gap)
        # header
        ax.add_patch(FancyBboxPatch((x, 4.5), w, 0.7,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2, 4.85, name, fontsize=14, fontweight='bold',
                color=BG, ha='center', va='center')
        # body
        ax.add_patch(FancyBboxPatch((x, y_bottom), w, 3.25,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(x + w / 2, 3.75, desc, fontsize=9, color=TEXT,
                ha='center', va='center', linespacing=1.5)
        # extra tag
        ax.add_patch(FancyBboxPatch((x + 0.15, y_bottom + 0.15), w - 0.3, 0.65,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=BG, edgecolor=DIM, linewidth=1))
        ax.text(x + w / 2, y_bottom + 0.475, extra, fontsize=7.8, color=DIM,
                ha='center', va='center', linespacing=1.3)

    ax.text(6.5, 0.5, 'MCP Server 统一暴露工具签名',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')
    ax.add_patch(FancyBboxPatch((4.0, 0.2), 5.0, 0.45,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=BG, edgecolor=GREEN, linewidth=1))
    ax.text(6.5, 0.425,
            'create_issue(title, description, owner, platform)',
            fontsize=9, color=GREEN, ha='center', va='center', fontfamily='monospace')

    save(fig, 'platforms.png')


if __name__ == '__main__':
    draw_pipeline(); draw_intent(); draw_owner(); draw_platforms()
    print('done')
