#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager

# 强制加载 CJK 字体,覆盖 matplotlib 默认缓存
for _ in font_manager.findSystemFonts():
    pass
font_manager._load_fontmanager(try_read_cache=False)
plt.rcParams['font.family'] = ['Noto Sans CJK SC', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = '#0a1420'
PANEL = '#112240'
TEXT = '#e2e8f0'
DIM = '#64748b'
BLUE = '#38bdf8'
PURPLE = '#a5b4fc'
GREEN = '#34d399'
AMBER = '#fbbf24'
GRID = '#1e3a5f'


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=150, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


# ── 1：两条配置时间线 ───────────────────────────────────────────────────
def draw_flow():
    fig, ax = plt.subplots(figsize=(12, 7.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 7.8); ax.axis('off')

    ax.text(6, 7.3, '企业微信 vs 飞书：配置时间线', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 6.8, '两者结构几乎一模一样，核心差在权限表和连接方式', fontsize=12.5, color=DIM, ha='center')

    # 两列 header
    ax.add_patch(FancyBboxPatch((0.55, 6.0), 5.0, 0.72,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=BLUE, edgecolor=BLUE, linewidth=0))
    ax.text(3.05, 6.36, '企业微信 WeCom', fontsize=14, fontweight='bold',
            color='#0a1420', ha='center', va='center')

    ax.add_patch(FancyBboxPatch((6.45, 6.0), 5.0, 0.72,
                                boxstyle='round,pad=0.04,rounding_size=0.1',
                                facecolor=PURPLE, edgecolor=PURPLE, linewidth=0))
    ax.text(8.95, 6.36, '飞书 Feishu / Lark', fontsize=14, fontweight='bold',
            color='#0a1420', ha='center', va='center')

    # 步骤内容
    steps_wecom = [
        ('1', '创建 AI Bot', '企业微信后台 → 应用管理 → 自建应用 → AI Bot', GREEN),
        ('2', '抄 Bot ID + Secret', '凭据页复制两个字段', GREEN),
        ('3', 'hermes gateway setup', '选 WeCom，扫码或手填', BLUE),
        ('4', 'hermes gateway 启动', 'WebSocket 长连，无需公网', BLUE),
    ]
    steps_feishu = [
        ('1', '创建自建应用', 'open.feishu.cn → 启用机器人能力', AMBER),
        ('2', '加权限 + 订阅事件', '5 个必选 scope + im.message.receive_v1', AMBER),
        ('3', 'hermes gateway setup', '选 Feishu/Lark，扫码或手填 App ID/Secret', PURPLE),
        ('4', 'hermes gateway 启动', 'WebSocket 推荐 / 可选 webhook', PURPLE),
    ]

    y = 5.05
    for (num, title, desc, color), (num2, title2, desc2, color2) in zip(steps_wecom, steps_feishu):
        # wecom cell
        ax.add_patch(FancyBboxPatch((0.55, y - 0.9), 5.0, 0.85,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=PANEL, edgecolor=color, linewidth=1.5))
        ax.text(0.75, y - 0.58, num, fontsize=11, fontweight='bold',
                color=color, ha='left')
        ax.text(1.05, y - 0.58, title, fontsize=11, fontweight='bold',
                color=TEXT, ha='left')
        ax.text(0.75, y - 0.82, desc, fontsize=8.5, color=DIM, ha='left')

        # feishu cell
        ax.add_patch(FancyBboxPatch((6.45, y - 0.9), 5.0, 0.85,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=PANEL, edgecolor=color2, linewidth=1.5))
        ax.text(6.65, y - 0.58, num2, fontsize=11, fontweight='bold',
                color=color2, ha='left')
        ax.text(6.95, y - 0.58, title2, fontsize=11, fontweight='bold',
                color=TEXT, ha='left')
        ax.text(6.65, y - 0.82, desc2, fontsize=8.5, color=DIM, ha='left')

        y -= 1.05

    save(fig, 'flow.png')


# ── 2：env 对照表 ────────────────────────────────────────────────────────
def draw_env():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.axis('off')

    ax.text(6, 6.0, '两个平台的 .env 必填字段', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.5, '写进 ~/.hermes/.env，hermes 自动加载', fontsize=12.5, color=DIM, ha='center')

    vars_wecom = [
        ('WECOM_BOT_ID', 'Bot ID', BLUE),
        ('WECOM_SECRET', 'Bot Secret', BLUE),
        ('WECOM_ALLOWED_USERS', '白名单 user_id1,user_id2（可选）', GREEN),
        ('WECOM_HOME_CHANNEL', 'cron 推送频道 chat_id（可选）', GREEN),
    ]
    vars_feishu = [
        ('FEISHU_APP_ID', 'App ID', PURPLE),
        ('FEISHU_APP_SECRET', 'App Secret', PURPLE),
        ('FEISHU_DOMAIN', 'feishu 或 lark', PURPLE),
        ('FEISHU_CONNECTION_MODE', 'websocket 或 webhook', AMBER),
    ]

    # header
    ax.add_patch(FancyBboxPatch((0.55, 4.55), 5.0, 0.58,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=BLUE, edgecolor=BLUE, linewidth=0))
    ax.text(3.05, 4.84, '企业微信', fontsize=12, fontweight='bold',
            color='#0a1420', ha='center', va='center')
    ax.add_patch(FancyBboxPatch((6.45, 4.55), 5.0, 0.58,
                                boxstyle='round,pad=0.03,rounding_size=0.08',
                                facecolor=PURPLE, edgecolor=PURPLE, linewidth=0))
    ax.text(8.95, 4.84, '飞书 / Lark', fontsize=12, fontweight='bold',
            color='#0a1420', ha='center', va='center')

    y = 3.85
    for (k1, v1, c1), (k2, v2, c2) in zip(vars_wecom, vars_feishu):
        ax.add_patch(FancyBboxPatch((0.55, y - 0.75), 5.0, 0.68,
                                    boxstyle='round,pad=0.025,rounding_size=0.07',
                                    facecolor=PANEL, edgecolor=c1, linewidth=1.2))
        ax.text(0.75, y - 0.38, k1, fontsize=9.5, fontweight='bold',
                color=c1, ha='left', fontfamily='monospace')
        ax.text(0.75, y - 0.62, v1, fontsize=8.5, color=DIM, ha='left')

        ax.add_patch(FancyBboxPatch((6.45, y - 0.75), 5.0, 0.68,
                                    boxstyle='round,pad=0.025,rounding_size=0.07',
                                    facecolor=PANEL, edgecolor=c2, linewidth=1.2))
        ax.text(6.65, y - 0.38, k2, fontsize=9.5, fontweight='bold',
                color=c2, ha='left', fontfamily='monospace')
        ax.text(6.65, y - 0.62, v2, fontsize=8.5, color=DIM, ha='left')

        y -= 0.9

    # footer removed: matplotlib CJK+Latin fallback unreliable in this env
    save(fig, 'env_vars.png')


# ── 3：差异对比 ───────────────────────────────────────────────────────────
def draw_diff():
    fig, ax = plt.subplots(figsize=(12, 6.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.axis('off')

    ax.text(6, 6.3, '两个平台的主要差异', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 5.8, '相同点：都是长连为主，扫码即配', fontsize=11.5, color=DIM, ha='center')

    diffs = [
        ('连接方式',
         '纯 WebSocket\n无需公网端点\naiohttp + httpx',
         'WebSocket 推荐\n可选 Webhook\n需配 FEISHU_ENCRYPT_KEY', BLUE),
        ('权限 / 事件',
         '无权限表\n直接开 bot 即可',
         '5 必选 scope\n订阅 im.message.receive_v1\ncard.action.trigger 回调', PURPLE),
        ('会话隔离',
         'DM / 群分别配\n每个群可单独设 allowlist',
         '默认群内按用户隔离\nconfig 改 group_sessions_per_user', GREEN),
    ]

    y = 4.75
    for label, wecom, feishu, color in diffs:
        # label badge
        ax.add_patch(FancyBboxPatch((0.55, y - 0.95), 2.0, 1.4,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=color, edgecolor=color, linewidth=0))
        ax.text(1.55, y - 0.25, label, fontsize=11, fontweight='bold',
                color='#0a1420', ha='center', va='center')
        ax.text(1.55, y - 0.6, '维度', fontsize=8, color='#0a1420', ha='center',
                alpha=0.6, va='center')

        # wecom cell
        ax.add_patch(FancyBboxPatch((2.7, y - 0.95), 4.4, 1.4,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=PANEL, edgecolor=BLUE, linewidth=1.2))
        ax.text(2.9, y - 0.25, wecom, fontsize=9.5, color=TEXT,
                ha='left', va='center', linespacing=1.5)

        # feishu cell
        ax.add_patch(FancyBboxPatch((7.3, y - 0.95), 4.15, 1.4,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor=PANEL, edgecolor=PURPLE, linewidth=1.2))
        ax.text(7.5, y - 0.25, feishu, fontsize=9.5, color=TEXT,
                ha='left', va='center', linespacing=1.5)

        y -= 1.75

    save(fig, 'diff.png')


# ── 4：启动验证 ───────────────────────────────────────────────────────────
def draw_start():
    fig, ax = plt.subplots(figsize=(12, 5.8), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, 12); ax.set_ylim(0, 5.8); ax.axis('off')

    ax.text(6, 5.3, '启动 & 验证', fontsize=22, fontweight='bold',
            color=TEXT, ha='center')
    ax.text(6, 4.8, 'hermes gateway 起一个后台服务，把两个平台同时挂上', fontsize=12.5, color=DIM, ha='center')

    # 三个代码块横排
    items = [
        ('启动 gateway',
         'hermes gateway', BLUE,
         'WebSocket 自动连\n异常自动重连'),
        ('看状态',
         'hermes gateway status', GREEN,
         '平台显示 connected / retrying'),
        ('设 home chat',
         '/set-home', AMBER,
         '在聊天里执行\n标记 cron/通知推送频道'),
    ]

    w = 3.55; gap = 0.25
    x = (12 - (w * 3 + gap * 2)) / 2
    for title, cmd, color, desc in items:
        ax.add_patch(FancyBboxPatch((x, 1.4), w, 3.0,
                                    boxstyle='round,pad=0.05,rounding_size=0.12',
                                    facecolor=PANEL, edgecolor=color, linewidth=2))
        ax.text(x + w/2, 4.0, title, fontsize=12.5, fontweight='bold',
                color=color, ha='center')
        ax.add_patch(FancyBboxPatch((x + 0.25, 3.25), w - 0.5, 0.75,
                                    boxstyle='round,pad=0.04,rounding_size=0.1',
                                    facecolor='#0a1420', edgecolor=GRID, linewidth=1))
        ax.text(x + w/2, 3.625, cmd, fontsize=10, color=TEXT, ha='center',
                va='center', fontfamily='monospace')
        ax.text(x + w/2, 2.4, desc, fontsize=9.5, color=DIM, ha='center',
                va='center', linespacing=1.5)

        x += w + gap

    ax.text(6, 0.75, '两个平台可以同时启用。',
            fontsize=10, color=DIM, ha='center', va='center', style='italic')

    save(fig, 'start.png')


if __name__ == '__main__':
    draw_flow(); draw_env(); draw_diff(); draw_start()
    print('done')
