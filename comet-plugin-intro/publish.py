#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comet 推文 API 直发脚本
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
WORK_DIR = "/workspace/comet-plugin-intro"
TITLE = "AI 能写代码，却管不住长任务。这个开源工具补上了后半程"
AUTHOR = "Comet"
DIGEST = "Comet 是一个面向 Coding 的可恢复长程任务工作流与 Skill 平台，中断后能接着跑，并用 Rubric、Pass@k、Pass^k 评估 Skill。"
CONTENT_SOURCE_URL = "https://github.com/rpamis/comet"
THUMB_NAME = "cover-comet.png"
PROXY = "http://127.0.0.1:18080"
MAX_RETRY = 80

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


def multipart(fields_file, field_name="media"):
    filename = os.path.basename(fields_file)
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    with open(fields_file, "rb") as f:
        filedata = f.read()
    boundary = "----WebKitFormBoundary" + os.urandom(8).hex()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode("utf-8") + filedata + f"\r\n--{boundary}--\r\n".encode("utf-8")
    return body, boundary


def upload_body_image(token, filepath):
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    body, boundary = multipart(filepath)
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def upload_thumb(token, filepath):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    body, boundary = multipart(filepath)
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    # 1. token
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

    # 3. 上传正文图片到微信 CDN 并替换
    assets_dir = os.path.join(WORK_DIR, "assets")
    images = sorted(f for f in os.listdir(assets_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")))
    print(f"② 上传 {len(images)} 张正文图片 …")
    for img in images:
        local_path = os.path.join(assets_dir, img)
        res = retry(lambda p=local_path: upload_body_image(token, p), f"upload:{img}")
        wx_url = res["url"]
        content = content.replace(f"assets/{img}", wx_url)
        print(f"   ✅ {img} -> {wx_url[:50]}…")

    if "assets/" in content:
        print("⚠️ 仍有未替换的本地图片引用，请检查。")

    # 4. 封面素材
    print(f"③ 上传封面素材（{THUMB_NAME}）…")
    thumb_path = os.path.join(assets_dir, THUMB_NAME)
    thumb_res = retry(lambda: upload_thumb(token, thumb_path), "thumb")
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

    # 6. 提交发布
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
