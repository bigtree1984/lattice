"""Subject の .md を1つの JSON にまとめる（ビューアー用）。

使い方: python3 viewer/build_bundle_json.py subjects/edible-coffee bundle.json

荷札（frontmatter）は生の YAML 文字列のまま入れる。server.py は build() を呼んで、その場で返す。解析はビューアー側（js-yaml）で行う。
"""
import json
import pathlib
import sys


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return "", text


def visible(p, root):
    """隠しファイル・隠しフォルダ（Subject 自身の .git など）は載せない。"""
    return not any(x.startswith(".") for x in p.relative_to(root).parts)


def build(bundle_dir):
    root = pathlib.Path(bundle_dir)
    files = []
    for p in sorted(x for x in root.rglob("*.md") if visible(x, root)):
        frontmatter, body = split_frontmatter(p.read_text(encoding="utf-8"))
        files.append({
            "path": "/" + p.relative_to(root).as_posix(),
            "frontmatter": frontmatter,
            "body": body,
        })
    # .md 以外の実物（PDF・Excel など）は、パスだけ載せる。中身は /s/<Subject>/bundle/<パス> で取る
    assets = ["/" + p.relative_to(root).as_posix() for p in sorted(root.rglob("*"))
              if p.is_file() and p.suffix != ".md" and visible(p, root)]
    return {"bundle": root.name, "files": files, "assets": assets}


def main(bundle_dir, out_path):
    data = build(bundle_dir)
    files = data["files"]
    pathlib.Path(out_path).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(files)} files -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
