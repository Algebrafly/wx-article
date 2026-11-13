#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""整合管理推文配图生成"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0d1117'
PANEL = '#161b22'
CARD = '#1c2430'
LINE = '#2d3846'
CYAN = '#22d3ee'
BLUE = '#60a5fa'
VIOLET = '#a78bfa'
AMBER = '#fbbf24'
GREEN = '#4ade80'
ROSE = '#fb7185'
TEXT = '#e6edf3'
DIM = '#8b98a8'

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(OUT, exist_ok=True)


def canvas(w=13, h=6.6):
    fig = plt.figure(figsize=(w, h), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 13)
    ax.set_ylim(0, h)
    ax.axis('off')
    ax.set_facecolor(BG)
    return fig, ax


def card(ax, x, y, w, h, ec, fc=CARD, lw=1.3, r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f'round,pad=0.04,rounding_size={r}',
                                facecolor=fc, edgecolor=ec, linewidth=lw))


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.12)
    plt.close(fig)
    print(f'✓ {name}')


def head(ax, h, title, sub, ty=None, sy=None):
    ty = h - 0.55 if ty is None else ty
    sy = h - 0.95 if sy is None else sy
    ax.text(6.5, ty, title, fontsize=17.5, fontweight='bold', color=TEXT,
            ha='center', va='center')
    ax.text(6.5, sy, sub, fontsize=11, color=DIM, ha='center', va='center')


# ── 1：七个过程 ────────────────────────────────────────────────────────
def fig_pipeline():
    fig, ax = canvas(13, 7.2)
    head(ax, 7.2, '整合管理有七个过程，是十大领域里最多的',
         '其他领域各管一段，整合管理管的是接缝', ty=6.70, sy=6.34)

    row1 = [
        ('01', '制定项目章程', '授权', CYAN,
         '商业文件 · 协议', '专家判断 · 会议', '项目章程'),
        ('02', '制定管理计划', '定基线', BLUE,
         '章程 · 各领域计划', '专家判断 · 引导', '项目管理计划'),
        ('03', '指导与管理执行', '做事', VIOLET,
         '计划 · 变更请求', '项目管理信息系统', '可交付成果'),
        ('04', '管理项目知识', '沉淀', GREEN,
         '可交付成果 · 计划', '知识管理 · 信息管理', '经验教训登记册'),
    ]
    row2 = [
        ('05', '监控项目工作', '看偏差', AMBER,
         '计划 · 工作绩效数据', '数据分析 · 趋势分析', '工作绩效报告'),
        ('06', '实施整体变更控制', '管变更', ROSE,
         '变更请求 · 绩效报告', '专家判断 · CCB', '批准的变更'),
        ('07', '结束项目或阶段', '收口', CYAN,
         '验收成果 · 计划', '验收 · 复盘 · 归档', '最终报告与移交'),
    ]

    def draw_row(items, y0, ch, cw, gap, fs):
        x0 = (13 - (len(items) * cw + (len(items) - 1) * gap)) / 2
        for i, (num, name, verb, c, ins, techs, outs) in enumerate(items):
            x = x0 + i * (cw + gap)
            card(ax, x, y0, cw, ch, c + '55')
            ax.add_patch(FancyBboxPatch((x, y0 + ch - 0.34), cw, 0.34,
                                        boxstyle='round,pad=0.04,rounding_size=0.12',
                                        facecolor=c, edgecolor='none'))
            ax.text(x + 0.18, y0 + ch - 0.17, num, fontsize=fs + 0.3,
                    fontweight='bold', color='#0d1117', ha='left', va='center')
            ax.text(x + 0.58, y0 + ch - 0.17, name, fontsize=fs,
                    fontweight='bold', color='#0d1117', ha='left', va='center')
            ax.text(x + cw - 0.16, y0 + ch - 0.17, verb, fontsize=fs - 0.4,
                    color='#0d1117', ha='right', va='center', alpha=0.65)

            blocks = [('输入', ins, CYAN, y0 + ch - 0.62),
                      ('技术', techs, VIOLET, y0 + ch - 1.04),
                      ('输出', outs, AMBER, y0 + ch - 1.46)]
            for label, txt, lc, ly in blocks:
                ax.text(x + 0.18, ly, label, fontsize=fs - 0.3,
                        fontweight='bold', color=lc, ha='left', va='center')
                ax.text(x + 0.18, ly - 0.21, txt, fontsize=fs - 0.4,
                        color='#b9c6d4', ha='left', va='center')

    draw_row(row1, 3.60, 2.10, 3.02, 0.20, 7.0)
    draw_row(row2, 1.18, 2.10, 4.06, 0.32, 7.6)

    ax.text(6.5, 5.98, '执行流：章程授权 → 计划定基线 → 执行产出 → 沉淀知识 → 监控偏差 → 变更纠偏 → 收口归档',
            fontsize=8.2, color=CYAN, ha='center', va='center')
    ax.text(6.5, 0.60, '七个过程不是七个阶段：从章程签发到项目关账，它们每天都在同时运转',
            fontsize=8.2, color=DIM, ha='center', va='center')
    save(fig, 'pipeline.png')


# ── 2：冲突裁决表 ───────────────────────────────────────────────────────
def fig_conflict():
    fig, ax = canvas(13, 6.8)
    head(ax, 6.8, '十个领域的数据同时说话时，规则必须在事前定好',
         '事后吵架的本质，是事前没写「谁优先」')

    x0, ytop = 0.55, 5.35
    widths = [3.85, 3.75, 4.35]
    hx = x0
    cols = ['冲突场景', '裁决结果', '依据']
    for c, w in zip(cols, widths):
        ax.add_patch(FancyBboxPatch((hx, ytop - 0.52), w, 0.52,
                                    boxstyle='round,pad=0.03,rounding_size=0.06',
                                    facecolor='#1f2937', edgecolor='#334155', linewidth=1))
        ax.text(hx + 0.18, ytop - 0.26, c, fontsize=8.2, fontweight='bold',
                color=CYAN, ha='left', va='center')
        hx += w

    rows = [
        ('范围要加 vs 进度已承诺', '走变更，进度重排', '范围基线是合同依据', ROSE),
        ('质量要保 vs 成本要砍', '保质量，砍范围', '外部失败成本最贵', AMBER),
        ('两项目争同一人', '按组合优先级，不排队抢', '组合层决策，项目层执行', VIOLET),
        ('风险应对 vs 预算不足', '动应急储备，不动基准', '基准内项目经理可批', GREEN),
        ('干系人期望 vs 基线', '基线不动，另立变更', '口头承诺不构成基线', BLUE),
    ]

    y = ytop - 0.52
    for i, (a, b, c, col) in enumerate(rows):
        h = 0.74
        ax.add_patch(FancyBboxPatch((x0, y - h), sum(widths), h,
                                    boxstyle='round,pad=0.02,rounding_size=0.05',
                                    facecolor=CARD if i % 2 == 0 else PANEL,
                                    edgecolor=LINE, linewidth=0.8))
        ax.plot([x0 + widths[0], x0 + widths[0]], [y - h, y], color=LINE, lw=0.8)
        ax.plot([x0 + widths[0] + widths[1], x0 + widths[0] + widths[1]],
                [y - h, y], color=LINE, lw=0.8)
        ax.text(x0 + 0.18, y - h / 2, a, fontsize=7.8, color='#d5dee8',
                ha='left', va='center')
        ax.text(x0 + widths[0] + 0.18, y - h / 2, b, fontsize=7.8,
                color=col, fontweight='bold', ha='left', va='center')
        ax.text(x0 + widths[0] + widths[1] + 0.18, y - h / 2, c, fontsize=7.6,
                color=DIM, ha='left', va='center')
        y -= h + 0.045

    ax.text(6.5, 0.45, '优先级：法规与合同 > 已批准基线 > 项目管理计划 > 会议结论 > 口头承诺',
            fontsize=8.6, color=AMBER, ha='center', va='center')
    save(fig, 'conflict.png')


# ── 3：变更控制 ────────────────────────────────────────────────────────
def fig_change():
    fig, ax = canvas(13, 6.6)
    head(ax, 6.6, '变更是唯一能合法打破基线的通道',
         '拦死和全放行，是两种同样严重的失控')

    steps = [('提出', '写清动因', CYAN), ('评估影响', '范围/进度/成本/质量', BLUE),
             ('分级', '按阈值定审批层', VIOLET), ('决策', 'CCB 或项目经理', AMBER),
             ('实施验证', '改基线并回写', GREEN)]
    n = len(steps)
    cw, gap = 2.10, 0.44
    x0 = (13 - (n * cw + (n - 1) * gap)) / 2
    yb, ch = 4.05, 1.05
    for i, (name, note, c) in enumerate(steps):
        x = x0 + i * (cw + gap)
        card(ax, x, yb, cw, ch, c + '66')
        ax.text(x + cw / 2, yb + ch - 0.32, name, fontsize=8.8, fontweight='bold',
                color=c, ha='center', va='center')
        ax.text(x + cw / 2, yb + 0.34, note, fontsize=6.8, color='#a8b6c6',
                ha='center', va='center')
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + cw + 0.06, yb + ch / 2),
                                         (x + cw + gap - 0.06, yb + ch / 2),
                                         arrowstyle='-|>', mutation_scale=13,
                                         color='#4b5a6b', lw=1.5))

    tiers = [
        ('L1 项目内', '≤ 5 人日 且 不影响里程碑', '项目经理批准', GREEN),
        ('L2 项目级', '≤ 20 人日 或 影响里程碑', 'CCB 集体决策', AMBER),
        ('L3 组合级', '> 20 人日 或 动合同与预算基准', '发起人 + PMO', ROSE),
    ]
    cw2, gap2 = 3.95, 0.30
    x2 = (13 - (3 * cw2 + 2 * gap2)) / 2
    for i, (lv, cond, who, c) in enumerate(tiers):
        x = x2 + i * (cw2 + gap2)
        card(ax, x, 1.05, cw2, 2.28, c + '66')
        ax.add_patch(FancyBboxPatch((x, 2.90), cw2, 0.43,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=c, edgecolor='none'))
        ax.text(x + 0.20, 3.115, lv, fontsize=8.0, fontweight='bold',
                color='#0d1117', ha='left', va='center')
        ax.text(x + 0.20, 2.42, '触发条件', fontsize=6.8, color=CYAN,
                ha='left', va='center')
        ax.text(x + 0.20, 2.12, cond, fontsize=7.2, color='#c2cfdc',
                ha='left', va='center')
        ax.text(x + 0.20, 1.72, '审批人', fontsize=6.8, color=AMBER,
                ha='left', va='center')
        ax.text(x + 0.20, 1.42, who, fontsize=7.6, color=c, fontweight='bold',
                ha='left', va='center')
        ax.text(x + 0.20, 1.15, '阈值由组织定，不由项目定', fontsize=6.3,
                color='#5f6d7e', ha='left', va='center')

    ax.text(6.5, 0.55, '被驳回的变更也要入库：否则同一个变更会被提第二次、第三次',
            fontsize=8.2, color=DIM, ha='center', va='center')
    save(fig, 'change.png')


# ── 4：知识沉淀与收尾 ──────────────────────────────────────────────────
def fig_close():
    fig, ax = canvas(13, 6.8)
    head(ax, 6.8, '收尾不是结束，是把项目变成组织的记忆',
         '经验教训登记册最常见的结局，是躺在某个共享盘里没人打开')

    colsdata = [
        ('验收与移交', CYAN, [
            '逐条对照验收标准',
            '遗留问题必须带责任人与日期',
            '文档、账号、监控全部移交',
            '移交单需接收方签字',
            '运维手册可独立执行',
        ]),
        ('复盘', VIOLET, [
            '只讲事不讲人',
            '预期与实际逐项对照',
            '每条教训产出可执行规则',
            '规则必须指定落地责任人',
            '复盘的结论要回写成模板',
        ]),
        ('归档进知识库', GREEN, [
            '六类文档按路径入库',
            'front-matter 齐全才收',
            '打标签：领域 / 阶段 / 教训类型',
            '跨项目检索优先于目录浏览',
            '旧版本 superseded 不删除',
        ]),
    ]
    cw, gap = 3.90, 0.35
    x0 = (13 - (3 * cw + 2 * gap)) / 2
    for i, (title, c, items) in enumerate(colsdata):
        x = x0 + i * (cw + gap)
        card(ax, x, 1.55, cw, 4.05, c + '55')
        ax.add_patch(FancyBboxPatch((x, 5.20), cw, 0.40,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=c, edgecolor='none'))
        ax.text(x + cw / 2, 5.40, title, fontsize=8.6, fontweight='bold',
                color='#0d1117', ha='center', va='center')
        for j, it in enumerate(items):
            yy = 4.82 - j * 0.62
            ax.text(x + 0.22, yy, '·', fontsize=9, color=c, ha='left', va='center')
            ax.text(x + 0.44, yy, it, fontsize=7.0, color='#c2cfdc',
                    ha='left', va='center')

    ax.text(6.5, 0.98, '经验教训转化率 = 变成规则的条数 / 记录条数',
            fontsize=8.2, color=AMBER, ha='center', va='center')
    ax.text(6.5, 0.62, '多数团队不到 10%：记了 100 条，30 条进了库，8 条真的改了做法',
            fontsize=8.0, color=DIM, ha='center', va='center')
    save(fig, 'close.png')


# ── 5：四类群消息 ──────────────────────────────────────────────────────
def fig_message():
    fig, ax = canvas(13, 6.9)
    head(ax, 6.9, '整合管理的群消息：只发需要集体知情或集体决策的',
         '单个领域的细节留在领域自己的频道里')

    items = [
        ('变更决策请求', ROSE, '需要 CCB 拍板', [
            '变更编号 + 一句话动因',
            '影响：范围 / 进度 / 成本 各一行',
            '三个选项 + 建议方案',
            '截止时间，超期默认怎么走',
        ]),
        ('里程碑达成', GREEN, '需要集体知情', [
            '里程碑名 + 计划 vs 实际',
            '关键交付物清单',
            '遗留问题与责任人',
            '下一步的前置条件',
        ]),
        ('项目健康度', AMBER, '周期性判断', [
            '一句话结论：绿 / 黄 / 红',
            '三条硬指标：SPI / CPI / 缺陷逃逸率',
            '一个最大风险 + 触发条件',
            '需要的支持，指名到人',
        ]),
        ('收尾归档通知', CYAN, '闭环与复用', [
            '项目名 + 起止时间',
            '验收结论与遗留项',
            '知识库路径',
            '三条可复用的教训',
        ]),
    ]

    cw, ch = 5.95, 2.10
    gx, gy = 0.40, 0.28
    x0 = (13 - (2 * cw + gx)) / 2
    for i, (title, c, tag, lines) in enumerate(items):
        x = x0 + (i % 2) * (cw + gx)
        y = 3.55 - (i // 2) * (ch + gy)
        card(ax, x, y, cw, ch, c + '55')
        ax.add_patch(FancyBboxPatch((x, y + ch - 0.40), 2.35, 0.40,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=c, edgecolor='none'))
        ax.text(x + 0.20, y + ch - 0.20, title, fontsize=7.6, fontweight='bold',
                color='#0d1117', ha='left', va='center')
        ax.text(x + 2.52, y + ch - 0.20, tag, fontsize=6.8, color=DIM,
                ha='left', va='center')
        for j, ln in enumerate(lines):
            ax.text(x + 0.22, y + ch - 0.66 - j * 0.31, '- ' + ln, fontsize=6.7,
                    color='#c2cfdc', ha='left', va='center')

    ax.text(6.5, 0.62, '判断标准很简单：如果这条消息不需要任何人做决定，它就不该进项目群',
            fontsize=8.4, color=AMBER, ha='center', va='center')
    save(fig, 'message.png')


if __name__ == '__main__':
    fig_pipeline()
    fig_conflict()
    fig_change()
    fig_close()
    fig_message()
    print('✓ 全部生成完毕')
