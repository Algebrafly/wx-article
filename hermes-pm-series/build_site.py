#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把十一篇推文打成一个可发布到 GitHub Pages 的静态站点"""
import os
import re
import shutil

SRC = '/workspace'
OUT = '/workspace/hermes-pm-site'

ARTICLES = [
    ('hermes-project-management', '01', '整体框架', '把项目经理拆成三层来配', '#22d3ee', '框架与 Profile'),
    ('hermes-scope-management', '02', '范围管理', '把范围写成事实', '#fb7185', '需求跟踪矩阵'),
    ('hermes-schedule-management', '03', '进度管理', '估得准，盯得早', '#34d399', 'PERT 与 CPM'),
    ('hermes-cost-management', '04', '成本管理', '花得值不值', '#e8b04b', 'EVM 与 EAC'),
    ('hermes-quality-management', '05', '质量管理', '把「算不算完成」钉死', '#f472b6', 'COQ 与控制图'),
    ('hermes-resource-management', '06', '资源管理', '人不是可分配的单位', '#a3e635', '负荷与产能'),
    ('hermes-communication-management', '07', '沟通管理', '把没说出口的放到台面上', '#60a5fa', '沟通漏斗'),
    ('hermes-risk-management', '08', '风险管理', '登记册为什么会死', '#fbbf24', '5×5 矩阵'),
    ('hermes-procurement-management', '09', '采购管理', '合同就是一张风险分配表', '#f97316', '合同风险谱'),
    ('hermes-stakeholder-management', '10', '干系人管理', '名单之外的人才是变量', '#c084fc', '四象限与信号'),
    ('hermes-integration-management', '11', '整合管理', '十个领域打架时听谁的', '#2dd4bf', '变更分级与收尾'),
]

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0;}
body{
  background:#0d1117;color:#e6edf3;
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  -webkit-font-smoothing:antialiased;
}
a{color:inherit;text-decoration:none;}
.wrap{max-width:820px;margin:0 auto;padding:0 22px 90px;}
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:22px 0 26px;font-size:13px;color:#8b98a8;gap:14px;flex-wrap:wrap;
}
.topbar a{color:#8b98a8;transition:color .18s;}
.topbar a:hover{color:#22d3ee;}
.topbar .mid{font-weight:700;letter-spacing:.5px;}
.paper{
  background:#ffffff;border-radius:16px;
  padding:46px 46px 52px;
  box-shadow:0 20px 60px rgba(0,0,0,.45);
}
.paper .art-head{border-bottom:1px solid #e6eaf0;padding-bottom:26px;margin-bottom:30px;}
.paper .art-kicker{font-size:12px;font-weight:700;letter-spacing:2px;margin-bottom:12px;}
.paper .art-title{font-size:27px;line-height:1.45;color:#161b22;font-weight:800;}
.paper .art-meta{margin-top:14px;font-size:13px;color:#7c8798;}
.pager{display:flex;gap:14px;margin-top:34px;}
.pager a{
  flex:1;background:#1c2430;border:1px solid #2d3846;border-radius:12px;
  padding:16px 18px;transition:border-color .18s,background .18s,transform .18s;
}
.pager a:hover{transform:translateY(-2px);background:#222c3c;}
.pager .lab{font-size:11px;color:#8b98a8;letter-spacing:1px;}
.pager .nm{font-size:15px;font-weight:700;margin-top:6px;}
.pager .right{text-align:right;}
footer{margin-top:46px;text-align:center;font-size:12.5px;color:#5f6d7e;line-height:2;}
@media(max-width:640px){
  .paper{padding:30px 20px 36px;border-radius:12px;}
  .paper .art-title{font-size:22px;}
  .pager{flex-direction:column;}
}
"""


def page(title, body, css_extra=''):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{BASE_CSS}{css_extra}</style>
</head>
<body>
{body}
</body>
</html>
"""


def build_article(idx, slug, num, name, tag, color, out, body_html, total):
    prev_i = (idx - 1) % total
    next_i = (idx + 1) % total
    p = ARTICLES[prev_i]
    n = ARTICLES[next_i]

    pager = (
        '<div class="pager">'
        f'<a href="../{p[0]}/index.html"><div class="lab">← 上一篇</div>'
        f'<div class="nm">{p[1]} {p[2]}</div></a>'
        f'<a class="right" href="../{n[0]}/index.html"><div class="lab">下一篇 →</div>'
        f'<div class="nm">{n[1]} {n[2]}</div></a>'
        '</div>'
    )

    body = f"""<div class="wrap">
  <div class="topbar">
    <a href="../index.html">← 系列目录</a>
    <span class="mid" style="color:{color}">{num} / {total:02d} · {name}</span>
    <a href="../index.html">用 Hermes 做项目管理</a>
  </div>

  <article class="paper">
    <div class="art-head">
      <div class="art-kicker" style="color:{color}">HERMES · 项目管理 · {num}</div>
      <h1 class="art-title">{tag}</h1>
      <div class="art-meta">{name} · 关键产出：{out} · 系列共 {total} 篇</div>
    </div>
    {body_html}
  </article>

  {pager}

  <footer>
    用 Hermes 做项目管理 · 系列第 {num} 篇<br/>
    输入 · 技术 · 输出 → 文档模板 → 组织过程资产 → 群消息格式
  </footer>
</div>"""

    title = f'{tag} · {name} | 用 Hermes 做项目管理'
    return page(title, body)


def build_index():
    cards = []
    for slug, num, name, tag, color, out in ARTICLES:
        cards.append(f"""    <a class="item" href="{slug}/index.html" style="--c:{color}">
      <div class="no">{num}</div>
      <div class="name">{name}</div>
      <div class="tag">{tag}</div>
      <div class="out">{out}</div>
    </a>""")

    css_extra = """
.hero{text-align:center;margin-bottom:8px;}
.hero img{width:100%;border-radius:14px;display:block;}
.hero h1{font-size:34px;letter-spacing:.5px;margin:38px 0 12px;color:#e6edf3;}
.hero p{color:#22d3ee;font-size:15px;letter-spacing:1px;}
.hero .sub{color:#8b98a8;font-size:14px;margin-top:16px;letter-spacing:0;line-height:1.9;}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:46px;}
.item{
  display:block;background:#1c2430;border:1px solid #2d3846;border-radius:12px;
  padding:20px 22px 18px;position:relative;overflow:hidden;
  transition:transform .18s ease,border-color .18s ease,background .18s ease;
}
.item::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--c);}
.item:hover{transform:translateY(-3px);border-color:var(--c);background:#222c3c;}
.item .no{font-size:12px;font-weight:700;color:var(--c);letter-spacing:1px;}
.item .name{font-size:17px;font-weight:700;margin:6px 0 8px;}
.item .tag{font-size:13px;color:#a8b6c6;line-height:1.6;}
.item .out{margin-top:12px;font-size:12px;color:var(--c);opacity:.85;}
.toc{margin-top:64px;}
.toc img{width:100%;border-radius:14px;display:block;}
.note{margin-top:40px;padding:20px 22px;border-left:3px solid #fbbf24;background:#161b22;
  border-radius:0 10px 10px 0;font-size:14px;color:#c2cfdc;line-height:1.95;}
.note b{color:#fbbf24;}
"""

    body = f"""<div class="wrap">
  <div class="hero">
    <img src="assets/series-cover.png" alt="用 Hermes 做项目管理 · 系列封面">
    <h1>用 Hermes 做项目管理</h1>
    <p>十大领域 · 十一篇 · 一套可落地的 SKILL</p>
    <p class="sub">每一篇都是同一个结构：过程 ITTO → 两到三个重点 → 文档模板<br/>→ 组织过程资产 → 群消息格式 → 边界</p>
  </div>

  <div class="list">
{chr(10).join(cards)}
  </div>

  <div class="toc">
    <img src="assets/series-toc.png" alt="系列目录页">
  </div>

  <div class="note">
    <b>整个系列的共同前提</b>：统一主键、统一口径、统一模板。不是为了整齐好看，是为了让十个领域的数字能互相对上——进度说完成 40%、成本说花了 45%、质量说缺陷翻倍，单看每一条都是汇报，放在一起才是判断。
  </div>

  <footer>
    共 11 篇 · 每篇 5 张配图 · 均为同一结构<br/>
    Hermes · Project Management Series
  </footer>
</div>"""

    return page('用 Hermes 做项目管理 · 系列目录', body, css_extra)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)

    # 系列配图
    for f in ('series-cover.png', 'series-toc.png'):
        shutil.copy(os.path.join(SRC, 'hermes-pm-series', 'assets', f),
                    os.path.join(OUT, 'assets', f))

    total = len(ARTICLES)
    for i, (slug, num, name, tag, color, out) in enumerate(ARTICLES):
        src_dir = os.path.join(SRC, slug)
        body_path = os.path.join(src_dir, 'body.html')
        if not os.path.exists(body_path):
            print(f'!! 缺少 {body_path}')
            continue
        with open(body_path, encoding='utf-8') as fh:
            body_html = fh.read()

        dst_dir = os.path.join(OUT, slug)
        os.makedirs(dst_dir, exist_ok=True)
        # 配图
        src_assets = os.path.join(src_dir, 'assets')
        if os.path.isdir(src_assets):
            shutil.copytree(src_assets, os.path.join(dst_dir, 'assets'), dirs_exist_ok=True)

        html = build_article(i, slug, num, name, tag, color, out, body_html, total)
        with open(os.path.join(dst_dir, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(html)
        print(f'✓ {num} {name}')

    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(build_index())
    print('✓ index.html')

    # GitHub Pages 配置
    open(os.path.join(OUT, '.nojekyll'), 'w').close()

    readme = """# 用 Hermes 做项目管理（十一篇合集）

一套把项目管理十大领域拆成可落地 SKILL 的系列文章，共 11 篇，结构统一：
过程 ITTO → 两到三个重点 → 文档模板 → 组织过程资产 → 群消息格式 → 边界。

## 目录

| # | 领域 | 主题 | 关键产出 |
|---|------|------|----------|
"""
    for slug, num, name, tag, color, out in ARTICLES:
        readme += f'| {num} | {name} | {tag} | {out} |\n'

    readme += """
## 发布到 GitHub Pages

```bash
git init
git add .
git commit -m "Hermes 项目管理系列 · 十一篇"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后在仓库 **Settings → Pages** 里，把 Source 设为 `Deploy from a branch`，
分支选 `main`、目录选 `/ (root)`，保存后等待一分钟即可访问：

```
https://<你的用户名>.github.io/<仓库名>/
```

## 说明

- 纯静态站点，无构建步骤、无外部依赖
- `index.html` 为系列封面与目录
- 每个子目录是一篇独立文章，图片在各篇 `assets/` 下
- `.nojekyll` 用于跳过 Jekyll 处理，保证目录结构原样访问
"""
    with open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8') as fh:
        fh.write(readme)
    print('✓ README.md / .nojekyll')


if __name__ == '__main__':
    main()
