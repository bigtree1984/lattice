"""Lattice ビューアーのローカルサーバー。

使い方: python3 viewer/server.py [ポート]（Windows は py viewer\\server.py。Python 3.9 以上）
  既定のポート: 8796。subjects/ の下のフォルダが、それぞれ1つの Subject。

- /                         Subject を選ぶ画面（subjects.html）
- /index.html?s=<Subject>   その Subject のビューアー
- /subjects.json            Subject の一覧（名前・Facet 数・Discussion 数）
- /s/<Subject>/bundle.json  その Subject の .md を、その場でまとめて返す（作り直しの手間をなくす）
- /s/<Subject>/bundle/<パス>  Subject の中のファイル（PDF・画像などの実物）をそのまま返す
- POST /api/open            {"subject": "...", "path": "/discussions/…", "mode": "app" | "reveal"}
                            既定のアプリで開く／フォルダで表示する（Mac は Finder、Windows はエクスプローラー）
- POST /api/focus           {"subject": "...", "label": "...", "paths": ["/facets/…", …]}
                            ビューアーで今見ているものを .lattice/focus.md に書く。Claude は「これ」と言われたらここを読む

安全のため:
- 127.0.0.1 にだけ bind する（自分の PC からしか届かない）。
- /api/* は、同じオリジン（このサーバーのページ）からの POST だけ受ける。他のサイトのページからは呼べない。
- 開けるのは subjects/ の中の、Subject のフォルダの中のファイルだけ。
"""
import json
import mimetypes
import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

from build_bundle_json import build

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SUBJECTS = ROOT / "subjects"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8796
FOCUS = ROOT / ".lattice" / "focus.md"
ORIGINS = {f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"}


def open_file(p, mode):
    """OS ごとの「既定のアプリで開く」「フォルダで表示（ファイルを選んだ状態）」。"""
    if sys.platform == "darwin":
        subprocess.run(["open", "-R", str(p)] if mode == "reveal" else ["open", str(p)], check=False)
    elif sys.platform == "win32":
        if mode == "reveal":
            subprocess.run(["explorer", f"/select,{p}"], check=False)
        else:
            os.startfile(p)
    else:  # Linux など。ファイルを選んだ状態にする共通の方法が無いので、フォルダを開く
        subprocess.run(["xdg-open", str(p.parent if mode == "reveal" else p)], check=False)


def subject_dir(name):
    """subjects/ 直下の Subject のフォルダ。名前に / や .. を含むもの、隠しフォルダ、index.md の無いものは受けない。"""
    name = str(name or "")
    if not name or name.startswith(".") or "/" in name or "\\" in name:
        return None
    d = (SUBJECTS / name).resolve()
    return d if d.is_dir() and (d / "index.md").is_file() else None


def in_subject(subject, rel):
    d = subject_dir(subject)
    if not d:
        return None
    p = (d / rel.lstrip("/")).resolve()
    return p if p.is_file() and p.is_relative_to(d) else None


def list_subjects():
    out = []
    for d in sorted(SUBJECTS.iterdir()) if SUBJECTS.is_dir() else []:
        if not subject_dir(d.name):
            continue
        title = next((l[2:].strip() for l in (d / "index.md").read_text(encoding="utf-8").splitlines()
                      if l.startswith("# ")), d.name)
        fdef = d / "facets.md"
        facets = len(re.findall(r"\{\s*id:", fdef.read_text(encoding="utf-8"))) if fdef.is_file() else 0
        discussions = len(list(d.glob("discussions/*/discussion_summary.md")))
        out.append({"id": d.name, "title": title, "facets": facets, "discussions": discussions})
    return out


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(HERE), **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = unquote(self.path.split("?")[0])
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/subjects.html")
            self.end_headers()
            return
        if path == "/subjects.json":
            return self.send_json(200, list_subjects())
        m = re.match(r"^/s/([^/]+)/(bundle\.json|bundle/.+)$", path)
        if m:
            subject, rest = m.groups()
            if rest == "bundle.json":
                d = subject_dir(subject)
                return self.send_json(200, build(d)) if d else self.send_error(404)
            p = in_subject(subject, rest[len("bundle"):])
            if not p:
                return self.send_error(404)
            data = p.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(p.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        return super().do_GET()

    def do_POST(self):
        if self.path not in ("/api/open", "/api/focus"):
            return self.send_error(404)
        if self.headers.get("Origin") not in ORIGINS:
            return self.send_json(403, {"error": "origin"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        except ValueError:
            return self.send_json(400, {"error": "json"})
        if self.path == "/api/focus":
            return self.write_focus(req)
        p = in_subject(req.get("subject"), str(req.get("path", "")))
        mode = req.get("mode")
        if not p or mode not in ("app", "reveal"):
            return self.send_json(400, {"error": "path or mode"})
        open_file(p, mode)
        return self.send_json(200, {"ok": True})

    def write_focus(self, req):
        subject = req.get("subject")
        paths = [p for p in (in_subject(subject, str(x)) for x in req.get("paths", [])[:5]) if p]
        if not paths:
            return self.send_json(400, {"error": "paths"})
        label = str(req.get("label", ""))[:200].replace("\n", " ")
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        lines = ["# ビューアーで今見ているもの", "",
                 f"- 更新: {now}", f"- Subject: {subject}", f"- 見ているもの: {label}",
                 "- ファイル（上ほど手前に開いているもの）:"]
        lines += [f"  - @{p.relative_to(ROOT.resolve()).as_posix()}" for p in paths]
        FOCUS.parent.mkdir(exist_ok=True)
        FOCUS.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return self.send_json(200, {"ok": True})


if __name__ == "__main__":
    print(f"subjects: {SUBJECTS}\nhttp://127.0.0.1:{PORT}/")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
