#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0f1618'
PANEL = '#182226'
CARD = '#223034'
TEXT = '#e6eef0'
DIM = '#7d8f94'
CORAL = '#fb923c'
MINT = '#5eead4'
YELLOW = '#fde047'
BLUE = '#60a5fa'
PINK = '#f472b6'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：三个过程 ITTO ────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 6.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.4); ax.axis('off')

    ax.text(6.5, 6.10, '沟通管理只有三个过程，却最容易做完等于没做', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.76, '计划写得再全，没有一条能证明对方真的收到并照做了', fontsize=11.5,
            color=DIM, ha='center')

    procs = [
        ('规划沟通管理', '定规则', CORAL,
         ['项目章程 · 干系人登记册', '项目管理计划', '需求文件 · 风险登记册'],
         ['沟通需求分析', '沟通模型 · 沟通技术', '人际关系与团队技能'],
         ['沟通管理计划', '干系人参与计划更新']),
        ('管理沟通', '促流转', BLUE,
         ['沟通管理计划', '工作绩效报告', '项目文件 · 变更日志'],
         ['沟通技术 · 沟通方法', '沟通技能 · 报告发布', '会议引导与演示'],
         ['项目沟通记录', '变更请求']),
        ('监督沟通', '验闭环', MINT,
         ['项目管理计划', '项目沟通记录', '工作绩效数据 · 问题日志'],
         ['干系人分析', '沟通技能 · 数据表现', 'PMIS 与反馈回路'],
         ['工作绩效信息', '变更请求']),
    ]

    w, gap = 3.95, 0.22
    x0 = (13 - (3 * w + 2 * gap)) / 2
    y, ch = 1.30, 4.20

    for idx, (name, tag, color, inp, tech, out) in enumerate(procs):
        x = x0 + idx * (w + gap)
        ax.add_patch(FancyBboxPatch((x, y), w, ch,
                                    boxstyle='round,pad=0.03,rounding_size=0.09',
                                    facecolor=PANEL, edgecolor='#2a3a3e', linewidth=1.2))
        ax.add_patch(FancyBboxPatch((x, y + ch - 0.66), w, 0.66,
                                    boxstyle='round,pad=0.03,rounding_size=0.09',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.20, y + ch - 0.33, f'{idx + 1:02d}', fontsize=8.6,
                fontweight='bold', color='#10201f', ha='left', va='center')
        ax.text(x + 0.64, y + ch - 0.33, name, fontsize=9.8, fontweight='bold',
                color='#10201f', ha='left', va='center')
        ax.text(x + w - 0.20, y + ch - 0.33, tag, fontsize=7.4, color='#10201f',
                ha='right', va='center')

        blocks = [('输入', inp, BLUE, 4.50, 0.26), ('技术', tech, MINT, 3.32, 0.26),
                  ('输出', out, YELLOW, 2.14, 0.26)]
        for label, items, lc, ly, step in blocks:
            ax.text(x + 0.20, ly, label, fontsize=6.6, fontweight='bold', color=lc,
                    ha='left', va='center')
            ax.plot([x + 0.20, x + 0.62], [ly - 0.14, ly - 0.14], color=lc, lw=1.0, alpha=0.5)
            for k, it in enumerate(items):
                ax.text(x + 0.70, ly - 0.26 * (k + 1), it, fontsize=6.4,
                        color='#c3d1d5', ha='left', va='center')

    ax.text(6.5, 0.90, '前两个过程在「发」，第三个过程才在「验」—— 绝大多数团队只做前两个',
            fontsize=8.4, color=DIM, ha='center', va='center')

    save(fig, 'pipeline.png')


# ── 2：沟通漏斗 + 三层验证 ─────────────────────────────────────────────
def draw_model():
    fig, ax = plt.subplots(figsize=(13, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6.5, 6.35, '同一个意思，每传一层就要少一半', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.02, '从「我想说」到「他真的做了」，中间有四次衰减，没有一次会报错',
            fontsize=11.5, color=DIM, ha='center')

    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.40, 5.25,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=CORAL, linewidth=1.5))
    ax.text(0.75, 5.50, '沟通漏斗 · 一次需求交底的衰减', fontsize=9.0,
            fontweight='bold', color=CORAL, ha='left', va='center')

    stages = [
        ('我想说的', 100, 5.00, CORAL),
        ('我编码后', 80, 4.28, '#fb923c'),
        ('渠道送出的', 60, 3.56, YELLOW),
        ('他解码后', 40, 2.84, BLUE),
        ('他记住并行动', 20, 2.12, MINT),
    ]
    cx = 3.45
    for name, pct, yv, color in stages:
        w = 0.9 + (pct / 100.0) * 4.6
        ax.add_patch(FancyBboxPatch((cx - w / 2, yv - 0.28), w, 0.56,
                                    boxstyle='round,pad=0.01,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0,
                                    alpha=0.90))
        ax.text(cx, yv + 0.01, name, fontsize=7.6, fontweight='bold', color='#10201f',
                ha='center', va='center')
        ax.text(cx + w / 2 + 0.16, yv + 0.01, f'{pct}%', fontsize=7.8,
                fontweight='bold', color=color, ha='left', va='center')

    ax.text(0.75, 1.55, '每一层都在做「合理的简化」，看起来都没错',
            fontsize=7.2, color='#c3d1d5', ha='left', va='center')
    ax.text(0.75, 1.24, '叠加五次之后，偏差已经不是同一个需求了',
            fontsize=7.2, color=DIM, ha='left', va='center')
    ax.text(0.75, 0.92, '而项目经理通常只检查第一层：发出去了吗',
            fontsize=7.4, color=CORAL, ha='left', va='center')

    # 右：三层验证
    ax.add_patch(FancyBboxPatch((7.05, 0.55), 5.50, 5.25,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=MINT, linewidth=1.5))
    ax.text(7.35, 5.50, '三层验证 · 缺一层都不算沟通完成', fontsize=9.0,
            fontweight='bold', color=MINT, ha='left', va='center')

    checks = [
        ('第一层 · 送达', '他能不能在正确的渠道找到这条信息',
         '可观测信号：发送成功、入群、已读回执', BLUE),
        ('第二层 · 理解', '他复述出来的，是不是你想说的那件事',
         '可观测信号：复述、提问、引用原文', YELLOW),
        ('第三层 · 行动', '他的下一步动作，有没有因此改变',
         '可观测信号：任务改期、工单关闭、状态转移', MINT),
    ]
    for idx, (name, line1, line2, color) in enumerate(checks):
        yv = 4.25 - idx * 1.40
        ax.add_patch(FancyBboxPatch((7.35, yv), 4.90, 1.20,
                                    boxstyle='round,pad=0.02,rounding_size=0.07',
                                    facecolor=CARD, edgecolor='#2c3c40', linewidth=1))
        ax.add_patch(FancyBboxPatch((7.35, yv + 0.10), 0.08, 1.00,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(7.58, yv + 0.92, name, fontsize=8.6, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(7.58, yv + 0.58, line1, fontsize=6.9, color='#c3d1d5', ha='left', va='center')
        ax.text(7.58, yv + 0.26, line2, fontsize=6.5, color=DIM, ha='left', va='center')

    ax.text(7.35, 0.88, '三层都验过，才敢说「这件事已经对齐了」',
            fontsize=7.2, color=DIM, ha='left', va='center')

    save(fig, 'model.png')


# ── 3：沟通需求矩阵 ────────────────────────────────────────────────────
def draw_matrix():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.15, '沟通计划不是写给自己看的清单', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.82, '每一行都要能回答：谁、要什么、多久一次、走哪个渠道、谁负责',
            fontsize=11.5, color=DIM, ha='center')

    ax.add_patch(FancyBboxPatch((0.45, 0.70), 12.10, 4.90,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=BLUE, linewidth=1.5))

    cols = ['干系人', '他要的信息', '频率', '渠道', '责任人']
    widths = [1.90, 3.90, 1.55, 2.50, 1.55]
    tx0 = 0.78
    xs = [tx0]
    for wd in widths:
        xs.append(xs[-1] + wd)

    rows = [
        ('高管 / PMO', '里程碑、整体风险、投入产出', '每月', '邮件 + 月度评审', '项目经理', CORAL),
        ('职能经理', '人力占用与释放计划', '每两周', '资源日历 + 单独同步', '项目经理', BLUE),
        ('客户方', '可验收成果、变更影响', '每迭代', '演示 + 变更单', '产品经理', YELLOW),
        ('开发组', '任务口径、依赖变化', '每日', '站会 + 看板', '技术负责人', MINT),
        ('运维', '上线窗口、回滚方案', '每次发布', '发布通知 + 应急群', '发布经理', PINK),
    ]

    top = 5.42
    hh = 0.60
    ax.add_patch(FancyBboxPatch((tx0, top - hh), sum(widths), hh,
                                boxstyle='round,pad=0.02,rounding_size=0.05',
                                facecolor=BLUE, edgecolor=BLUE, linewidth=0))
    for j, c in enumerate(cols):
        ax.text(xs[j] + 0.16, top - hh / 2, c, fontsize=8.0, fontweight='bold',
                color='#10201f', ha='left', va='center')

    rh = 0.74
    for i, (who, info, freq, chan, owner, color) in enumerate(rows):
        ry = top - hh - (i + 1) * rh
        ax.add_patch(FancyBboxPatch((tx0, ry), sum(widths), rh,
                                    boxstyle='round,pad=0.01,rounding_size=0.04',
                                    facecolor=CARD if i % 2 == 0 else '#1d282c',
                                    edgecolor='#2a3a3e', linewidth=0.8))
        ax.add_patch(FancyBboxPatch((tx0, ry + 0.10), 0.07, rh - 0.20,
                                    boxstyle='round,pad=0.01,rounding_size=0.02',
                                    facecolor=color, edgecolor=color, linewidth=0))
        vals = [who, info, freq, chan, owner]
        for j, v in enumerate(vals):
            ax.text(xs[j] + (0.20 if j != 0 else 0.22), ry + rh / 2, v,
                    fontsize=6.9 if j != 1 else 7.0,
                    fontweight='bold' if j == 0 else 'normal',
                    color=color if j == 0 else '#c3d1d5', ha='left', va='center')

    ax.text(0.78, 0.88, '关键不是信息多，是「同一件事只有一个权威来源」 —— 否则一定会出现两个版本',
            fontsize=7.6, color=DIM, ha='left', va='center')

    save(fig, 'matrix.png')


# ── 4：渠道留存 + 四个指标 ─────────────────────────────────────────────
def draw_metric():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.25, '同一条信息，换个渠道留存率差六倍', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.92, '所以「我已经发群里了」从来不构成一次有效沟通',
            fontsize=11.5, color=DIM, ha='center')

    ax.add_patch(FancyBboxPatch((0.45, 0.55), 6.45, 5.10,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=YELLOW, linewidth=1.5))
    ax.text(0.75, 5.35, '五种渠道的信息留存率', fontsize=9.0, fontweight='bold',
            color=YELLOW, ha='left', va='center')
    ax.text(0.75, 5.06, '留存率 = 一周后仍能准确复述的人占比', fontsize=6.8,
            color=DIM, ha='left', va='center')

    chans = [('会议（有结论）', 72, CORAL), ('一对一沟通', 68, '#fdba74'),
             ('文档（被读过）', 34, BLUE), ('群消息', 18, '#93c5fd'),
             ('群发邮件', 11, MINT)]
    bx = 2.75
    scale = 3.15 / 100.0
    for idx, (name, pct, color) in enumerate(chans):
        yv = 4.42 - idx * 0.76
        ax.text(2.62, yv + 0.27, name, fontsize=7.4, color=TEXT, ha='right', va='center')
        ax.add_patch(FancyBboxPatch((bx, yv), 3.15, 0.54,
                                    boxstyle='round,pad=0.01,rounding_size=0.05',
                                    facecolor='#131c20', edgecolor='#2a3a3e', linewidth=0))
        ax.add_patch(FancyBboxPatch((bx, yv), pct * scale, 0.54,
                                    boxstyle='round,pad=0.01,rounding_size=0.05',
                                    facecolor=color, edgecolor=color, linewidth=0, alpha=0.92))
        ax.text(bx + pct * scale + 0.12, yv + 0.27, f'{pct}%', fontsize=7.6,
                fontweight='bold', color=color, ha='left', va='center')

    ax.text(0.75, 1.10, '重要的事要选高留存渠道，并留一个「请复述」的动作',
            fontsize=7.2, color='#c3d1d5', ha='left', va='center')
    ax.text(0.75, 0.80, '低留存渠道只适合通知，不适合对齐',
            fontsize=7.0, color=DIM, ha='left', va='center')

    ax.add_patch(FancyBboxPatch((7.10, 0.55), 5.45, 5.10,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=MINT, linewidth=1.5))
    ax.text(7.40, 5.35, '监督沟通只看四个数', fontsize=9.0, fontweight='bold',
            color=MINT, ha='left', va='center')

    metrics = [
        ('到达率', '94%', '发送失败、漏发、发错群', BLUE),
        ('已读率', '61%', '关键人到底看没看到', YELLOW),
        ('响应时效', '4.2 h', '关键决策平均等待时长', CORAL),
        ('闭环率', '58%', '有结论、有责任人、有日期', MINT),
    ]
    for idx, (name, val, note, color) in enumerate(metrics):
        yv = 4.10 - idx * 0.90
        ax.add_patch(FancyBboxPatch((7.40, yv), 4.85, 0.76,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=CARD, edgecolor='#2c3c40', linewidth=1))
        ax.text(7.60, yv + 0.50, name, fontsize=7.8, color='#c3d1d5', ha='left', va='center')
        ax.text(12.05, yv + 0.50, val, fontsize=8.6, fontweight='bold', color=color,
                ha='right', va='center')
        ax.text(7.60, yv + 0.20, note, fontsize=6.5, color=DIM, ha='left', va='center')

    ax.text(7.40, 0.80, '四个数里，闭环率最能说明问题', fontsize=7.2, color=DIM,
            ha='left', va='center')

    save(fig, 'metric.png')


# ── 5：四类群消息 ──────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '沟通消息按「要对方做什么」分四类', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.72, '没有请求的消息不叫沟通，叫广播', fontsize=11.5,
            color=DIM, ha='center')

    cards = [
        ('决策请求', '需要拍板', CORAL, [
            '接口超时方案二选一，今天 17:00 前要定',
            '· 方案 A：加缓存，改 3 处，2 天',
            '· 方案 B：改协议，改 11 处，5 天',
            '请 @张总 17:00 前回复 A 或 B',
        ]),
        ('状态同步', '每周五 17:00', BLUE, [
            '本周完成 7/9，1 项延期，上线窗口不变',
            '· 延期：对账联调，上游接口未就绪',
            '· 风险：灰度比例仍按 20% 推进',
            '详情见 KB：PRJ-PAY / W45',
        ]),
        ('风险升级', '连续两次未响应', YELLOW, [
            '上游接口已延期 5 天，触发升级条件',
            '· 已尝试：3 次催办、2 次协调会',
            '· 若不处理：上线推迟到 12/02',
            '请 @李经理 明日前给出可执行排期',
        ]),
        ('会议结论', '会后 30 分钟内', MINT, [
            '评审会结论 3 条，全部责任人已确认',
            '· 缓存方案通过，王工 11/13 前完成',
            '· 灰度 5% 提到 20%，赵工跟进',
            '有异议请在今晚前提出，逾期视为认可',
        ]),
    ]

    positions = [(0.45, 3.85), (6.65, 3.85), (0.45, 0.65), (6.65, 0.65)]
    for (title, freq, color, lines), (cx, cy) in zip(cards, positions):
        cw, ch = 5.9, 2.75
        ax.add_patch(FancyBboxPatch((cx, cy), cw, ch,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.add_patch(FancyBboxPatch((cx + 0.22, cy + ch - 0.68), 1.5, 0.42,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(cx + 0.97, cy + ch - 0.47, title, fontsize=8.4, fontweight='bold',
                color='#10201f', ha='center', va='center')
        ax.text(cx + 1.85, cy + ch - 0.47, freq, fontsize=7.0, color=DIM,
                ha='left', va='center')

        iy = cy + ch - 1.05
        for j, line in enumerate(lines):
            ax.text(cx + 0.28, iy, line, fontsize=7.4,
                    color=TEXT if j == 0 else '#c3d1d5',
                    ha='left', va='center',
                    fontweight='bold' if j == 0 else 'normal')
            iy -= 0.42

    ax.text(6.5, 0.28, '每条四行：判断 / 依据 / 影响 / 要谁在什么时候做什么',
            fontsize=8.2, color=DIM, ha='center', va='center')

    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_model()
    draw_matrix()
    draw_metric()
    draw_message()
    print('✓ 全部生成完毕')
