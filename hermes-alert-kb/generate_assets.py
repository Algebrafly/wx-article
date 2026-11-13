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

BG = '#0a1628'
PANEL = '#122036'
CARD = '#1b3050'
TEXT = '#e2e8f0'
DIM = '#64748b'
RED = '#ef4444'
ORANGE = '#f97316'
YELLOW = '#eab308'
GREEN = '#22c55e'
BLUE = '#3b82f6'
PURPLE = '#a855f7'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：告警处理流水线 ───────────────────────────────────────────────────────
def draw_flow():
    fig, ax = plt.subplots(figsize=(13, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6.5, 6.35, '告警不是消息轰炸，是行动清单', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.9, '从信号到方案，四步过滤掉噪音、挂上知识库', fontsize=12, color=DIM, ha='center')

    steps = [
        ('采集', '日志 · 指标 · 事件', BLUE, 'SLS / Prometheus / 云监控'),
        ('归一', '过滤 · 去重 · 分级', ORANGE, '一分钟内相同告警只留一条'),
        ('检索', '企业知识库找方案', GREEN, '错误码 + 服务名 + 关键词'),
        ('投递', '企微 / 飞书群机器人', RED, '告警信息 + 解决方案 + 链接'),
    ]

    w = 2.3; h = 2.35; gap = 0.3
    total = w * 4 + gap * 3
    x0 = (13 - total) / 2
    yc = 3.55

    for i, (title, desc, color, note) in enumerate(steps):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.add_patch(plt.Circle((x + w / 2, yc + h / 2 - 0.32), 0.19,
                                facecolor=color, edgecolor='none', zorder=4))
        ax.text(x + w / 2, yc + h / 2 - 0.32, str(i + 1), fontsize=11, fontweight='bold',
                color=BG, ha='center', va='center', zorder=5)
        ax.text(x + w / 2, yc + 0.55, title, fontsize=13, fontweight='bold',
                color=TEXT, ha='center', va='center')
        ax.text(x + w / 2, yc - 0.12, desc, fontsize=9.2, color=color,
                ha='center', va='center')
        ax.text(x + w / 2, yc - 0.72, note, fontsize=7.8, color=DIM,
                ha='center', va='center')
        if i < 3:
            ax.annotate('', xy=(x + w + gap - 0.015, yc), xytext=(x + w + 0.015, yc),
                        arrowprops=dict(arrowstyle='->', color=DIM, lw=1.5))

    # 底部：降级策略
    ax.add_patch(FancyBboxPatch((2.0, 0.55), 9.0, 0.7,
                                boxstyle='round,pad=0.03,rounding_size=0.1',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(6.5, 0.9, '网关挂了 → 走兜底 webhook · 知识库查不到 → 只发告警不带方案 · 全挂了 → 保留日志事后回放',
            fontsize=9.0, color=TEXT, ha='center', va='center')

    save(fig, 'flow.png')


# ── 2：三路采集 ─────────────────────────────────────────────────────────────
def draw_collect():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6); ax.axis('off')

    ax.text(6.5, 7.15, '三路信号，各自有坑', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.7, '缺哪一路都会漏，但全拉了就是雪崩 —— 必须先分级再接入', fontsize=12,
            color=DIM, ha='center')

    sources = [
        ('业务日志', RED, '阿里云 SLS / ELK / 自建 Loki', [
            ('ERROR / FATAL', '必须告警'),
            ('WARN 批量出现', '阈值触发'),
            ('慢查询堆积', '5 分钟 > 10 条'),
        ]),
        ('服务器指标', BLUE, 'Prometheus + Grafana / 云监控', [
            ('CPU / 内存 > 90%', '持续 5 分钟'),
            ('磁盘剩余 < 10%', '硬红线'),
            ('网络丢包 > 1%', '跨 AZ 才管'),
        ]),
        ('云厂商事件', ORANGE, '阿里云 EventBridge / CloudWatch', [
            ('实例异常重启', '立即通知'),
            ('证书到期 < 15 天', '每日汇总'),
            ('安全组变更', '需要审计'),
        ]),
    ]

    w = 3.7; h = 5.3; gap = 0.2
    total = w * 3 + gap * 2
    x0 = (13 - total) / 2
    yb = 0.95

    for i, (name, color, src, items) in enumerate(sources):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, yb), w, h,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.8))
        ax.add_patch(FancyBboxPatch((x + 0.2, yb + h - 0.7), w - 0.4, 0.55,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + w / 2, yb + h - 0.425, name, fontsize=12, fontweight='bold',
                color=BG, ha='center', va='center')
        ax.text(x + 0.3, yb + h - 1.1, src, fontsize=8.2, color=DIM,
                ha='left', va='center')

        # 采集点
        iy = yb + h - 1.55
        for j, (trigger, note) in enumerate(items):
            ax.add_patch(plt.Circle((x + 0.45, iy + 0.1), 0.08,
                                    facecolor=color, edgecolor='none', zorder=4))
            ax.text(x + 0.65, iy + 0.18, trigger, fontsize=8.8, fontweight='bold',
                    color=TEXT, ha='left', va='center')
            ax.text(x + 0.65, iy - 0.12, note, fontsize=7.4, color=DIM,
                    ha='left', va='center')
            iy -= 0.72

        # 底部：频率
        ax.add_patch(FancyBboxPatch((x + 0.2, yb + 0.2), w - 0.4, 0.55,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=DIM, linewidth=1))
        freq = ['每 30 秒拉', '每 60 秒拉', '事件推送']
        ax.text(x + w / 2, yb + 0.475, freq[i], fontsize=8.5, color=DIM,
                ha='center', va='center')

    save(fig, 'collect.png')


# ── 3：分级 + 降噪 ─────────────────────────────────────────────────────────
def draw_filter():
    fig, ax = plt.subplots(figsize=(13, 7.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.4); ax.axis('off')

    ax.text(6.5, 7.0, '90% 的告警其实不值得看', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.55, '分级 + 聚合 + 降噪 —— 三道闸门把 1000 条压到 10 条', fontsize=12,
            color=DIM, ha='center')

    # 漏斗
    stages = [
        ('原始信号', '1000+ 条/天', RED, '全部进来'),
        ('分级过滤', '~300 条', ORANGE, 'INFO 直接丢弃'),
        ('时间窗口聚合', '~80 条', YELLOW, '同错误码 5 分钟只留 1 条'),
        ('关联去重', '~25 条', GREEN, '一次故障连带的 10 条合并'),
        ('最终投递', '~10 条', BLUE, '发到群里'),
    ]

    y = 6.0
    for i, (label, count, color, note) in enumerate(stages):
        width = 11.0 - i * 2.0
        x = (13 - width) / 2
        h = 0.75
        ax.add_patch(FancyBboxPatch((x, y - h / 2), width, h,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=color, linewidth=1.4,
                                    alpha=0.9))
        ax.text(x + 0.3, y + 0.08, label, fontsize=11, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(x + width - 0.3, y + 0.08, count, fontsize=11, fontweight='bold',
                color=TEXT, ha='right', va='center')
        ax.text(x + width / 2, y - 0.25, note, fontsize=7.5, color=DIM,
                ha='center', va='center')
        y -= 1.1

    # 右侧：分级规则
    ax.add_patch(FancyBboxPatch((0.5, 0.55), 4.2, 1.6,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PANEL, edgecolor=RED, linewidth=1.2))
    ax.text(0.75, 1.95, '四级分级', fontsize=9.5, fontweight='bold', color=RED, ha='left')
    levels = [
        ('P0 紧急', '立即电话 + 群内 @all', RED),
        ('P1 严重', '群内 @oncall', ORANGE),
        ('P2 一般', '汇总到日报', YELLOW),
        ('P3 提示', '只写日志不通知', DIM),
    ]
    ly = 1.7
    for lv, desc, color in levels:
        ax.add_patch(FancyBboxPatch((0.75, ly - 0.12), 0.75, 0.28,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.125, ly + 0.02, lv, fontsize=7.6, fontweight='bold', color=BG,
                ha='center', va='center')
        ax.text(1.6, ly + 0.02, desc, fontsize=7.8, color=TEXT,
                ha='left', va='center')
        ly -= 0.38

    save(fig, 'filter.png')


# ── 4：知识库检索 + 投递卡 ───────────────────────────────────────────────────
def draw_solution():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.35, '告警本身没价值，附上方案才有用', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.9, '同一错误码被 5 个人查过，知识库就会记得答案', fontsize=12, color=DIM, ha='center')

    # 左：知识库检索
    ax.add_patch(FancyBboxPatch((0.5, 0.85), 4.2, 6.0,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=GREEN, linewidth=1.8))
    ax.text(0.85, 6.55, '知识库检索', fontsize=11.5, fontweight='bold',
            color=GREEN, ha='left', va='center')
    ax.text(0.85, 6.28, '命中 3 条，按置信度排序', fontsize=8, color=DIM, ha='left', va='center')
    ax.plot([0.85, 4.3], [6.1, 6.1], color='#2e3f5a', lw=1)

    matches = [
        ('ERR_LOCK_TIMEOUT · PostgreSQL', '置信度 95%\n上次出现：3 天前\n根因：长事务未提交\n解决：kill pid + 缩短事务', GREEN),
        ('ERR_DB_CONNECTION_POOL', '置信度 78%\n上次出现：2 周前\n根因：连接池耗尽\n解决：调大 max 或重启服务', BLUE),
        ('ERR_503_UPSTREAM', '置信度 60%\n上次出现：1 个月前\n根因：下游超时\n解决：重试 + 降级缓存', ORANGE),
    ]
    y = 5.75
    for title, content, color in matches:
        ax.add_patch(FancyBboxPatch((0.85, y - 0.85), 3.5, 0.8,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=color, linewidth=1))
        ax.text(1.02, y - 0.2, title, fontsize=8.2, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(1.02, y - 0.55, content, fontsize=6.9, color=TEXT,
                ha='left', va='top', linespacing=1.55)
        y -= 1.0

    # 右：企微群消息卡
    ax.add_patch(FancyBboxPatch((5.05, 0.85), 7.25, 6.0,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=RED, linewidth=1.8))
    ax.text(5.4, 6.55, '企微群机器人消息示例', fontsize=11.5, fontweight='bold',
            color=TEXT, ha='left', va='center')
    ax.text(5.4, 6.28, '格式：告警信息 + 解决方案 + 链接 + @oncall', fontsize=8,
            color=DIM, ha='left', va='center')
    ax.plot([5.4, 11.9], [6.1, 6.1], color='#2e3f5a', lw=1)

    # 告警头
    ax.add_patch(FancyBboxPatch((5.4, 5.45), 6.55, 0.6,
                                boxstyle='round,pad=0.02,rounding_size=0.06',
                                facecolor=RED, edgecolor=RED, linewidth=0))
    ax.text(5.55, 5.75, '[P0] 紧急 - 支付服务 ERR_LOCK_TIMEOUT', fontsize=10.5,
            fontweight='bold', color=BG, ha='left', va='center')
    ax.text(5.55, 5.52, '2026-11-05 14:32:18 · 实例 pay-svc-03', fontsize=7.8,
            color='#fecaca', ha='left', va='center')

    # 错误信息
    ax.text(5.4, 5.15, '错误信息', fontsize=9, fontweight='bold', color=TEXT, ha='left')
    ax.add_patch(FancyBboxPatch((5.4, 4.6), 6.55, 0.5,
                                boxstyle='round,pad=0.02,rounding_size=0.04',
                                facecolor='#0f172a', edgecolor='#334155', linewidth=1))
    ax.text(5.55, 4.85, 'canceling statement due to lock timeout', fontsize=7.4,
            color='#f87171', ha='left', va='center')

    # 解决方案
    ax.text(5.4, 4.3, '[KB] 知识库建议（置信度 95%）', fontsize=9, fontweight='bold',
            color=GREEN, ha='left')
    ax.text(5.4, 3.9, '根因：长事务未提交导致行锁堆积', fontsize=8.2, color=TEXT,
            ha='left', va='center')
    ax.text(5.4, 3.58, '立即执行：', fontsize=8.2, color=DIM, ha='left', va='center')
    ax.text(5.4, 3.3,
            'psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity\n'
            "WHERE state = 'idle in transaction' AND\n"
            "query_start < now() - interval '10 min'\"",
            fontsize=6.5, color='#6ee7b7', ha='left', va='top',
            fontfamily='monospace', linespacing=1.45)

    ax.text(5.4, 2.75, '长期修复：缩短事务粒度，加行锁超时重试', fontsize=8.2,
            color=TEXT, ha='left', va='center')

    # 操作链接
    ax.add_patch(FancyBboxPatch((5.4, 1.85), 2.05, 0.55,
                                boxstyle='round,pad=0.02,rounding_size=0.08',
                                facecolor=BLUE, edgecolor=BLUE, linewidth=0))
    ax.text(6.425, 2.125, '[链接] 完整方案', fontsize=8.2, fontweight='bold', color=BG,
            ha='center', va='center')
    ax.add_patch(FancyBboxPatch((7.6, 1.85), 2.05, 0.55,
                                boxstyle='round,pad=0.02,rounding_size=0.08',
                                facecolor=PURPLE, edgecolor=PURPLE, linewidth=0))
    ax.text(8.625, 2.125, '[面板] 监控面板', fontsize=8.2, fontweight='bold', color=BG,
            ha='center', va='center')
    ax.add_patch(FancyBboxPatch((9.8, 1.85), 2.15, 0.55,
                                boxstyle='round,pad=0.02,rounding_size=0.08',
                                facecolor=ORANGE, edgecolor=ORANGE, linewidth=0))
    ax.text(10.875, 2.125, '[通知] @oncall 张三', fontsize=8.2, fontweight='bold',
            color=BG, ha='center', va='center')

    ax.text(5.4, 1.3, '知识库命中 ID：KB-ERR-LOCK-TIMEOUT-003 · 上次验证：3 天前',
            fontsize=7.2, color=DIM, ha='left', va='center')

    save(fig, 'solution.png')


if __name__ == '__main__':
    draw_flow()
    draw_collect()
    draw_filter()
    draw_solution()
    print('✓ 全部生成完毕')
