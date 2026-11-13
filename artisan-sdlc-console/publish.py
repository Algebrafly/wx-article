#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARTISAN SDLC CONSOLE 推文发布脚本
代理出口 IP 动态轮换，采用重试策略直到命中白名单 IP。
"""
import json
import os
import sys
import time
import urllib.request
import mimetypes

APPID = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")
WORK_DIR = "/workspace/artisan-sdlc-console"
TITLE = "AI 只帮你写代码就够了吗？这个控制台把 AI 铺进了研发全流程"
AUTHOR = "ARTISAN"
DIGEST = "一个把 AI 铺进需求、架构、编码、测试、发布、运维六个环节的研发协作控制台。"
CONTENT_SOURCE_URL = "https://algebrafly.github.io/ai-sdlc-console-prototypes/ai-sdlc-console/"
PROXY = "http://127.0.0.1:18080"
MAX_RETRY = 60  # 单步最大重试次数

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
)


def api_get(url):
    req = urllib.request.Request(url)
    with opener.open(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def api_post_json(url, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with opener.open(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def retry(fn, label):
    """重试直到成功或达到上限（主要应对动态 IP 白名单 40164）"""
    for i in range(1, MAX_RETRY + 1):
        try:
            res = fn()
            if isinstance(res, dict) and res.get("errcode") == 40164:
                print(f"  [{label}] 第 {i} 次 IP 未命中白名单，重试…")
                time.sleep(1.5)
                continue
            return res
        except Exception as e:
            print(f"  [{label}] 第 {i} 次异常: {e}，重试…")
            time.sleep(1.5)
    print(f"❌ [{label}] 超过最大重试次数，放弃。")
    sys.exit(1)


def upload_image(token, filepath):
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    filename = os.path.basename(filepath)
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    with open(filepath, "rb") as f:
        filedata = f.read()
    boundary = "----WebKitFormBoundary" + os.urandom(8).hex()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode("utf-8") + filedata + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    # 1. token（重试直到命中白名单 IP）
    print("① 获取 access_token …")
    tk_url = (
        f"https://api.weixin.qq.com/cgi-bin/token"
        f"?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    )
    tk = retry(lambda: api_get(tk_url), "token")
    token = tk["access_token"]
    print(f"✅ access_token = {token[:12]}…")

    # 2. 读取正文
    with open(os.path.join(WORK_DIR, "body.html"), "r", encoding="utf-8") as f:
        content = f.read()

    # 3. 上传正文图片到微信 CDN
    assets_dir = os.path.join(WORK_DIR, "assets")
    images = sorted(f for f in os.listdir(assets_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")))
    print(f"② 上传 {len(images)} 张正文图片 …")
    for img in images:
        local_path = os.path.join(assets_dir, img)
        res = retry(lambda p=local_path: upload_image(token, p), f"upload:{img}")
        wx_url = res["url"]
        content = content.replace(f"assets/{img}", wx_url)
        print(f"   ✅ {img} -> {wx_url[:55]}…")

    # 4. 封面图（永久素材）
    print("③ 上传封面素材 …")
    thumb_path = os.path.join(assets_dir, images[0])
    thumb_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

    def _upload_thumb():
        filename = os.path.basename(thumb_path)
        ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        with open(thumb_path, "rb") as f:
            filedata = f.read()
        boundary = "----WebKitFormBoundary" + os.urandom(8).hex()
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
            f"Content-Type: {ctype}\r\n\r\n"
        ).encode("utf-8") + filedata + f"\r\n--{boundary}--\r\n".encode("utf-8")
        req = urllib.request.Request(
            thumb_url, data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        with opener.open(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))

    thumb_res = retry(_upload_thumb, "thumb")
    thumb_media_id = thumb_res["media_id"]
    print(f"✅ 封面 media_id = {thumb_media_id}")

    # 5. 创建草稿
    print("④ 创建草稿 …")
    draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    draft_data = {
        "articles": [{
            "title": TITLE,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": content,
            "content_source_url": CONTENT_SOURCE_URL,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }]
    }
    draft_res = retry(lambda: api_post_json(draft_url, draft_data), "draft")
    draft_media_id = draft_res["media_id"]
    print(f"✅ 草稿 media_id = {draft_media_id}")

    # 6. 尝试发布
    print("⑤ 提交发布 …")
    pub_url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
    pub_res = retry(lambda: api_post_json(pub_url, {"media_id": draft_media_id}), "publish")
    print("发布返回:", pub_res)
    if pub_res.get("errcode") == 0:
        print(f"🎉 已提交发布，publish_id = {pub_res.get('publish_id')}")
    else:
        print("⚠️ 发布接口未成功（个人订阅号通常仅支持到草稿），请到公众号后台手动发布。")

    print("\n========== 完成 ==========")


if __name__ == "__main__":
    main()
