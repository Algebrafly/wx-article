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

BG = '#14111f'
PANEL = '#1e1930'
CARD = '#2a2342'
TEXT = '#ece9f5'
DIM = '#7b7492'
INDIGO = '#818cf8'
CYAN = '#22d3ee'
AMBER = '#fbbf24'
ROSE = '#f472b6'
GREEN = '#4ade80'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：三层架构 ─────────────────────────────────────────────────────────────
def draw_framework():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.0, '一个项目经理，拆成三层来配', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.55, '人设定判断，技能定动作，Profile 定权限', fontsize=12, color=DIM, ha='center')

    # 第一层：Profile
    ax.add_patch(FancyBboxPatch((1.0, 4.95), 11.0, 1.0,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=INDIGO, linewidth=1.8))
    ax.text(1.35, 5.66, 'Profile · ai-pm', fontsize=11.5, fontweight='bold',
            color=INDIGO, ha='left', va='center')
    ax.text(1.35, 5.28, '挂哪些模型 · 接哪些 MCP · 能碰哪些项目 · 能发到哪些群',
            fontsize=8.6, color=TEXT, ha='left', va='center')
    ax.text(11.65, 5.45, '边界', fontsize=9, color=DIM, ha='right', va='center')

    # 第二层：SOUL
    ax.add_patch(FancyBboxPatch((1.0, 3.55), 5.4, 1.1,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ROSE, linewidth=1.8))
    ax.text(1.32, 4.33, 'SOUL.md · 人设', fontsize=10.8, fontweight='bold',
            color=ROSE, ha='left', va='center')
    ax.text(1.32, 3.93, '怎么判断优先级 · 什么时候该报警\n什么话不能说', fontsize=8.2,
            color=TEXT, ha='left', va='center', linespacing=1.5)

    # 第三层：Skill
    ax.add_patch(FancyBboxPatch((6.6, 3.55), 5.4, 1.1,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=CYAN, linewidth=1.8))
    ax.text(6.92, 4.33, 'Skill · project-manager', fontsize=10.8, fontweight='bold',
            color=CYAN, ha='left', va='center')
    ax.text(6.92, 3.93, '拉哪张表 · 算什么指标 · 用什么模板\n输出成什么格式', fontsize=8.2,
            color=TEXT, ha='left', va='center', linespacing=1.5)

    # 箭头 down
    ax.annotate('', xy=(6.5, 3.35), xytext=(6.5, 4.85),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))

    # 十领域条
    ax.add_patch(FancyBboxPatch((0.8, 2.55), 11.4, 0.62,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=AMBER, linewidth=1.4))
    domains = ['整合', '范围', '进度', '成本', '质量', '资源', '沟通', '风险', '采购', '干系人']
    dx = 1.35
    for d in domains:
        ax.text(dx, 2.86, d, fontsize=8.2, color=AMBER, ha='center', va='center')
        dx += 1.115
    ax.text(0.95, 2.24, '十大管理领域 · 同一套人设和技能，换查询和模板', fontsize=7.8,
            color=DIM, ha='left', va='center')

    # 输出
    ax.annotate('', xy=(6.5, 1.85), xytext=(6.5, 2.48),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))

    outs = [
        (1.0, '企微项目群', '标准 markdown 卡片', GREEN),
        (4.55, '飞书项目群', '富文本 + 待办', CYAN),
        (8.1, '平台留痕', '写回禅道 / Jira', AMBER),
    ]
    for x, name, note, color in outs:
        ax.add_patch(FancyBboxPatch((x, 0.95), 3.2, 0.82,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(x + 1.6, 1.5, name, fontsize=9.5, fontweight='bold', color=color,
                ha='center', va='center')
        ax.text(x + 1.6, 1.16, note, fontsize=7.6, color=DIM, ha='center', va='center')

    ax.text(6.5, 0.42, '人设决定「怎么想」，技能决定「怎么做」，Profile 决定「能不能做」',
            fontsize=9.2, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'framework.png')


# ── 2：十大领域矩阵 ─────────────────────────────────────────────────────────
def draw_domains():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.22, '十大领域，各自回答一个问题', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.80, '不是十个模块，是十个提问角度 —— 数据源高度重合', fontsize=11.8,
            color=DIM, ha='center')

    items = [
        ('01', '整合管理', '这周该先推哪件事', '全平台', INDIGO),
        ('02', '范围管理', '哪些在范围内，哪些是镀金', '需求单 · PRD', CYAN),
        ('03', '进度管理', '关键路径有没有被拖', '任务 · 甘特', AMBER),
        ('04', '成本管理', '预算烧到哪一步了', '工时 · 采购单', ROSE),
        ('05', '质量管理', '缺陷密度和返工率在恶化吗', '缺陷 · 测试报告', GREEN),
        ('06', '资源管理', '谁满负荷，谁在空转', '工时 · 排期', INDIGO),
        ('07', '沟通管理', '该通知的人通知到了吗', '群消息 · 会议', CYAN),
        ('08', '风险管理', '哪三个风险最可能爆', '风险台账 · 告警', AMBER),
        ('09', '采购管理', '合同和验收节点是否对齐', '合同 · 付款节点', ROSE),
        ('10', '干系人管理', '谁的支持在减弱', '会议 · 反馈 · 变更', GREEN),
    ]

    w = 5.9; h = 0.98
    xs = [0.55, 6.55]
    y = 5.72
    for i, (num, name, q, src, color) in enumerate(items):
        x = xs[i % 2]
        if i % 2 == 0 and i > 0:
            y -= h + 0.2
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor='#332b4d', linewidth=1))
        # 左侧色条
        ax.add_patch(FancyBboxPatch((x, y), 0.09, h,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.28, y + h - 0.28, num, fontsize=10, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + 0.72, y + h - 0.28, name, fontsize=10.2, fontweight='bold',
                color=TEXT, ha='left', va='center')
        ax.text(x + 0.72, y + 0.3, q, fontsize=8.4, color=color,
                ha='left', va='center')
        ax.text(x + w - 0.18, y + h - 0.28, src, fontsize=7.0, color=DIM,
                ha='right', va='center')

    ax.text(6.5, 0.3, '十个领域共用一份数据底座 —— 差别只在「问什么」和「怎么讲」',
            fontsize=9.2, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'domains.png')


# ── 3：群消息格式 ───────────────────────────────────────────────────────────
def draw_output():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.35, '群里发的不是报表，是结论', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.9, '三段式：一句判断、三条事实、一个请求', fontsize=12, color=DIM, ha='center')

    # 消息卡
    ax.add_patch(FancyBboxPatch((0.7, 0.75), 8.3, 5.85,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=CYAN, linewidth=1.8))
    # 头部
    ax.add_patch(FancyBboxPatch((0.95, 5.92), 7.8, 0.5,
                                boxstyle='round,pad=0.02,rounding_size=0.06',
                                facecolor=CARD, edgecolor='#332b4d', linewidth=1))
    ax.text(1.15, 6.17, '支付中台项目 · 第 12 周周报', fontsize=9.6, fontweight='bold',
            color=TEXT, ha='left', va='center')
    ax.text(8.5, 6.17, '每周一 09:00', fontsize=7.4, color=DIM, ha='right', va='center')

    # 第一段：判断
    ax.text(0.95, 5.55, '结论', fontsize=8.6, fontweight='bold', color=AMBER, ha='left')
    ax.text(0.95, 5.15, '进度可控，但成本超支 8%，主因是退款模块两次返工',
            fontsize=9.2, color=TEXT, ha='left', va='center')

    # 第二段：三条事实
    ax.text(0.95, 4.72, '三条事实', fontsize=8.6, fontweight='bold', color=CYAN, ha='left')
    facts = [
        ('进度', '关键路径剩余 6 天，浮动 2 天', GREEN),
        ('成本', '已用 108 人日 / 预算 100 人日', ROSE),
        ('范围', '本周新增 3 个需求，2 个已挂起', AMBER),
    ]
    fy = 4.34
    for label, text, color in facts:
        ax.add_patch(FancyBboxPatch((0.95, fy - 0.13), 0.62, 0.3,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.26, fy + 0.02, label, fontsize=7.2, fontweight='bold', color=BG,
                ha='center', va='center')
        ax.text(1.72, fy + 0.02, text, fontsize=8.4, color=TEXT, ha='left', va='center')
        fy -= 0.46

    # 第三段：请求
    ax.text(0.95, 2.68, '需要拍板', fontsize=8.6, fontweight='bold', color=ROSE, ha='left')
    asks = ['退款模块是否砍掉第二期，换回 6 人日',
            '下周三前端资源能否从 A 项目借 1 人',
            '客户验收时间是否可后延一周']
    ay = 2.3
    for i, a in enumerate(asks):
        ax.text(1.0, ay, f'{i + 1}.', fontsize=8.2, color=ROSE, ha='left', va='center')
        ax.text(1.32, ay, a, fontsize=8.3, color=TEXT, ha='left', va='center')
        ay -= 0.36

    # 底部链接
    ax.add_patch(FancyBboxPatch((0.95, 1.0), 2.3, 0.4,
                                boxstyle='round,pad=0.02,rounding_size=0.06',
                                facecolor=INDIGO, edgecolor=INDIGO, linewidth=0))
    ax.text(2.1, 1.2, '完整周报', fontsize=7.6, fontweight='bold', color=BG,
            ha='center', va='center')
    ax.add_patch(FancyBboxPatch((3.4, 1.0), 2.3, 0.4,
                                boxstyle='round,pad=0.02,rounding_size=0.06',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(4.55, 1.2, '风险台账', fontsize=7.6, color=TEXT, ha='center', va='center')
    ax.add_patch(FancyBboxPatch((5.85, 1.0), 2.3, 0.4,
                                boxstyle='round,pad=0.02,rounding_size=0.06',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(7.0, 1.2, '@项目经理', fontsize=7.6, color=TEXT, ha='center', va='center')

    # 右侧：格式规则
    ax.add_patch(FancyBboxPatch((9.25, 0.75), 3.15, 5.85,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=AMBER, linewidth=1.8))
    ax.text(9.5, 6.32, '四条格式铁律', fontsize=9.6, fontweight='bold', color=AMBER,
            ha='left', va='center')

    rules = [
        ('一句话结论', '不超过 40 字'),
        ('数字带口径', '「108 人日」不是「很多」'),
        ('风险带动作', '「需要借 1 人」不是「有风险」'),
        ('全文 < 1500 字', '超出就放链接'),
    ]
    ry = 5.85
    for i, (name, note) in enumerate(rules):
        ax.text(9.5, ry, f'0{i + 1}', fontsize=8, fontweight='bold', color=AMBER,
                ha='left', va='center')
        ax.text(9.85, ry + 0.02, name, fontsize=8.2, fontweight='bold', color=TEXT,
                ha='left', va='center')
        ax.text(9.85, ry - 0.3, note, fontsize=7.2, color=DIM, ha='left', va='center')
        ry -= 0.98

    ax.text(10.82, 1.25, '企微上限 4096 字节\n超了会被截断',
            fontsize=7.2, color=DIM, ha='center', va='center', linespacing=1.6)

    save(fig, 'output.png')


# ── 4：配置树 + SOUL 片段 ───────────────────────────────────────────────────
def draw_config():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.0, '配置就四个文件', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.55, '没有隐藏魔法 —— 全部可版本化、可 review', fontsize=12,
            color=DIM, ha='center')

    # 左：文件树
    ax.add_patch(FancyBboxPatch((0.55, 0.75), 5.7, 5.5,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=CYAN, linewidth=1.6))
    ax.text(0.85, 5.85, '~/.hermes/', fontsize=9.5, fontweight='bold', color=CYAN,
            ha='left', va='center')

    tree = [
        ('profiles/', DIM, 5.45),
        ('└─ ai-pm.yaml', INDIGO, 5.1),
        ('&nbsp;&nbsp;&nbsp;model · mcp · projects · groups', DIM, 4.78),
        ('souls/', DIM, 4.35),
        ('└─ pm.SOUL.md', ROSE, 4.0),
        ('&nbsp;&nbsp;&nbsp;判断标准 · 语气 · 禁忌', DIM, 3.68),
        ('skills/', DIM, 3.25),
        ('└─ project-manager/', CYAN, 2.9),
        ('&nbsp;&nbsp;&nbsp;SKILL.md + 十个领域的查询模板', DIM, 2.58),
        ('cron/', DIM, 2.15),
        ('└─ jobs.json', GREEN, 1.8),
        ('&nbsp;&nbsp;&nbsp;周报 / 日报 / 风险巡检', DIM, 1.48),
        ('.env', DIM, 1.05),
    ]
    for txt, color, y in tree:
        ax.text(0.85, y, txt.replace('&nbsp;', ' '), fontsize=8.4, color=color,
                ha='left', va='center')

    # 右：SOUL 片段
    ax.add_patch(FancyBboxPatch((6.6, 0.75), 5.8, 5.5,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor='#0f0c18', edgecolor=ROSE, linewidth=1.6))
    ax.text(6.9, 5.85, 'pm.SOUL.md（节选）', fontsize=9.5, fontweight='bold',
            color=ROSE, ha='left', va='center')

    lines = [
        ('你是这个项目的项目经理，不是助理。', TEXT),
        ('', TEXT),
        ('## 判断优先级', ROSE),
        ('1. 影响交付日期的 > 影响体验的', TEXT),
        ('2. 影响多人的 > 影响单人的', TEXT),
        ('3. 已承诺的 > 想做的', TEXT),
        ('', TEXT),
        ('## 说话方式', ROSE),
        ('- 先给结论，再给依据', TEXT),
        ('- 数字必须带口径和时间', TEXT),
        ('- 不说「建议关注」，说「建议做什么」', TEXT),
        ('', TEXT),
        ('## 禁止', ROSE),
        ('- 不替客户做范围承诺', TEXT),
        ('- 不在群里点名批评个人', TEXT),
        ('- 不确定的事标「待确认」，不猜', TEXT),
    ]
    ly = 5.48
    for txt, color in lines:
        ax.text(6.9, ly, txt, fontsize=7.8, color=color, ha='left', va='center')
        ly -= 0.298

    save(fig, 'config.png')


if __name__ == '__main__':
    draw_framework()
    draw_domains()
    draw_output()
    draw_config()
    print('✓ 全部生成完毕')
