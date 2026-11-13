#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mattpocock/skills 推文 API 直发脚本（代理出口 IP 轮换，重试直到命中白名单）"""
import json
import os
import sys
import time
import urllib.request
import mimetypes

APPID = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")
WORK_DIR = "/workspace/mattpocock-agent-skills"
TITLE = "AI 写代码为什么总翻车，这套开源 Skills 给了四个解法"
AUTHOR = "TraeWork"
DIGEST = "Matt Pocock 把自己每天在用的智能体技能开源了。27 个 skill，治的是 AI 编程的四个老毛病，从对齐需求一直管到代码审查。"
CONTENT_SOURCE_URL = "https://github.com/mattpocock/skills"
THUMB_NAME = "banner.png"
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
            "content": content, "content_source_url": CONTENT_SOURCE_URL,
            "thumb_media_id": thumb["media_id"],
            "need_open_comment": 1, "only_fans_can_comment": 0,
        }]}
    ), "draft")
    print(f"✅ 草稿 media_id = {draft['media_id']}")

    print("⑤ 提交发布 …")
    pub = retry(lambda: api_post_json(
        f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}",
        {"media_id": draft["media_id"]}
    ), "publish")
    print("发布返回:", pub)
    if pub.get("errcode") == 0:
        print(f"🎉 已提交发布，publish_id = {pub.get('publish_id')}")
    else:
        print("⚠️ 发布接口未成功（订阅号通常仅支持到草稿），请到后台手动发布。")
    print("\n========== 完成 ==========")


if __name__ == "__main__":
    main()
