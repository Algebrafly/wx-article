#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenSpec 推文 API 直发脚本（代理出口 IP 轮换，重试直到命中白名单）—— 仅创建草稿"""
import json
import os
import sys
import time
import urllib.request
import mimetypes

APPID = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")
WORK_DIR = "/workspace/openspec-intro"
TITLE = "总让 AI 理解偏需求？OpenSpec 把需求变成一个文件夹"
AUTHOR = "TraeWork"
DIGEST = "一个变更走五步，规格随代码一起长大。附四个能直接照做的示例，以及它和 Spec Kit、Kiro 的取舍。"
THUMB_NAME = "loop.png"
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
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
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
    req = urllib.request.Request(url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_thumb(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    body, boundary = multipart(path)
    req = urllib.request.Request(url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    print("① 获取 access_token …")
    tk = retry(lambda: api_get(
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    ), "token")
    token = tk["access_token"]
    print(f"✅ access_token = {token[:12]}…")

    with open(os.path.join(WORK_DIR, "body.html"), "r", encoding="utf-8") as f:
        content = f.read()

    assets = os.path.join(WORK_DIR, "assets")
    images = sorted(f for f in os.listdir(assets) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    print(f"② 上传 {len(images)} 张正文图片 …")
    for img in images:
        res = retry(lambda p=os.path.join(assets, img): upload_body_image(token, p), f"upload:{img}")
        content = content.replace(f"assets/{img}", res["url"])
        print(f"   ✅ {img}")

    if "assets/" in content:
        print("⚠️ 仍有未替换的本地图片引用。")

    print(f"③ 上传封面素材（{THUMB_NAME}）…")
    thumb = retry(lambda: upload_thumb(token, os.path.join(assets, THUMB_NAME)), "thumb")
    print(f"✅ 封面 media_id = {thumb['media_id']}")

    print("④ 创建草稿 …")
    draft = retry(lambda: api_post_json(
        f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
        {"articles": [{
            "title": TITLE, "author": AUTHOR, "digest": DIGEST,
            "content": content, "thumb_media_id": thumb["media_id"],
            "need_open_comment": 1, "only_fans_can_comment": 0,
        }]}
    ), "draft")
    print(f"✅ 草稿 media_id = {draft['media_id']}")
    print("\n========== 完成：请到公众号后台草稿箱手动发表 ==========")


if __name__ == "__main__":
    main()
