#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib import font_manager

for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#170f12'
PANEL = '#241820'
CARD = '#32212c'
TEXT = '#f6ecef'
DIM = '#94818c'
GOLD = '#f5b942'
ROSE = '#fb7185'
JADE = '#4ade80'
SKY = '#60a5fa'
LILAC = '#c084fc'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：一天两次调度 ─────────────────────────────────────────────────────────
def draw_flow():
    fig, ax = plt.subplots(figsize=(13, 6.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.6); ax.axis('off')

    ax.text(6.5, 6.15, '一天两次，早上排兵，晚上交卷', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 5.7, '全程只读平台数据，不改任何任务状态', fontsize=12, color=DIM, ha='center')

    panels = [
        (0.6, '08:30 · 个人作战图', GOLD, [
            ('拉取', '四平台「我负责的」待办', '按人过滤，不拉全量'),
            ('归一', '打分后落进四象限', '重要度 × 紧急度'),
            ('推送', '企微 / 飞书 私聊本人', '一张图 + 今日前三件事'),
        ]),
        (6.78, '18:00 · 向上交答卷', ROSE, [
            ('采集', '状态变更 + 工时 + 提交', '当日区间，按人聚合'),
            ('生成', '日报四段：完成 / 进行 / 风险 / 明日', 'AI 归因，不写流水账'),
            ('投递', '项目大群 + 平台记录', '群里可见，平台可查'),
        ]),
    ]

    for px, title, color, steps in panels:
        w = 5.6
        ax.add_patch(FancyBboxPatch((px, 0.95), w, 4.45,
                                    boxstyle='round,pad=0.05,rounding_size=0.14',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.8))
        ax.text(px + 0.3, 5.02, title, fontsize=12, fontweight='bold',
                color=color, ha='left', va='center')
        ax.plot([px + 0.3, px + w - 0.3], [4.82, 4.82], color='#3c2a36', lw=1)

        ys = [3.95, 2.72, 1.49]
        for i, (name, desc, note) in enumerate(steps):
            y = ys[i]
            ax.add_patch(plt.Circle((px + 0.62, y + 0.12), 0.2,
                                    facecolor=color, edgecolor='none', zorder=4))
            ax.text(px + 0.62, y + 0.12, str(i + 1), fontsize=10, fontweight='bold',
                    color=BG, ha='center', va='center', zorder=5)
            ax.text(px + 0.98, y + 0.3, name, fontsize=10.5, fontweight='bold',
                    color=TEXT, ha='left', va='center')
            ax.text(px + 0.98, y - 0.02, desc, fontsize=8.5, color=color,
                    ha='left', va='center')
            ax.text(px + 0.98, y - 0.32, note, fontsize=7.6, color=DIM,
                    ha='left', va='center')
            if i < 2:
                ax.annotate('', xy=(px + 0.62, ys[i + 1] + 0.4),
                            xytext=(px + 0.62, y - 0.14),
                            arrowprops=dict(arrowstyle='->', color=DIM, lw=1.2))

    ax.text(6.5, 0.55, '两个任务互不依赖：早上失败不影响晚上，晚上失败第二天早上照常',
            fontsize=9.2, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'flow.png')


# ── 2：四象限 ───────────────────────────────────────────────────────────────
def draw_quadrant():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.4, '不是所有待办都值得今天做', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.95, '重要度看影响，紧急度看时间 —— 两个分数各自独立算', fontsize=12,
            color=DIM, ha='center')

    x0, x1 = 2.35, 11.15
    y0, y1 = 1.15, 6.25
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2

    rects = [
        (x0, my, mx - x0, y1 - my, GOLD, '重要 · 不紧急', '排期做', 0.22),
        (mx, my, x1 - mx, y1 - my, ROSE, '重要 · 紧急', '立刻做', 0.18),
        (x0, y0, mx - x0, my - y0, '#6b5a64', '不重要 · 不紧急', '砍掉或延后', 0.13),
        (mx, y0, x1 - mx, my - y0, SKY, '不重要 · 紧急', '快速处理或委托', 0.14),
    ]
    for rx, ry, rw, rh, color, label, action, alpha in rects:
        ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor=color, alpha=alpha,
                               edgecolor='#3c2a36', lw=1))
        ax.text(rx + 0.22, ry + rh - 0.32, label, fontsize=10.5, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(rx + 0.22, ry + rh - 0.62, action, fontsize=8.2, color=DIM,
                ha='left', va='center')

    # 轴
    ax.annotate('', xy=(x1 + 0.35, y0), xytext=(x0 - 0.35, y0),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.6))
    ax.annotate('', xy=(x0, y1 + 0.35), xytext=(x0, y0 - 0.35),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.6))
    ax.text((x0 + x1) / 2, y0 - 0.55, '紧急度（剩余时间 · 是否阻塞他人）',
            fontsize=9.2, color=DIM, ha='center', va='center')
    ax.text(x0 - 0.52, (y0 + y1) / 2, '重要度（优先级 · 影响面 · 金额）',
            fontsize=9.2, color=DIM, ha='center', va='center', rotation=90)

    # 任务卡
    tasks = [
        (9.55, 5.02, '线上支付故障', 'P0 · 阻塞收款', ROSE),
        (9.55, 4.30, '客户周五验收', 'P1 · 剩余 3 天', ROSE),
        (3.55, 5.02, '季度架构评审', 'P1 · 无截止日期', GOLD),
        (3.55, 4.30, '技术债清理', 'P2 · 影响迭代速度', GOLD),
        (9.55, 2.55, '群里的临时询问', 'P3 · 5 分钟能答', SKY),
        (3.55, 2.55, '周报模板美化', 'P3 · 没人看', '#8b7a85'),
    ]
    for tx, ty, name, note, color in tasks:
        w, h = 2.55, 0.72
        ax.add_patch(FancyBboxPatch((tx - w / 2, ty - h / 2), w, h,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=CARD, edgecolor=color, linewidth=1.3))
        ax.text(tx - w / 2 + 0.18, ty + 0.14, name, fontsize=8.6, fontweight='bold',
                color=TEXT, ha='left', va='center')
        ax.text(tx - w / 2 + 0.18, ty - 0.16, note, fontsize=7.3, color=color,
                ha='left', va='center')

    save(fig, 'quadrant.png')


# ── 3：多平台归一 ───────────────────────────────────────────────────────────
def draw_aggregate():
    fig, ax = plt.subplots(figsize=(13, 7.2), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.2); ax.axis('off')

    ax.text(6.5, 6.8, '四个平台，最后只剩一张任务池', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.35, '字段名不同、状态码不同，先归一才有可比性', fontsize=12,
            color=DIM, ha='center')

    sources = [
        ('禅道', 'GET /api.php?m=my&f=work', GOLD, 'pri: 1–4'),
        ('Jira', 'GET /rest/api/3/search?jql', SKY, 'priority: P1–P5'),
        ('PingCode', 'GET /v1/project/work_items', JADE, 'priority_id: 1–4'),
        ('阿里云效', 'GET /devops/tasks/my', LILAC, 'priority: 高/中/低'),
    ]

    y = 5.45
    for name, api_path, color, note in sources:
        ax.add_patch(FancyBboxPatch((0.5, y - 0.5), 3.5, 0.95,
                                    boxstyle='round,pad=0.03,rounding_size=0.1',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.4))
        ax.text(0.72, y + 0.22, name, fontsize=10.5, fontweight='bold',
                color=color, ha='left', va='center')
        ax.text(0.72, y - 0.12, api_path, fontsize=6.8, color=DIM,
                ha='left', va='center')
        ax.text(3.75, y - 0.12, note, fontsize=6.6, color=color,
                ha='right', va='center')
        y -= 1.12

    ax.annotate('', xy=(4.15, 3.55), xytext=(4.05, 3.55),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))

    # 中间：统一对象
    ax.add_patch(FancyBboxPatch((4.25, 1.35), 3.35, 4.5,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=JADE, linewidth=1.6))
    ax.text(4.48, 5.55, '统一任务对象', fontsize=10.5, fontweight='bold',
            color=JADE, ha='left', va='center')
    fields = [
        ('id', '平台:单号（唯一键）', TEXT),
        ('title', '需求标题', TEXT),
        ('priority', '归一为 P0–P3', GOLD),
        ('due', '截止时间（含时区）', SKY),
        ('status', 'todo / doing / blocked', JADE),
        ('impact', '影响人数 / 金额', LILAC),
    ]
    fy = 5.15
    for k, v, color in fields:
        ax.text(4.48, fy, k, fontsize=8.2, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(5.5, fy, v, fontsize=7.8, color=TEXT, ha='left', va='center')
        fy -= 0.56

    ax.add_patch(FancyBboxPatch((4.45, 1.55), 2.95, 0.5,
                                boxstyle='round,pad=0.02,rounding_size=0.08',
                                facecolor=CARD, edgecolor=DIM, linewidth=1))
    ax.text(5.92, 1.8, '去重：同单跨平台只留一条', fontsize=7.4, color=DIM,
            ha='center', va='center')

    ax.annotate('', xy=(7.95, 3.55), xytext=(7.75, 3.55),
                arrowprops=dict(arrowstyle='->', color=DIM, lw=1.4))

    # 右侧：两个坐标
    ax.add_patch(FancyBboxPatch((8.0, 1.35), 4.5, 4.5,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=ROSE, linewidth=1.6))
    ax.text(8.25, 5.55, '两个坐标，各自算', fontsize=10.5, fontweight='bold',
            color=ROSE, ha='left', va='center')

    ax.text(8.25, 5.05, '重要度', fontsize=9.2, fontweight='bold', color=GOLD, ha='left')
    ax.text(8.25, 4.72, '0.5 × 优先级 + 0.3 × 影响面\n+ 0.2 × 金额量级', fontsize=7.8,
            color=TEXT, ha='left', va='top', linespacing=1.6)
    ax.text(8.25, 3.98, '紧急度', fontsize=9.2, fontweight='bold', color=SKY, ha='left')
    ax.text(8.25, 3.65, '0.6 × 剩余天数倒数 + 0.4 × 阻塞人数\n（已逾期直接封顶 100）', fontsize=7.8,
            color=TEXT, ha='left', va='top', linespacing=1.6)

    ax.add_patch(FancyBboxPatch((8.25, 1.95), 3.95, 0.85,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=CARD, edgecolor=GOLD, linewidth=1))
    ax.text(8.45, 2.57, '例：PAY-3412', fontsize=7.6, color=DIM, ha='left')
    ax.text(8.45, 2.30, '重要 86 · 紧急 91 → 第一象限', fontsize=8.2,
            fontweight='bold', color=ROSE, ha='left')

    ax.text(6.5, 0.62, '分数不是给别人看的，是给「今天先做哪件」找一个可解释的依据',
            fontsize=9.2, color=DIM, ha='center', va='center')

    save(fig, 'aggregate.png')


# ── 4：日报 ─────────────────────────────────────────────────────────────────
def draw_report():
    fig, ax = plt.subplots(figsize=(13, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6.5, 7.4, '日报不是流水账，是三个问题的答案', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6.5, 6.95, '今天交付了什么 · 明天承诺什么 · 有什么需要领导拍板', fontsize=12,
            color=DIM, ha='center')

    # 左：日报卡
    ax.add_patch(FancyBboxPatch((0.5, 0.7), 7.55, 5.85,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=JADE, linewidth=1.8))
    ax.text(0.85, 6.2, '张明 · 2026-11-04 · 支付组', fontsize=11.5, fontweight='bold',
            color=TEXT, ha='left', va='center')
    ax.text(0.85, 5.88, '数据来源：禅道 · Jira · PingCode · 云效 · GitLab', fontsize=7.8,
            color=DIM, ha='left', va='center')
    ax.plot([0.85, 7.7], [5.7, 5.7], color='#3c2a36', lw=1)

    sections = [
        ('今日完成', JADE, 'PAY-3412 分账回归通过（48 用例全绿）· 支付超时告警阈值调整上线'),
        ('进行中', SKY, '退款异步改造 60%，卡在消息幂等 · 商户资质校验联调，等待第三方回包'),
        ('风险 / 阻塞', ROSE, '第三方支付证书 11-15 到期未续 · 测试库容量告警，需 DBA 扩盘'),
        ('明日计划', GOLD, '完成退款异步改造 · 评审分账二期方案 · 输出对账差异周报'),
    ]
    y = 5.35
    for label, color, content in sections:
        ax.add_patch(FancyBboxPatch((0.85, y - 0.17), 0.14, 0.34,
                                    boxstyle='round,pad=0.02,rounding_size=0.05',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.12, y + 0.04, label, fontsize=9.2, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(1.12, y - 0.36, content, fontsize=8.0, color=TEXT, ha='left',
                va='top', wrap=True)
        y -= 1.18

    # 右：领导只看三样
    ax.add_patch(FancyBboxPatch((8.35, 0.7), 4.15, 5.85,
                                boxstyle='round,pad=0.05,rounding_size=0.14',
                                facecolor=PANEL, edgecolor=ROSE, linewidth=1.8))
    ax.text(8.62, 6.2, '领导实际只看三样', fontsize=10.5, fontweight='bold',
            color=ROSE, ha='left', va='center')

    stats = [
        ('5', '今日关闭', '有验收记录才算', JADE),
        ('2', '风险项', '需要跨部门协调', ROSE),
        ('1', '待拍板', '方案二选一', GOLD),
    ]
    y = 5.55
    for num, label, note, color in stats:
        ax.text(8.65, y + 0.12, num, fontsize=30, fontweight='bold', color=color,
                ha='left', va='center')
        ax.text(9.55, y + 0.3, label, fontsize=9.5, fontweight='bold', color=TEXT,
                ha='left', va='center')
        ax.text(9.55, y - 0.02, note, fontsize=7.6, color=DIM, ha='left', va='center')
        y -= 1.28

    ax.text(8.65, 1.60, '口径写死：\n完成 = 状态关闭 + 有验收记录\n风险必须带「需要谁做什么」',
            fontsize=7.8, color=DIM, ha='left', va='top', linespacing=1.7)

    save(fig, 'report.png')


if __name__ == '__main__':
    draw_flow()
    draw_quadrant()
    draw_aggregate()
    draw_report()
    print('✓ 全部生成完毕')
