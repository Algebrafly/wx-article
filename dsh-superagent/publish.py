# -*- coding: utf-8 -*-
import os, re, sys, json, time, uuid, mimetypes, urllib.request

APPID = os.environ.get("WX_APPID", "")
APPSECRET = os.environ.get("WX_APPSECRET", "")
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
BODY = os.path.join(WORK_DIR, "body.html")
TITLE = "读 dsh-superagent：一份写好的域模型"
AUTHOR = "TraeWork"
DIGEST = "DeepSeek 开源 super agent prototype 的哲学、域模型、Ticket 状态机与授权路径。"
THUMB_NAME = "domain.png"
PROXY = "http://127.0.0.1:18080"
MAX_RETRY = 80

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))

def http(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with opener.open(req, timeout=60) as r:
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
    boundary = "----WX" + uuid.uuid4().hex
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    filename = os.path.basename(path)
    with open(path, "rb") as f:
        content = f.read()
    parts = []
    parts.append(("--" + boundary).encode())
    parts.append(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"'.encode())
    parts.append(f"Content-Type: {mime}".encode())
    parts.append(b"")
    parts.append(content)
    parts.append(("--" + boundary + "--").encode())
    parts.append(b"")
    return b"\r\n".join(parts), f"multipart/form-data; boundary={boundary}"

def upload_body_image(token, path):
    body, ct = multipart(path)
    url = ("https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=" + token)
    return http(url, data=body, headers={"Content-Type": ct})

def upload_material(token, path):
    body, ct = multipart(path)
    url = ("https://api.weixin.qq.com/cgi-bin/material/add_material?access_token="
           + token + "&type=image")
    return http(url, data=body, headers={"Content-Type": ct})

def main():
    print("1) 获取 access_token")
    token_res = retry(
        lambda: http("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
                     f"&appid={APPID}&secret={APPSECRET}"),
        "token")
    token = token_res.get("access_token")
    if not token:
        print("❌ 获取 token 失败:", token_res)
        sys.exit(1)
    print("   ok")

    html = open(BODY, encoding="utf-8").read()
    imgs = re.findall(r'src="(assets/[^"]+)"', html)
    print(f"2) 上传正文图片 {len(imgs)} 张")
    for rel in imgs:
        abs_path = os.path.join(WORK_DIR, rel)
        res = retry(lambda p=abs_path: upload_body_image(token, p), "body-img")
        wx_url = res.get("url")
        if not wx_url:
            print("❌ 正文图上传失败:", rel, res)
            sys.exit(1)
        html = html.replace(f'src="{rel}"', f'src="{wx_url}"')
        print("   ok", rel)

    print("3) 上传封面")
    thumb_path = os.path.join(WORK_DIR, "assets", THUMB_NAME)
    mat = retry(lambda: upload_material(token, thumb_path), "thumb")
    thumb_id = mat.get("media_id")
    if not thumb_id:
        print("❌ 封面上传失败:", mat)
        sys.exit(1)
    print("   ok", thumb_id)

    print("4) 创建草稿")
    article = {
        "title": TITLE,
        "author": AUTHOR,
        "digest": DIGEST,
        "content": html,
        "thumb_media_id": thumb_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8")
    draft = retry(
        lambda: http("https://api.weixin.qq.com/cgi-bin/draft/add?access_token=" + token,
                     data=payload, headers={"Content-Type": "application/json"}),
        "draft")
    media_id = draft.get("media_id")
    if not media_id:
        print("❌ 草稿创建失败:", draft)
        sys.exit(1)

    print("✅ 推送成功")
    print("   media_id:", media_id)

if __name__ == "__main__":
    main()
