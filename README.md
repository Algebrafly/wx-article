# wx-article

微信公众号推文仓库。文章默认面向「想把 AI / Hermes Agent 用进业务和团队日常」的读者。

## 主题分组

**Hermes Agent 主线** — 围绕 Hermes Agent（Nous Research 出品）在实际业务中的各种用法。

```
hermes-alert-kb/              生产告警 + 企业知识库方案
hermes-bi-dashboard/         只读账号自动生成 BI 看板
hermes-messaging-setup/      群消息推送基础设施
hermes-issue-auto-bridge/    业务群 → 工单自动建单桥
hermes-code-to-knowledge/     代码库转知识库
hermes-enterprise-knowledge/  企业知识库搭建
hermes-cron-daily-brief/     每日定时简报
hermes-quadrant-daily/       每日四象限巡检
hermes-auto-testing/         自动化测试 agent
hermes-prd-prototype/        PRD → 原型
hermes-a2a-sdlc/             A2A + SDLC 多 agent 协作
hermes-agent/                Hermes Agent 产品介绍
```

**Hermes 项目管理十大领域系列** — 把 PMBOK 十大领域逐个拆开，结合 Hermes 落地。

```
hermes-project-management/   十大领域整体框架
hermes-scope-management/     范围管理
hermes-schedule-management/  进度管理（PERT / CPM / 关键路径漂移）
hermes-cost-management/      成本管理（估算精度 / EVM 挣值）
hermes-quality-management/   质量管理（COQ / 1-10-100 / 控制图）
hermes-resource-management/  资源管理
hermes-risk-management/      风险管理
hermes-communication-management/ 沟通管理
hermes-procurement-management/ 采购管理
hermes-stakeholder-management/ 干系人管理
hermes-integration-management/ 整合管理（九篇串起来）
```

**AI native SDLC / Super Agent 架构** — 多 agent 协作、harness、域模型。

```
hermes-ai-native-sdlc/       AI native SDLC 多智能体接力 + 四道人工闸口
ai-native-sdlc/              AI native SDLC 控制面与数据面
deer-flow-super-agent/       读 DeerFlow 2.0：什么是 super agent harness
dsh-superagent/              读 dsh-superagent：DeepSeek 给你的一份域模型
affaan-ecc/                  ECC（Everything Claude Code）agent harness OS
ruvnet-ruflo/               Ruflo：模型 + 基座解耦
mcp-a2a-e2e/                 MCP + A2A + 单 agent E2E
mcp-evolution-2026/          MCP 从 Function Calling 到通用连接层
omnibase-mcp-opencode/       TypeScript agent + Go sidecar 解耦
openspec-intro/              OpenSpec：变更五步走，规格自动更新
superpowers-intro/           Superpowers：从一句话到一次合并的七道关
superpowers-vs-openspec/     Superpowers vs OpenSpec 对比
```

**Agent 工程实践** — testing、browser、security、plugin。

```
playwright-e2e/              Playwright E2E Browser/Context/Page 三层
browserskill-testing/        Browser Skill 端到端测试
cloudflare-security-audit/   Cloudflare 六阶段安全审计流水线
comet-plugin-intro/          Comet plugin 介绍
artisan-sdlc-console/        内部原型：SDLC 控制台
```

**Prompt 与模型能力** — 阿里云百炼三篇姊妹篇 + gpt-image-2。

```
aliyun-prompt-guide/         百炼文生文 Prompt 指南（2026-10 更新）
aliyun-text-to-image-prompt/ 百炼文生图 Prompt 指南
aliyun-text-to-video-prompt/ 百炼文生视频 Prompt 指南
gpt-image-2-prompts/         OpenAI gpt-image-2：长提示词跟随 + 图中文字
token-saving-tools/          省 token 的实用工具
```

**外部产品与仓库导读**

```
mattpocock-agent-skills/     读 mattpocock/skills 仓库
tencent-weknora/             腾讯 WeKnora 企业知识库
```

### 按目录名字母序（便于 git grep）

```
affaan-ecc/
ai-native-sdlc/
aliyun-prompt-guide/
aliyun-text-to-image-prompt/
aliyun-text-to-video-prompt/
artisan-sdlc-console/
browserskill-testing/
cloudflare-security-audit/
comet-plugin-intro/
deer-flow-super-agent/
dsh-superagent/
gpt-image-2-prompts/
hermes-a2a-sdlc/
hermes-agent/
hermes-ai-native-sdlc/
hermes-alert-kb/
hermes-auto-testing/
hermes-bi-dashboard/
hermes-code-to-knowledge/
hermes-communication-management/
hermes-cost-management/
hermes-cron-daily-brief/
hermes-enterprise-knowledge/
hermes-integration-management/
hermes-issue-auto-bridge/
hermes-messaging-setup/
hermes-prd-prototype/
hermes-procurement-management/
hermes-project-management/
hermes-quadrant-daily/
hermes-quality-management/
hermes-resource-management/
hermes-risk-management/
hermes-schedule-management/
hermes-scope-management/
hermes-stakeholder-management/
mattpocock-agent-skills/
mcp-a2a-e2e/
mcp-evolution-2026/
omnibase-mcp-opencode/
openspec-intro/
playwright-e2e/
ruvnet-ruflo/
superpowers-intro/
superpowers-vs-openspec/
tencent-weknora/
token-saving-tools/
```

## 每篇目录结构

```
<slug>/
├── body.html           正文（全部行内 style，公众号粘贴即留）
├── generate_assets.py  matplotlib 配图脚本（Agg 后端，中文字体 Noto Sans CJK SC）
├── index.html          注入模板后的预览页（浏览器直接打开）
├── publish.py          可选——微信公众号 API 直发脚本
└── assets/             配图 PNG（dpi=160，圆角卡片，零 emoji / monospace 中文）
```

少数目录还带 `playbook.pdf` / `playbook.txt`（如 `ai-native-sdlc/`），是正文附赠的配套材料。

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
