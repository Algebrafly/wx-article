# wx-article

微信公众号推文仓库。文章默认面向「想把 AI / Hermes Agent 用进业务和团队日常」的读者。

## 目录

仓库里的每一个子目录就是一篇完整的推文，目录名即 slug。

```
hermes-alert-kb/         生产告警 + 企业知识库方案
hermes-bi-dashboard/    只读账号自动生成 BI 看板
hermes-project-management/  Hermes AI PM 十大领域框架
hermes-scope-management/   范围管理（需求跟踪 / 基线判定）
hermes-schedule-management/ 进度管理（PERT / CPM / 关键路径漂移）
hermes-cost-management/     成本管理（估算三档精度 / EVM 挣值）
hermes-quality-management/  质量管理（COQ 四象限 / 1-10-100 法则 / 控制图）
hermes-ai-native-sdlc/     AI native SDLC 多智能体接力 + 四道人工闸口
deer-flow-super-agent/     读 DeerFlow 2.0：什么是 super agent harness
dsh-superagent/            读 dsh-superagent：DeepSeek 给你的一份域模型
```

### 每篇一句摘要

| 目录 | 开头一句 |
|---|---|
| `hermes-alert-kb` | 凌晨三点半手机震了，企微群 99+ 未读，核心错误只有一条：支付服务 PostgreSQL 行锁超时。 |
| `hermes-bi-dashboard` | 早上九点有人问昨天 GMV，数据组回复：需求已收到，排期到周四。 |
| `hermes-project-management` | 项目管理有十大领域。再加上把它们串起来的整合管理。 |
| `hermes-scope-management` | 项目复盘常听到一句话：范围一直没控制住。 |
| `hermes-schedule-management` | 进度管理最容易被误解成一件事：画甘特图。第三天开始就没人看了。 |
| `hermes-cost-management` | 成本管理最常见的误解：把它当成记账。 |
| `hermes-quality-management` | 质量管理最容易被简化成一句话：测完了，没大问题。 |
| `hermes-ai-native-sdlc` | 瓶颈已经不是 agent 会不会写代码了，是它写完之后人要挨个 review、点合并、补上下文。 |
| `deer-flow-super-agent` | DeerFlow 2.0 登上 GitHub Trending 第一。它把自己重新定义成了一个 super agent harness。 |
| `dsh-superagent` | DeepSeek 把 dsh-superagent-prototype 开源了，12 天 22k star。它给你的是一份设计。 |

## 每篇目录结构

```
<slug>/
├── body.html           正文（全部行内 style，公众号粘贴即留）
├── generate_assets.py  matplotlib 配图脚本（Agg 后端，中文字体 Noto Sans CJK SC）
├── index.html          注入模板后的预览页（浏览器直接打开）
├── publish.py          可选——微信公众号 API 直发脚本
└── assets/             配图 PNG（dpi=160，圆角卡片，零 emoji / monospace 中文）
```

## 本地预览

```bash
# 1. 生成配图（可选，仓库已带成品）
cd <slug> && python3 generate_assets.py

# 2. 直接浏览器打开 index.html 预览
xdg-open index.html  # Linux
open index.html      # macOS
```

## 公众号粘贴兼容铁律（写 body.html 时必须遵守）

- 全部行内 `style=""`，禁用 `<h1>`–`<h6>`、`class=`、`<style>` 块、`display:flex`、`position:`、`@media`。
- 每个可见元素是独立顶层 `<p>`，自带全套 style，不依赖父容器。
- 章节标题统一用「款式 D」——描边几何框数字 + 撞色偏移块。
- 代码块底色 `#0a0e14 ~ #13100b`、等宽字体 `Consolas/Monaco`、`border-radius:8px`。
- 配图 `<p style="text-align:center;margin:20px 0 0;"><img src="assets/xxx.png" style="width:100%;border-radius:10px;"/></p>` + 一行图注。

## matplotlib 三条铁律（写 generate_assets.py 时必须遵守）

1. `fontfamily='monospace'` 的 `ax.text` 只能写纯 ASCII，中文会渲染成方框。
2. 禁用 emoji / 特殊符号（🔴💡🔗✕ 会 tofu），改用 `[P0]`、`- `。
3. **禁止在已 `set_xlim(0,13)` 的整图画布上用 `ax.plot` 画真实数据**（autoscale 会毁掉坐标系），必须手工 `px()`/`py()` 映射到卡片坐标。

## publish.py 安全说明

仓库里的 `publish.py` 是可选的——它负责把生成好的正文推送到公众号草稿箱。脚本从**环境变量**读取凭据：

```bash
export WX_APPID=<your-appid>
export WX_APPSECRET=<your-secret>
python3 publish.py
```

仓库里**没有任何硬编码的 AppSecret**。如果你 fork 本仓库，不需要删除任何密钥文件。

## 授权

文章内容和配图归 Algebrafly 所有。代码（`generate_assets.py` / `publish.py`）可自由复用。
