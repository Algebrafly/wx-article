#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager

font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0f1419'
PANEL = '#171f26'
CARD = '#212b34'
TEXT = '#eaf0f4'
DIM = '#8b9aa6'
TEAL = '#2dd4bf'
PURPLE = '#a78bfa'
AMBER = '#f5b544'
CORAL = '#f87171'
BLUE = '#60a5fa'
GREEN = '#86efac'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=160, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：四个过程 ────────────────────────────────────────────────────────
def draw_pipeline():
    fig, ax = plt.subplots(figsize=(13, 6.0), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.0)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 5.62, '干系人管理有四个过程，但真正难的是第一个', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.28, '名单漏了人，后面所有策略都是对着空气做的',
            fontsize=11.5, color=DIM, ha='center')

    procs = [
        ('01', '识别干系人', '找全', TEAL,
         ['章程 · 商业文件', '项目管理计划 · 协议'],
         ['问卷 · 头脑风暴', '干系人分析 · 会议'],
         ['干系人登记册'],
         ['名单之外的人', '往往才是变量']),
        ('02', '规划参与', '定策略', BLUE,
         ['章程 · 项目管理计划', '干系人登记册'],
         ['专家判断 · 数据收集', '决策 · 数据表现'],
         ['干系人参与计划'],
         ['写期望状态', '不写现状打分']),
        ('03', '管理参与', '促参与', PURPLE,
         ['参与计划 · 沟通计划', '变更日志 · 问题日志'],
         ['沟通方法 · 人际技能', '谈判 · 冲突管理'],
         ['变更请求', '计划与文件更新'],
         ['动作只有三类', '沟通 谈判 冲突']),
        ('04', '监督参与', '验效果', AMBER,
         ['项目管理计划', '问题日志 · 参与计划'],
         ['数据分析 · 决策', '数据表现 · 沟通技能'],
         ['工作绩效信息', '变更请求'],
         ['看行为数据', '不看口头表态']),
    ]

    cw, gap = 3.02, 0.20
    x0 = (13 - (4 * cw + 3 * gap)) / 2
    for i, (num, name, verb, c, ins, techs, outs, keys) in enumerate(procs):
        x = x0 + i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, 0.72), cw, 4.20,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=CARD, edgecolor=c + '55', linewidth=1.4))
        ax.add_patch(FancyBboxPatch((x, 4.28), cw, 0.64,
                                    boxstyle='round,pad=0.04,rounding_size=0.12',
                                    facecolor=c, edgecolor=c, linewidth=0))
        ax.text(x + 0.22, 4.60, num, fontsize=12, fontweight='bold',
                color='#0f1419', ha='left', va='center')
        ax.text(x + 0.64, 4.60, name, fontsize=9.2, fontweight='bold',
                color='#0f1419', ha='left', va='center')
        ax.text(x + cw - 0.20, 4.60, verb, fontsize=6.8,
                color='#0f1419', ha='right', va='center', alpha=0.7)

        blocks = [('输入', ins, TEAL, 4.06, [3.80, 3.54]),
                  ('技术', techs, PURPLE, 3.16, [2.90, 2.64]),
                  ('输出', outs, AMBER, 2.24, [1.98, 1.72])]
        for label, lines, lc, ly, ys in blocks:
            ax.text(x + 0.22, ly, label, fontsize=6.8, fontweight='bold',
                    color=lc, ha='left', va='center')
            for txt, yy in zip(lines, ys):
                ax.text(x + 0.22, yy, txt, fontsize=6.5, color='#bfccd6',
                        ha='left', va='center')

        ax.plot([x + 0.22, x + cw - 0.22], [1.48, 1.48], color='#33414c', lw=0.8)
        for j, k in enumerate(keys):
            ax.text(x + 0.22, 1.24 - j * 0.26, k, fontsize=6.5,
                    color=c, ha='left', va='center')

    ax.text(6.5, 0.40, '第 2 到第 4 个过程的质量，完全取决于第 1 个过程漏没漏人',
            fontsize=7.6, color=DIM, ha='center', va='center')
    save(fig, 'pipeline.png')


# ── 2：权力 / 利益四象限 ───────────────────────────────────────────────
def draw_power():
    fig, ax = plt.subplots(figsize=(13, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.8)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 6.42, '谁是关键人物，一张四象限就够了', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.08, '纵轴是权力，横轴是利益 —— 位置决定你要多久找他一次',
            fontsize=11.5, color=DIM, ha='center')

    gx0, gx1 = 2.42, 10.72
    gy0, gy1 = 1.02, 5.28
    mx, my = (gx0 + gx1) / 2, (gy0 + gy1) / 2

    ax.plot([mx, mx], [gy0, gy1], color='#3b4852', lw=1.2, linestyle='--')
    ax.plot([gx0, gx1], [my, my], color='#3b4852', lw=1.2, linestyle='--')

    quads = [
        (gx0, my, mx - gx0, gy1 - my, AMBER, '保持满意', 'Keep Satisfied',
         ['权力大、利益小', '定期汇报结论，不给细节', '别让他从别人嘴里听说'],
         ['分管副总', '财务总监']),
        (mx, my, gx1 - mx, gy1 - my, CORAL, '重点管理', 'Manage Closely',
         ['权力大、利益大', '高频沟通，拉进决策', '这一步没有捷径'],
         ['项目发起人', '业务负责人']),
        (gx0, gy0, mx - gx0, my - gy0, DIM, '监督即可', 'Monitor',
         ['权力小、利益小', '低成本维护，公告覆盖', '不要主动制造接触'],
         ['周边团队', '外部观察者']),
        (mx, gy0, gx1 - mx, my - gy0, TEAL, '随时告知', 'Keep Informed',
         ['权力小、利益大', '及时同步，收集反馈', '他们常常是最早发现问题的人'],
         ['一线使用者', '测试与运维']),
    ]

    for (qx, qy, qw, qh, c, name, en, lines, examples) in quads:
        ax.add_patch(FancyBboxPatch((qx + 0.06, qy + 0.06), qw - 0.12, qh - 0.12,
                                    boxstyle='round,pad=0.02,rounding_size=0.10',
                                    facecolor=CARD, edgecolor=c + '55', linewidth=1.4))
        ax.text(qx + 0.28, qy + qh - 0.30, name, fontsize=11.5, fontweight='bold',
                color=c, ha='left', va='center')
        ax.text(qx + 0.28, qy + qh - 0.58, en, fontsize=6.6, color=DIM,
                ha='left', va='center', fontfamily='monospace')
        for j, ln in enumerate(lines):
            ax.text(qx + 0.28, qy + qh - 0.90 - j * 0.26, ln, fontsize=7.0,
                    color='#c8d3dc' if j < 2 else DIM, ha='left', va='center')
        ax.text(qx + 0.28, qy + 0.26, ' · '.join(examples), fontsize=6.6,
                color=c, ha='left', va='center', alpha=0.9)

    ax.text((gx0 + gx1) / 2, gy0 - 0.34, '利益（低 → 高）', fontsize=7.6,
            color=DIM, ha='center', va='center')
    ax.text(gx0 - 0.30, (gy0 + gy1) / 2, '权力（低 → 高）', fontsize=7.6,
            color=DIM, rotation=90, ha='center', va='center')

    ax.text(6.5, 0.42, '位置会变：项目阶段一换，很多人的权力和利益都会移动 —— 所以这张图每季度要重画',
            fontsize=7.6, color=DIM, ha='center', va='center')
    save(fig, 'power.png')


# ── 3：参与度评估矩阵 ──────────────────────────────────────────────────
def draw_engagement():
    fig, ax = plt.subplots(figsize=(13, 6.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.4)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 6.05, '参与度要画成「从哪到哪」，不是打一个分', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.72, '空心是现状，实心是期望，中间的箭头就是你的工作量',
            fontsize=11.5, color=DIM, ha='center')

    levels = ['不知晓', '抵制', '中立', '支持', '领导']
    lx0, lstep, lw = 3.02, 1.46, 1.34

    for i, lv in enumerate(levels):
        x = lx0 + i * lstep
        ax.add_patch(FancyBboxPatch((x, 4.86), lw, 0.34,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor='#2b3742', edgecolor='#3b4852', linewidth=0))
        ax.text(x + lw / 2, 5.03, lv, fontsize=7.4, color='#c8d3dc',
                ha='center', va='center')

    rows = [
        ('项目发起人', 2, 4, CORAL, '高'),
        ('业务负责人', 3, 4, CORAL, '高'),
        ('财务总监', 2, 3, AMBER, '中'),
        ('研发组长', 3, 3, AMBER, '中'),
        ('一线使用者', 1, 3, TEAL, '中'),
        ('运维团队', 0, 2, DIM, '低'),
    ]

    for j, (name, cur, des, c, pri) in enumerate(rows):
        y = 4.30 - j * 0.66
        ax.add_patch(FancyBboxPatch((0.42, y - 0.24), 2.42, 0.48,
                                    boxstyle='round,pad=0.02,rounding_size=0.06',
                                    facecolor=CARD, edgecolor=c + '44', linewidth=1.0))
        ax.text(0.60, y + 0.02, name, fontsize=7.4, color=TEXT, ha='left', va='center')
        ax.text(2.66, y + 0.02, pri, fontsize=6.6, color=c, ha='right', va='center')

        for i in range(5):
            if min(cur, des) <= i <= max(cur, des):
                continue
            x = lx0 + i * lstep + lw / 2
            ax.add_patch(plt.Circle((x, y), 0.065, facecolor='none',
                                    edgecolor='#33414c', linewidth=0.9))
        xc = lx0 + cur * lstep + lw / 2
        xd = lx0 + des * lstep + lw / 2
        ax.add_patch(plt.Circle((xc, y), 0.085, facecolor=BG, edgecolor=c,
                                linewidth=1.8, zorder=4))
        ax.add_patch(plt.Circle((xd, y), 0.085, facecolor=c, edgecolor=c,
                                linewidth=1.8, zorder=4))
        if des != cur:
            ax.add_patch(FancyArrowPatch((xc + 0.14, y), (xd - 0.14, y),
                                         arrowstyle='-|>', mutation_scale=9,
                                         color=c, linewidth=1.2, alpha=0.75, zorder=3))
        elif des == cur:
            ax.text(xd, y, '', fontsize=1)

    ax.text(0.60, 0.56, '现状 = 期望的行（如研发组长）不需要动作，有箭头的才是要投入的',
            fontsize=7.0, color=DIM, ha='left', va='center')
    ax.text(11.28, 4.80, '箭头越长', fontsize=7.0, color=DIM, ha='left', va='center')
    ax.text(11.28, 4.52, '越要先做', fontsize=7.0, color=CORAL, ha='left', va='center',
            fontweight='bold')
    ax.text(11.28, 4.12, '一次跨两级', fontsize=7.0, color=DIM, ha='left', va='center')
    ax.text(11.28, 3.84, '基本做不到', fontsize=7.0, color=AMBER, ha='left', va='center')
    ax.text(11.28, 3.44, '拆成两轮', fontsize=7.0, color=DIM, ha='left', va='center')
    ax.text(11.28, 3.16, '先到中立', fontsize=7.0, color=DIM, ha='left', va='center')

    save(fig, 'engagement.png')


# ── 4：参与度信号监测 ──────────────────────────────────────────────────
def draw_signal():
    fig, ax = plt.subplots(figsize=(13, 6.4), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 6.4)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 6.05, '参与度会掉，而且掉之前一定有信号', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 5.72, '不看态度，看四个能被系统记录的行为',
            fontsize=11.5, color=DIM, ha='center')

    # 左：参与度指数趋势
    ax.add_patch(FancyBboxPatch((0.42, 0.62), 7.10, 4.80,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=TEAL + '88', linewidth=1.4))
    ax.text(0.72, 5.10, '关键干系人参与度指数 · 近 8 周', fontsize=9.0,
            fontweight='bold', color=TEAL, ha='left', va='center')

    gx0, gx1 = 1.62, 7.16
    gy0, gy1 = 1.36, 4.66

    def mx(i):
        return gx0 + i / 7.0 * (gx1 - gx0)

    def my(v):
        return gy0 + (v - 30.0) / 60.0 * (gy1 - gy0)

    for v in [30, 45, 60, 75, 90]:
        ax.plot([gx0, gx1], [my(v), my(v)], color='#2b3742', lw=0.7, zorder=1)
        ax.text(gx0 - 0.10, my(v), str(v), fontsize=6.4, color=DIM, ha='right', va='center')

    ax.plot([gx0, gx1], [my(60), my(60)], color=CORAL, lw=1.4,
            linestyle='--', alpha=0.8, zorder=2)
    ax.text(gx0 + 0.06, my(60) + 0.15, '警戒线 60', fontsize=6.6, color=CORAL,
            ha='left', va='bottom')

    vals = [82, 84, 80, 76, 71, 67, 61, 54]
    ax.plot([mx(i) for i in range(8)], [my(v) for v in vals], color=TEAL,
            lw=2.2, zorder=3)
    for i, v in enumerate(vals):
        ax.scatter([mx(i)], [my(v)], s=26, color=BG, edgecolor=TEAL, linewidth=1.6, zorder=4)
    ax.scatter([mx(7)], [my(54)], s=46, color=CORAL, edgecolor=CORAL, linewidth=1.6, zorder=5)
    ax.text(mx(7) - 0.06, my(54) - 0.26, '本周越线', fontsize=6.8, color=CORAL,
            fontweight='bold', ha='right', va='top')

    for i in range(8):
        ax.text(mx(i), gy0 - 0.20, f'W{36 + i}', fontsize=6.0, color=DIM,
                ha='center', va='center')

    ax.text(0.72, 0.84, '指数 = 出席率 30% + 响应时效 25% + 承诺兑现 30% + 主动提议 15%',
            fontsize=6.6, color=DIM, ha='left', va='center')

    # 右：四个信号
    ax.add_patch(FancyBboxPatch((7.72, 0.62), 4.86, 4.80,
                                boxstyle='round,pad=0.05,rounding_size=0.12',
                                facecolor=PANEL, edgecolor=AMBER + '88', linewidth=1.4))
    ax.text(8.02, 5.10, '四个信号', fontsize=9.0, fontweight='bold',
            color=AMBER, ha='left', va='center')

    signals = [('会议出席率', '62%', '连续三周缺席评审会', CORAL),
               ('平均响应时长', '18h', '从 4h 涨到 18h', CORAL),
               ('承诺兑现率', '70%', '答应的事有一半没下文', AMBER),
               ('主动提议数', '1', '从每周 4 条降到 1 条', AMBER)]
    for i, (name, val, note, c) in enumerate(signals):
        y = 4.56 - i * 0.92
        ax.add_patch(FancyBboxPatch((8.00, y - 0.66), 4.30, 0.78,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=CARD, edgecolor=c + '44', linewidth=1.0))
        ax.text(8.16, y - 0.06, name, fontsize=6.9, color='#c8d3dc', ha='left', va='center')
        ax.text(12.14, y - 0.06, val, fontsize=9.2, fontweight='bold', color=c,
                ha='right', va='center')
        ax.text(8.16, y - 0.42, note, fontsize=6.2, color=DIM, ha='left', va='center')

    ax.text(8.02, 0.86, '三个信号同时变差 = 不是忙，是撤了', fontsize=7.0,
            color=DIM, ha='left', va='center')
    save(fig, 'signal.png')


# ── 5：四类群消息 ──────────────────────────────────────────────────────
def draw_message():
    fig, ax = plt.subplots(figsize=(13, 7.6), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 13); ax.set_ylim(0, 7.6)
    ax.autoscale(False); ax.axis('off')

    ax.text(6.5, 7.15, '干系人消息只有四类，其余都该私下说', fontsize=21,
            fontweight='bold', color=TEXT, ha='center')
    ax.text(6.5, 6.72, '让谁参与、请谁决策、谁在降温、阶段复盘',
            fontsize=11.5, color=DIM, ha='center')

    cards = [
        ('参与邀请', '拉进决策', TEAL, [
            '支付重构方案下周定稿，需要业务方确认验收口径',
            '· 涉及 3 个下游系统，改动影响面较大',
            '· 前置材料已发邮件，含两份候选方案',
            '请 @陈总 周四 15:00 参加方案评审']),
        ('决策请求', '需要拍板', CORAL, [
            '灰度范围二选一，本周必须定，否则影响上线窗口',
            '· 方案 A：全量灰度，风险高但验证快',
            '· 方案 B：10% 灰度，多花 2 周',
            '请 @王总 周三前批复，超期默认走 B']),
        ('参与度降温', '信号异常', AMBER, [
            '财务总监已连续三周缺席评审，响应时长从 4h 涨到 18h',
            '· 预算相关的两个决议因此卡住',
            '· 已私信两次，未回复',
            '请 @项目经理 本周内当面沟通一次']),
        ('阶段复盘', '关系盘点', BLUE, [
            '本阶段干系人变化：新增 2 人，退出 1 人，2 人降级',
            '· 运维团队从「中立」升到「支持」',
            '· 合规部新提异议 3 条，已排期',
            '请 @全员 周五前确认新的四象限定位']),
    ]

    cw, ch = 6.06, 2.42
    for i, (title, tag, c, lines) in enumerate(cards):
        col, row = i % 2, i // 2
        x = 0.42 + col * (cw + 0.20)
        y = 3.90 - row * (ch + 0.22)
        ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=CARD, edgecolor=c + '66', linewidth=1.4))
        ax.add_patch(FancyBboxPatch((x + 0.24, y + ch - 0.62), 1.62, 0.40,
                                    boxstyle='round,pad=0.02,rounding_size=0.08',
                                    facecolor=c, edgecolor=c, linewidth=0))
        ax.text(x + 0.33, y + ch - 0.42, title, fontsize=8.0, fontweight='bold',
                color='#0f1419', ha='left', va='center')
        ax.text(x + 2.00, y + ch - 0.42, tag, fontsize=6.6, color=DIM,
                ha='left', va='center')

        for j, ln in enumerate(lines):
            ax.text(x + 0.30, y + ch - 0.98 - j * 0.42, ln, fontsize=7.0,
                    color='#eaf0f4' if j == 0 else '#bfccd6',
                    fontweight='bold' if j == 0 else 'normal',
                    ha='left', va='center')

    ax.text(6.5, 0.72, '涉及评价某个人的内容，一律不进群 —— 进群就变成了公开表态',
            fontsize=8.2, color=CORAL, ha='center', va='center')
    save(fig, 'message.png')


if __name__ == '__main__':
    draw_pipeline()
    draw_power()
    draw_engagement()
    draw_signal()
    draw_message()
    print('✓ 全部生成完毕')
