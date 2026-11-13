#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""omnibase-mcp + OpenCode 推文 API 直发（代理出口 IP 轮换重试）"""
import json
import os
import re
import sys
import time
import urllib.request
import mimetypes

APPID = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
TITLE = "omnibase-mcp：一个 MCP server 接 50+ 数据库，我拿 OpenCode 搭了一套"
AUTHOR = "TraeWork"
DIGEST = (
    "omnibase-mcp 把数据库接进 MCP，OpenCode 当客户端。"
    "两层解耦、三层权限、自定义工具写进 YAML，"
    "不用再给 Agent 单独装数据库客户端。"
)
THUMB_NAME = "arch.png"
PROXY = "http://127.0.0.1:18080"
MAX_RETRY = 80

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
)


def api_get(url):
    with opener.open(urllib.request.Request(url), timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def api_post_json(url, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}
    )
    with opener.open(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def retry(fn, label):
    for i in range(1, MAX_RETRY + 1):
        try:
            res = fn()
            if isinstance(res, dict) and res.get("errcode") == 40164:
                print(f"  [{label}] 第 {i} 次 IP 未命中白名单，重试…")
                time.sleep(1.2)
                continue
            return res
        except Exception as e:
            print(f"  [{label}] 第 {i} 次异常: {e}，重试…")
            time.sleep(1.2)
    print(f"❌ [{label}] 超过最大重试次数，放弃。")
    sys.exit(1)


def multipart(path, field_name="media"):
    filename = os.path.basename(path)
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        filedata = f.read()
    boundary = "----WebKitFormBoundary" + os.urandom(8).hex()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode("utf-8") + filedata + f"\r\n--{boundary}--\r\n".encode("utf-8")
    return body, boundary


def upload_body_image(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    body, boundary = multipart(path)
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_thumb(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    body, boundary = multipart(path)
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


IMG_RE = re.compile(r'src="(assets/[^"]+)"')


def main():
    print("① 获取 access_token …")
    tk = retry(lambda: api_get(
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
        f"&appid={APPID}&secret={APPSECRET}"
    ), "token")
    token = tk["access_token"]
    print(f"✅ access_token = {token[:12]}…")

    body_path = os.path.join(WORK_DIR, "body.html")
    with open(body_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 从正文解析出所有本地图片引用
    local_imgs = sorted(set(IMG_RE.findall(content)))
    print(f"② 上传 {len(local_imgs)} 张正文图片 …")
    for rel in local_imgs:
        full = os.path.join(WORK_DIR, rel)
        res = retry(lambda p=full: upload_body_image(token, p), f"upload:{rel}")
        content = content.replace(f'src="{rel}"', f'src="{res["url"]}"')
        print(f"   ✅ {rel}")

    remaining = IMG_RE.findall(content)
    if remaining:
        print(f"⚠️ 仍有未替换的本地引用: {remaining}")

    assets_dir = os.path.join(WORK_DIR, "assets")
    thumb_path = os.path.join(assets_dir, THUMB_NAME)
    print(f"③ 上传封面素材（{THUMB_NAME}）…")
    thumb = retry(lambda: upload_thumb(token, thumb_path), "thumb")
    print(f"✅ 封面 media_id = {thumb['media_id']}")

    print("④ 创建草稿 …")
    draft = retry(lambda: api_post_json(
        f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
        {"articles": [{
            "title": TITLE,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": content,
            "thumb_media_id": thumb["media_id"],
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
        }]},
    ), "draft")

    if "media_id" not in draft:
        print(f"❌ 创建草稿失败: {draft}")
        sys.exit(1)

    media_id = draft["media_id"]
    print(f"✅ 草稿 media_id = {media_id}")

    print("\n" + "=" * 60)
    print("🎉 草稿推送成功")
    print(f"   media_id : {media_id}")
    print(f"   标题     : {TITLE}")
    print(f"   封面     : {THUMB_NAME}  (thumb_media_id={thumb['media_id']})")
    print(f"   本地预览 : {os.path.join(WORK_DIR, 'index.html')}")
    print("👉 请到公众号后台「草稿箱」查看并发布")
    print("=" * 60)


if __name__ == "__main__":
    main()
