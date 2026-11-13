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

BG = '#1a1410'
PANEL = '#262d17'
PANEL = '#261d17'
CARD = '#332720'
TEXT = '#f2e9e1'
DIM = '#8d7a6b'
ORANGE = '#f97316'
AMBER = '#fbbf24'
TEAL = '#2dd4bf'
BLUE = '#60a5fa'
PINK = '#f472b6'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：六过程 ITTO ─────────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.85, '范围管理六个过程，一条流水线', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.42, '每个过程的输出，就是下一个过程的输入 —— 断一环就全断', fontsize=11.8,
            color=DIM, ha='center')

    procs = [
        ('01', '规划范围管理', '章程 · 计划 · OPA', '专家判断 · 会议',
         '范围管理计划\n需求管理计划', TEAL),
        ('02', '收集需求', '干系人登记册\n商业论证', '访谈 · 原型 · 问卷',
         '需求文件\n需求跟踪矩阵', BLUE),
        ('03', '定义范围', '需求文件 · 章程', '产品分析\n备选方案生成',
         '项目范围\n说明书', AMBER),
        ('04', '创建 WBS', '范围说明书\n需求文件', '分解',
         '范围基准\nWBS 词典', ORANGE),
        ('05', '确认范围', '可交付成果\n质量报告', '检查 · 投票',
         '验收成果\n变更请求', PINK),
        ('06', '控制范围', '绩效数据 · RTM', '偏差分析\n趋势分析',
         '变更请求\n计划更新', TEAL),
    ]

    cw = 1.97; gap = 0.14
    total = cw * 6 + gap * 5
    x0 = (13 - total) / 2

    for i, (num, name, inp, tech, out, color) in enumerate(procs):
        x = x0 + i * (cw + gap)
        # 头部
        ax.add_patch(FancyBboxPatch((x, 5.42), cw, 0.78,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + cw / 2, 5.98, num, fontsize=7.6, color=BG, ha='center', va='center')
        ax.text(x + cw / 2, 5.68, name, fontsize=9.2, fontweight='bold', color=BG,
                ha='center', va='center')
        # 三行
        rows = [
            ('输入', inp, 1.30, TEXT),
            ('技术', tech, 1.30, TEXT),
            ('输出', out, 1.62, color),
        ]
        y = 5.18
        for label, content, h, c in rows:
            ax.add_patch(FancyBboxPatch((x, y - h), cw, h,
                                        boxstyle='round,pad=0.02,rounding_size=0.06',
                                        facecolor=PANEL, edgecolor='#3c2f26', linewidth=1))
            ax.text(x + 0.12, y - 0.24, label, fontsize=7.0, color=DIM,
                    ha='left', va='center')
            ax.text(x + cw / 2, y - h + (h - 0.28) / 2 + 0.05, content,
                    fontsize=7.6, color=c, ha='center', va='center', linespacing=1.55)
            y -= h + 0.08

        if i < 5:
            ax.annotate('', xy=(x + cw + gap - 0.005, 4.55), xytext=(x + cw + 0.005, 4.55),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.1))

    ax.text(6.5, 0.40, '图上只列了主输入 —— 完整 ITTO 里还有事业环境因素和组织过程资产，那是 AI 最该介入的地方',
            fontsize=8.8, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'pipeline.png')


# ── 2：六份文档模板 ─────────────────────────────────────────────────────────
def draw_templates():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.22, '六份文档，六套字段', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.80, '字段固定，AI 才能填；空着的字段就是要去追问的地方', fontsize=11.8,
            color=DIM, ha='center')

    docs = [
        ('范围管理计划', 'scope-plan', TEAL, [
            '范围定义方法',
            '验收标准与流程',
            '变更审批链路',
            'WBS 分解层级',
        ]),
        ('需求文件', 'requirements', BLUE, [
            'REQ-ID / 标题',
            '来源干系人',
            '优先级 + 理由',
            '验收条件（可测）',
        ]),
        ('需求跟踪矩阵', 'rtm', AMBER, [
            'REQ-ID → 业务目标',
            '→ 设计 / 代码提交',
            '→ 测试用例',
            '→ 验收状态',
        ]),
        ('项目范围说明书', 'scope-statement', ORANGE, [
            '项目目标与成功标准',
            '可交付成果清单',
            '除外责任（不做什么）',
            '假设条件 / 约束',
        ]),
        ('WBS 与词典', 'baseline', PINK, [
            'WBS 编码（1.2.3）',
            '工作包负责人',
            '工期 / 成本估算',
            '验收标准',
        ]),
        ('验收单与变更单', 'acceptance-change', TEAL, [
            '交付物 + 验收结论',
            '偏差说明',
            '变更影响（范围/进度/成本）',
            '签字人与时间',
        ]),
    ]

    w = 3.95; h = 2.4
    xs = [0.35, 4.52, 8.69]
    ys = [3.85, 1.05]

    for i, (name, slug, color, fields) in enumerate(docs):
        x = xs[i % 3]; y = ys[i // 3]
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.6))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.55), w, 0.55,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.2, y + h - 0.27, name, fontsize=10, fontweight='bold',
                color=BG, ha='left', va='center')
        ax.text(x + w - 0.2, y + h - 0.27, slug, fontsize=6.6, color=BG,
                ha='right', va='center')

        fy = y + h - 0.92
        for f in fields:
            ax.add_patch(plt.Circle((x + 0.3, fy + 0.02), 0.055,
                                    facecolor=color, edgecolor='none', zorder=4))
            ax.text(x + 0.48, fy, f, fontsize=7.8, color=TEXT, ha='left', va='center')
            fy -= 0.36

    save(fig, 'templates.png')


# ── 3：OPA 归档 ─────────────────────────────────────────────────────────────
def draw_opa():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.05, '文档不进共享盘，进知识库', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.62, '共享盘里的文档是死的，知识库里的文档会被下一次检索调用', fontsize=11.8,
            color=DIM, ha='center')

    # 左：元数据
    ax.add_patch(FancyBboxPatch((0.5, 0.85), 6.7, 5.35,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor='#120d0a', edgecolor=TEAL, linewidth=1.6))
    ax.text(0.8, 5.9, '入库前先加一层 front-matter', fontsize=10, fontweight='bold',
            color=TEAL, ha='left', va='center')

    yaml_lines = [
        ('---', DIM),
        ('doc_id: pay-platform/scope-statement/v3', TEXT),
        ('doc_type: scope_statement', TEAL),
        ('project: pay-platform', TEXT),
        ('version: 3', TEXT),
        ('status: baselined', AMBER),
        ('baseline_at: 2026-11-06', TEXT),
        ('owner: zhangming', TEXT),
        ('stakeholders: [pay, finance, risk]', TEXT),
        ('related: [REQ-012, REQ-018]', TEXT),
        ('supersedes: v2', TEXT),
        ('---', DIM),
    ]
    ly = 5.5
    for txt, color in yaml_lines:
        ax.text(0.8, ly, txt, fontsize=7.6, color=color, ha='left', va='center',
                fontfamily='monospace')
        ly -= 0.345

    ax.text(0.8, 1.32, '状态只有三种：draft → baselined → superseded', fontsize=8,
            color=DIM, ha='left', va='center')
    ax.text(0.8, 1.02, '基线之后任何改动，都必须走变更单，不能直接改文档', fontsize=8,
            color=PINK, ha='left', va='center')

    # 右：四类复用
    ax.add_patch(FancyBboxPatch((7.4, 0.85), 5.1, 5.35,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ORANGE, linewidth=1.6))
    ax.text(7.7, 5.9, '四类复用场景', fontsize=10, fontweight='bold', color=ORANGE,
            ha='left', va='center')

    uses = [
        ('新项目立项', '找相似范围的历史项目\n直接复用可交付成果清单', TEAL),
        ('需求评审', '查同类需求的验收条件\n和历史上的反例', BLUE),
        ('变更评估', '看以往同类变更的\n实际影响工时', AMBER),
        ('季度复盘', '统计各项目范围蔓延率\n定位根因', PINK),
    ]
    uy = 5.28
    for name, desc, color in uses:
        ax.add_patch(FancyBboxPatch((7.7, uy - 0.85), 4.5, 0.86,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=color, linewidth=1))
        ax.text(7.9, uy - 0.14, name, fontsize=8.8, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(7.9, uy - 0.52, desc, fontsize=7.4, color=TEXT, ha='left', va='center',
                linespacing=1.5)
        uy -= 1.1

    ax.text(6.5, 0.35, '组织过程资产的价值，不在于存了多少，在于被检索到多少次', fontsize=8.8,
            color=DIM, ha='center', va='center', style='italic')

    save(fig, 'opa.png')


# ── 4：群消息四种格式 ───────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.42, '四种消息，四种语气', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 7.0, '同一件事发给不同人，格式不一样 —— 但都只有三段', fontsize=11.8,
            color=DIM, ha='center')

    msgs = [
        ('范围预警', '每天 09:00 · 有异常才发', ORANGE, [
            '⚠ 检测到 3 个未走变更的需求',
            '· REQ-041 导出增加水印（+2 人日）',
            '· REQ-044 支持多币种（+5 人日）',
            '请 @张明 今日内确认是否纳入本期',
        ]),
        ('变更审批', '变更单创建时', PINK, [
            '范围变更 #CR-017 待审批',
            '变更内容：对账报表增加 4 个维度',
            '影响：进度 +3 天 · 成本 +2.5 人日',
            '截止 11-08 18:00，超时自动挂起',
        ]),
        ('验收通过', '验收单签署后', TEAL, [
            'PAY-3412 分账功能已验收',
            '验收方式：48 用例全通过 + 财务抽检',
            '偏差：无',
            '验收人：李静 · 已归档至知识库 v2',
        ]),
        ('范围健康度', '每周五 17:30', BLUE, [
            '本周范围健康度：78 分（上周 85）',
            '蔓延率 12% · 镀金项 2 个 · 变更 3 次',
            '根因：需求评审时未确认导出格式',
            '下周动作：评审模板新增「格式确认」项',
        ]),
    ]

    w = 5.95; h = 2.52
    xs = [0.4, 6.65]
    ys = [4.1, 1.3]

    for i, (name, when, color, lines) in enumerate(msgs):
        x = xs[i % 2]; y = ys[i // 2]
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.6))
        # 标签
        ax.add_patch(FancyBboxPatch((x + 0.2, y + h - 0.62), 1.35, 0.38,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.875, y + h - 0.43, name, fontsize=8.2, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(x + 1.7, y + h - 0.43, when, fontsize=7.4, color=DIM,
                ha='left', va='center')

        ly = y + h - 0.95
        for j, ln in enumerate(lines):
            ax.text(x + 0.25, ly, ln, fontsize=7.8, color=TEXT if j else color,
                    ha='left', va='center', fontweight='bold' if j == 0 else 'normal')
            ly -= 0.38

    ax.text(6.5, 0.55, '三类是事件驱动，一类是定时汇总 —— 事件要快，汇总要准',
            fontsize=9, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_templates()
    draw_opa()
    draw_message()
    print('✓ 全部生成完毕')
