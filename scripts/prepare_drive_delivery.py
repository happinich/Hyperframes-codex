#!/usr/bin/env python3
"""Prepare portable publishing copies for the authorized Drive destination.

This script prepares local files only. Upload using a connected Drive tool or
the authenticated browser, then record the actual result separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths: list[str] = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"src", "href"} and value:
                self.paths.append(value)


def prepare_multi_short_delivery(project: Path, policy: dict, shorts: list[dict]) -> dict:
    """Validate an episode-specific portable package containing multiple Shorts."""
    publish = project / "07_publish"
    output = publish / "drive-upload"
    package = json.loads((output / "delivery-manifest.json").read_text())
    required = {"longform-publish.md", "longform-publish.html", "thumbnail-a.png", "thumbnail-b.png",
                "longform-captions.srt", "longform-captions.vtt", "README.md"}
    allowed_videos = set()
    for i, short in enumerate(shorts, 1):
        sid = short.get("short_id", f"shorts-{i:02}")
        stem = f"{project.name}-{sid}"
        required.update({f"{stem}.{ext}" for ext in ("mp4", "srt", "vtt")})
        required.update({f"{sid}-publish.{ext}" for ext in ("md", "html")})
        allowed_videos.add(f"{stem}.mp4")
    entries = package["files"]
    names = {entry["filename"] for entry in entries}
    if package["project_id"] != project.name or not required <= names:
        raise ValueError("Incomplete multi-Short portable package")
    if len(names) != len(entries) or any(Path(name).name != name for name in names):
        raise ValueError("Duplicate or unsafe delivery filename")
    actual = {f.name for f in output.iterdir() if f.is_file()}
    if actual != names | {"delivery-manifest.json"}:
        raise ValueError("Unexpected files in multi-Short delivery folder")
    files = []
    for name in sorted(actual):
        path = output / name
        if path.suffix == ".mp4" and name not in allowed_videos:
            raise ValueError("Only final Shorts MP4s may be uploaded")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if name != "delivery-manifest.json":
            entry = next(e for e in entries if e["filename"] == name)
            if path.stat().st_size != entry["bytes"] or digest != entry["sha256"]:
                raise ValueError(f"Delivery file changed after packaging: {name}")
        if path.suffix == ".html":
            parser = Links(); parser.feed(path.read_text())
            for target in parser.paths:
                if target.startswith(("https://", "http://", "data:", "#")):
                    continue
                if target not in actual:
                    raise ValueError(f"Broken portable link in {name}: {target}")
        files.append({"name": name, "path": str(path), "bytes": path.stat().st_size, "sha256": digest})
    manifest = {"project_id": project.name, "destination": policy["folder_url"],
                "remote_subfolder_name": project.name, "status": "prepared_not_uploaded",
                "longform_video_included": False, "shorts_count": len(shorts), "files": files}
    (publish / "drive-delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def prepare(project: Path) -> dict:
    project = project.resolve()
    if project.parent != ROOT / "projects":
        raise ValueError("Use a project directly under this workspace's projects/.")
    policy = json.loads((ROOT / "config/success-rules.json").read_text())["publishing_rules"]["google_drive_delivery"]
    if not policy["enabled"] or "longform_mp4" not in policy["exclude"]:
        raise ValueError("Drive delivery must be enabled with long-form MP4 excluded.")
    publish = project / "07_publish"
    short_metadata = publish / "shorts/shorts-publish.json"
    if short_metadata.is_file():
        shorts = json.loads(short_metadata.read_text()).get("shorts", [])
        if len(shorts) > 1:
            return prepare_multi_short_delivery(project, policy, shorts)
    shorts_name = f"{project.name}-shorts.mp4"
    sources = {
        "youtube-publish.html": publish / "youtube/youtube-publish.html",
        "youtube-publish.md": publish / "youtube/youtube-publish.md",
        "thumbnail-a.png": publish / "youtube/thumbnail-a.png",
        "thumbnail-b.png": publish / "youtube/thumbnail-b.png",
        "shorts-publish.html": publish / "shorts/shorts-publish.html",
        "shorts-publish.md": publish / "shorts/shorts-publish.md",
        shorts_name: project / f"06_delivery/shorts/{shorts_name}",
        **{f"{prefix}.{ext}": project / f"03_sync/{prefix}.{ext}"
           for prefix in ("captions", "shorts-captions") for ext in ("srt", "vtt")},
    }
    for path in sources.values():
        if not path.is_file() or path.stat().st_size == 0:
            raise FileNotFoundError(f"Missing completed deliverable: {path}")
    output = publish / "drive" / project.name
    output.mkdir(parents=True, exist_ok=True)
    expected_names = set(sources) | {"README.txt"}
    unexpected = {p.name for p in output.iterdir()} - expected_names
    if unexpected:
        raise ValueError(f"Unexpected files in delivery folder: {sorted(unexpected)}")
    for name, src in sources.items():
        dst = output / name
        if src.suffix == ".html":
            html = src.read_text()
            if name.startswith("youtube"):
                html = re.sub(r"<video\b[^>]*>.*?</video>", "", html, flags=re.S)
                html = re.sub(r'<a\b[^>]*href="[^\"]*-youtube[^\"]*\.mp4"[^>]*>.*?</a>', "", html, flags=re.S)
                html = html.replace("<h2>영상과 자막</h2>", "<h2>게시 자료와 자막</h2><p>롱폼 영상은 로컬 제작 폴더에 보관합니다.</p>")
            html = re.sub(r'(\b(?:src|href)=")\.\./\.\./(?:03_sync|06_delivery/shorts)/([^\"]+)(")', r'\1\2\3', html)
            dst.write_text(html)
        else:
            shutil.copy2(src, dst)
    (output / "README.txt").write_text(
        f"{project.name}\n\n"
        "롱폼 게시 전략: youtube-publish.md / youtube-publish.html\n"
        "썸네일: thumbnail-a.png / thumbnail-b.png\n"
        f"쇼츠 영상: {shorts_name}\n"
        "쇼츠 게시 전략: shorts-publish.md / shorts-publish.html\n"
        "본편 및 쇼츠 업로드용 자막: captions / shorts-captions의 SRT와 VTT\n\n"
        "HTML 복사 버튼과 미리보기는 이 폴더 전체를 내려받아 같은 폴더에서 여세요.\n"
        "롱폼 영상은 Google Drive 전달 대상에서 제외했습니다.\n"
    )
    for name in ("youtube-publish.html", "shorts-publish.html"):
        parser = Links()
        parser.feed((output / name).read_text())
        for target in parser.paths:
            if target.startswith(("https://", "http://", "data:", "#")):
                continue
            if target not in expected_names or not (output / target).is_file():
                raise ValueError(f"Broken delivery link in {name}: {target}")
    files = []
    for path in sorted(output.iterdir()):
        if path.suffix == ".mp4" and path.name != shorts_name:
            raise ValueError("Only the final Shorts MP4 may be uploaded.")
        files.append({"name": path.name, "path": str(path), "bytes": path.stat().st_size,
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {"project_id": project.name, "destination": policy["folder_url"],
                "remote_subfolder_name": project.name, "status": "prepared_not_uploaded",
                "longform_video_included": False, "files": files}
    (publish / "drive-delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    manifest = prepare(args.project)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
