#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0b1526'
PANEL = '#132238'
CARD = '#1b2c46'
TEXT = '#e2e8f0'
DIM = '#64748b'
TEAL = '#2dd4bf'
AMBER = '#fbbf24'
CORAL = '#f87171'
BLUE = '#60a5fa'
VIOLET = '#a78bfa'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：主流程 ─────────────────────────────────────────────────────────────
def draw_flow():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.15, '状态一改成「待测试」，后面全自动', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.65, '从监听事件到 BUG 回写，六段无人值守', fontsize=12, color=DIM, ha='center')

    steps = [
        ('监听', '状态 → 待测试', TEAL, 'webhook + 兜底轮询'),
        ('取料', '需求 + 用例', BLUE, '平台字段 + 仓库 test'),
        ('准备', '拉起环境', AMBER, '容器 / 测试库 / mock'),
        ('执行', '跑测试集', CORAL, '接口 / UI / 单测'),
        ('报告', '结构化结果', VIOLET, '通过率 + 失败明细'),
        ('回写', '建 BUG', TEAL, '带证据 + 去重'),
    ]

    w = 1.8; h = 2.35; gap = 0.31
    total = w * 6 + gap * 5
    x0 = (13 - total) / 2
    yc = 2.95

    for i, (title, desc, color, note) in enumerate(steps):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        # 序号圆点
        ax.add_patch(plt.Circle((x + w / 2, yc + h / 2 - 0.32), 0.19,
                                facecolor=color, edgecolor='none', zorder=4))
        ax.text(x + w / 2, yc + h / 2 - 0.32, str(i + 1), fontsize=11, fontweight='bold',
                color=BG, ha='center', va='center', zorder=5)
        ax.text(x + w / 2, yc + 0.45, title, fontsize=14, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(x + w / 2, yc - 0.05, desc, fontsize=9.2, color=color,
                ha='center', va='center', linespacing=1.5)
        ax.text(x + w / 2, yc - 0.72, note, fontsize=7.8, color=DIM,
                ha='center', va='center', linespacing=1.4)
        if i < 5:
            ax.annotate('', xy=(x + w + gap - 0.015, yc), xytext=(x + w + 0.015, yc),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))

    # 底部：耗时/门槛
    ax.add_patch(FancyBboxPatch((3.05, 0.45), 6.9, 0.62,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 0.76, '端到端 3–12 分钟  ·  失败必留证据  ·  同一 BUG 不重复建单',
            fontsize=9.5, color=TEXT, ha='center', va='center')

    save(fig, 'flow.png')


# ── 2：四平台触发方式对比 ─────────────────────────────────────────────────
def draw_trigger():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.7, '四个平台，四种触发姿势', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.2, '能 webhook 就 webhook，不能就轮询 —— 两者都要做', fontsize=12,
            color=DIM, ha='center')

    cards = [
        ('Jira', 'Webhook', 'jira:issue_updated\n事件体自带 changelog', TEAL, '最规范'),
        ('禅道', '内置触发器', 'action=edittask\n需自建回调地址', AMBER, '要改造'),
        ('PingCode', 'Webhook', 'work_item.updated\n支持状态过滤', BLUE, '可用'),
        ('阿里云效', 'Webhook + 轮询', '状态变更事件\n延迟偶发偏高', CORAL, '需兜底'),
    ]

    w = 2.82; gap = 0.18
    total = w * 4 + gap * 3
    x0 = (13 - total) / 2
    yb = 2.05

    for i, (name, mode, desc, color, tag) in enumerate(cards):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yb + 3.3), w, 0.72,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2, yb + 3.66, name, fontsize=14, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.add_patch(FancyBboxPatch((x, yb), w, 3.15,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.6))
        ax.text(x + w / 2, yb + 2.55, mode, fontsize=11, fontweight='bold',
                color=color, ha='center', va='center')
        ax.text(x + w / 2, yb + 1.62, desc, fontsize=8.5, color=TEXT,
                ha='center', va='center', linespacing=1.55)
        # tag
        ax.add_patch(FancyBboxPatch((x + w / 2 - 0.62, yb + 0.3), 1.24, 0.42,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=CARD, edgecolor=color, linewidth=1))
        ax.text(x + w / 2, yb + 0.51, tag, fontsize=8.5, color=color,
                ha='center', va='center')

    # 兜底轮询条
    ax.add_patch(FancyBboxPatch((1.0, 0.55), 11.0, 1.05,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PANEL, edgecolor=VIOLET, linewidth=1.6))
    ax.text(1.35, 1.28, '兜底：每 10 分钟轮询一次', fontsize=10.5, fontweight='bold',
            color=VIOLET, ha='left')
    ax.text(1.35, 0.88, '查询状态为「待测试」且 24h 内未被处理的工作项，补触发 —— webhook 丢了也不会漏',
            fontsize=8.8, color=TEXT, ha='left')

    save(fig, 'trigger.png')


# ── 3：执行矩阵 ───────────────────────────────────────────────────────────
def draw_matrix():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.9, '四类测试，四种跑法', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.45, '按需求说明里有什么，决定跑哪几类 —— 不是每次都全跑', fontsize=11.8,
            color=DIM, ha='center')

    headers = ['测试类型', '输入', '执行方式', '典型耗时', '产物']
    hx = [0.75, 3.35, 6.05, 8.85, 10.35]
    for h, x in zip(headers, hx):
        ax.text(x, 5.95, h, fontsize=10, fontweight='bold', color=BLUE, ha='left')

    rows = [
        ('接口测试', 'OpenAPI 文档\n+ 用例表', '容器内跑 pytest\nrequests 打真实服务', '2–5 分钟', '请求/响应、状态码', TEAL),
        ('单元测试', '仓库 test/ 目录\n或改动模块', '沙箱内 go test\n/ pytest 指定包', '30 秒–2 分钟', '覆盖率、失败栈', BLUE),
        ('UI 回归', '用例里的\n页面路径', '无头浏览器\nPlaywright 脚本', '5–15 分钟', '截图、DOM、录屏', AMBER),
        ('契约测试', '服务间接口\n契约文件', '比对响应 schema\n与契约版本', '1–3 分钟', '字段差异清单', VIOLET),
    ]

    y = 5.25
    for name, inp, way, cost, out, color in rows:
        ax.add_patch(FancyBboxPatch((0.65, y - 0.55), 11.7, 1.1,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor='#223449', linewidth=1))
        # 左侧色条
        ax.add_patch(FancyBboxPatch((0.65, y - 0.55), 0.12, 1.1,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(0.95, y, name, fontsize=11, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(3.35, y, inp, fontsize=8.5, color=TEXT, ha='left', va='center', linespacing=1.5)
        ax.text(6.05, y, way, fontsize=8.5, color=TEXT, ha='left', va='center', linespacing=1.5)
        ax.text(8.85, y, cost, fontsize=9, color=AMBER, ha='left', va='center')
        ax.text(10.35, y, out, fontsize=8.5, color=DIM, ha='left', va='center', linespacing=1.5)
        y -= 1.28

    ax.text(6.5, 0.32, '全部在一次性容器里跑 —— 跑完即销毁，不污染共享测试环境',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'matrix.png')


# ── 4：报告 + BUG 卡片 ────────────────────────────────────────────────────
def draw_report():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.3, '测试报告与 BUG 卡片长什么样', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.85, '同一份结果，两种读者：人看结论，平台看字段', fontsize=11.8,
            color=DIM, ha='center')

    # 左：报告卡片
    ax.add_patch(FancyBboxPatch((0.6, 0.75), 5.85, 5.7,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=TEAL, linewidth=1.8))
    ax.text(0.9, 6.05, 'PAY-3412 · 分账功能回归', fontsize=12, fontweight='bold',
            color=TEXT, ha='left')
    ax.text(0.9, 5.7, '触发：状态改为「待测试」 · 09:12', fontsize=8.5, color=DIM, ha='left')
    ax.plot([0.9, 6.15], [5.5, 5.5], color='#223449', lw=1)

    stats = [('用例 48', TEAL), ('通过 41', '#34d399'), ('失败 7', CORAL)]
    x = 0.9
    for label, color in stats:
        ax.add_patch(FancyBboxPatch((x, 4.85), 1.55, 0.45,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=CARD, edgecolor=color, linewidth=1))
        ax.text(x + 0.775, 5.075, label, fontsize=9, fontweight='bold', color=color,
                ha='center', va='center')
        x += 1.72

    ax.text(0.9, 4.45, '失败明细', fontsize=9.5, fontweight='bold', color=CORAL, ha='left')
    fails = [
        '- 拆单金额与子商户合计不符（期望 100.00）',
        '- 子商户账户余额不足时错误码为 500',
        '- 分账后主订单状态未同步为「已结算」',
    ]
    y = 4.1
    for f in fails:
        ax.text(0.95, y, f, fontsize=8.2, color=TEXT, ha='left', va='center')
        y -= 0.36
    ax.text(0.9, 3.0, '… 另有 4 条，已折叠', fontsize=8, color=DIM, ha='left')

    ax.plot([0.9, 6.15], [2.75, 2.75], color='#223449', lw=1)
    ax.text(0.9, 2.45, '证据附件', fontsize=9.5, fontweight='bold', color=BLUE, ha='left')
    ev = ['请求/响应 JSON 快照', '失败截图 7 张', '执行日志（含 trace_id）']
    y = 2.12
    for e in ev:
        ax.text(0.95, y, '· ' + e, fontsize=8.2, color=DIM, ha='left', va='center')
        y -= 0.32

    # 右：BUG 卡片
    ax.add_patch(FancyBboxPatch((6.85, 0.75), 5.55, 5.7,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=CORAL, linewidth=1.8))
    ax.add_patch(FancyBboxPatch((7.05, 5.55), 0.55, 0.5,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=CORAL, edgecolor=CORAL, linewidth=0))
    ax.text(7.325, 5.8, 'B', fontsize=12, fontweight='bold', color=BG,
            ha='center', va='center')
    ax.text(7.75, 5.85, 'BUG · 已建单', fontsize=11, fontweight='bold', color=CORAL, ha='left')
    ax.text(7.75, 5.55, 'PAY-3521', fontsize=9, fontweight='bold', color=TEXT, ha='left')

    fields = [
        ('标题', '拆单金额与子商户合计不符'),
        ('所属项目', '支付平台 / PAY'),
        ('类型', 'Bug · 严重：高'),
        ('经办人', '张三（代码 blame 命中）'),
        ('关联需求', 'PAY-3412'),
        ('环境', 'test · v2.3.0-rc1'),
        ('复现率', '7/48 用例稳定失败'),
    ]
    y = 4.95
    for k, v in fields:
        ax.text(7.05, y, k, fontsize=8, color=DIM, ha='left', va='center')
        ax.text(8.55, y, v, fontsize=8.2, color=TEXT, ha='left', va='center')
        y -= 0.42

    ax.plot([7.05, 12.2], [1.85, 1.85], color='#223449', lw=1)
    ax.text(7.05, 1.6, '描述自动附带：失败用例名 / 请求响应 / 截图链接',
            fontsize=8, color=DIM, ha='left')
    ax.text(7.05, 1.25, '查重：同标题 + 同模块 → 追加复现次数，不新建',
            fontsize=8, color=AMBER, ha='left')

    save(fig, 'report.png')


if __name__ == '__main__':
    draw_flow(); draw_trigger(); draw_matrix(); draw_report()
    print('done')
