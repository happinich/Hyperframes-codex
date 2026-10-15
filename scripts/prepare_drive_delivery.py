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


def sha256_file(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def includes_longform(policy: dict) -> bool:
    included = "longform_mp4" in policy.get("include", [])
    if included and "longform_mp4" in policy.get("exclude", []):
        raise ValueError("Conflicting long-form MP4 delivery policy")
    return included


def longform_source(project: Path) -> Path:
    source = project / "06_delivery/youtube" / f"{project.name}-youtube.mp4"
    if not source.is_file() or source.stat().st_size == 0:
        raise FileNotFoundError(f"Missing completed long-form main video: {source}")
    return source


def portable_main_links(html: str, main_name: str) -> str:
    html = re.sub(r'(\b(?:src|href)=")\.\./\.\./06_delivery/youtube/([^\"]+)(")',
                  r'\1\2\3', html)
    parser = Links()
    parser.feed(html)
    if main_name not in parser.paths:
        link = f'<p><a href="{main_name}">롱폼 메인 영상 MP4</a></p>'
        html = html.replace("</body>", link + "</body>") if "</body>" in html else html + link
    return html


def external_caption_delivery(project: Path) -> bool:
    """Use the project decision, falling back to the current delivery default."""
    profile = project / "06_delivery/profile.json"
    if profile.is_file():
        data = json.loads(profile.read_text())
        if "external_caption_files_delivery" in data:
            return bool(data["external_caption_files_delivery"])
        # Legacy project profiles predate the automatic-caption preference.
        # New projects record their policy explicitly in the template.
        return True
    rules = json.loads((ROOT / "config/success-rules.json").read_text())
    return bool(rules["defaults"]["subtitles"].get("external_files_delivery", True))


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
    include_main = includes_longform(policy)
    main_source = longform_source(project) if include_main else None
    captions = external_caption_delivery(project)
    required = {"longform-publish.md", "longform-publish.html", "thumbnail-a.png", "thumbnail-b.png", "README.md"}
    if captions:
        required.update({"longform-captions.srt", "longform-captions.vtt"})
    allowed_videos = set()
    if main_source:
        allowed_videos.add(main_source.name)
    for i, short in enumerate(shorts, 1):
        sid = short.get("short_id", f"shorts-{i:02}")
        stem = f"{project.name}-{sid}"
        required.add(f"{stem}.mp4")
        if captions:
            required.update({f"{stem}.{ext}" for ext in ("srt", "vtt")})
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
        if not captions and path.suffix.lower() in {".srt", ".vtt"}:
            raise ValueError("External captions are excluded by this project's delivery policy")
        if path.suffix == ".mp4" and name not in allowed_videos:
            raise ValueError("Only the final main video and final Shorts MP4s may be uploaded")
        digest = sha256_file(path)
        if name != "delivery-manifest.json":
            entry = next(e for e in entries if e["filename"] == name)
            if path.stat().st_size != entry["bytes"] or digest != entry["sha256"]:
                raise ValueError(f"Delivery file changed after packaging: {name}")
        if path.suffix == ".html":
            parser = Links(); parser.feed(path.read_text())
            for target in parser.paths:
                if target.startswith(("https://", "http://", "data:", "#")):
                    continue
                if main_source and target == main_source.name:
                    continue
                if target not in actual:
                    raise ValueError(f"Broken portable link in {name}: {target}")
        files.append({"name": name, "path": str(path), "bytes": path.stat().st_size, "sha256": digest})

    # Validate the authored package before adding the required main video.
    # Its original entries must still match the approved local files.
    if main_source:
        target = output / main_source.name
        if target.exists():
            if target.stat().st_size != main_source.stat().st_size or sha256_file(target) != sha256_file(main_source):
                raise ValueError("Packaged main video differs from the final master")
        else:
            shutil.copy2(main_source, target)
        readme_path = output / "README.md"
        readme = readme_path.read_text()
        for old in (
            "본편 MP4는 로컬 제작 폴더에 보관합니다.",
            "롱폼 MP4는 로컬에 보관하며 이 Drive 전달 폴더에는 포함하지 않았습니다.",
        ):
            readme = readme.replace(old, "")
        if main_source.name not in readme:
            readme += f"\n롱폼 메인 영상: {main_source.name}\n"
        readme_path.write_text(readme)
        html_path = output / "longform-publish.html"
        html_path.write_text(portable_main_links(html_path.read_text(), main_source.name))
        package["longform_mp4_included"] = True
        if "longform_video_included" in package:
            package["longform_video_included"] = True
        package["files"] = [
            {"filename": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(output.iterdir())
            if path.is_file() and path.name != "delivery-manifest.json"
        ]
        (output / "delivery-manifest.json").write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n")
        files = [{"name": path.name, "path": str(path), "bytes": path.stat().st_size,
                  "sha256": sha256_file(path)} for path in sorted(output.iterdir()) if path.is_file()]
    manifest = {"project_id": project.name, "destination": policy["folder_url"],
                "remote_subfolder_name": project.name, "status": "prepared_not_uploaded",
                "longform_video_included": include_main, "external_caption_files_included": captions,
                "shorts_count": len(shorts), "files": files}
    (publish / "drive-delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def prepare(project: Path) -> dict:
    project = project.resolve()
    if project.parent != ROOT / "projects":
        raise ValueError("Use a project directly under this workspace's projects/.")
    policy = json.loads((ROOT / "config/success-rules.json").read_text())["publishing_rules"]["google_drive_delivery"]
    if not policy["enabled"]:
        raise ValueError("Drive delivery must be enabled.")
    include_main = includes_longform(policy)
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
    }
    if include_main:
        main_source = longform_source(project)
        sources[main_source.name] = main_source
    captions = external_caption_delivery(project)
    if captions:
        sources.update({f"{prefix}.{ext}": project / f"03_sync/{prefix}.{ext}"
                        for prefix in ("captions", "shorts-captions") for ext in ("srt", "vtt")})
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
            if not captions:
                html = re.sub(r'<a\b[^>]*href="[^\"]*\.(?:srt|vtt)"[^>]*>.*?</a>', "", html, flags=re.S | re.I)
            if name.startswith("youtube"):
                if include_main:
                    html = portable_main_links(html, main_source.name)
                else:
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
        + ("본편 및 쇼츠 업로드용 자막: captions / shorts-captions의 SRT와 VTT\n\n" if captions
         else "YouTube 자동 자막 사용. 외부 SRT/VTT는 납품·업로드하지 않습니다.\n\n")
        + "HTML 복사 버튼과 미리보기는 이 폴더 전체를 내려받아 같은 폴더에서 여세요.\n"
        + (f"롱폼 메인 영상: {main_source.name}\n" if include_main
           else "롱폼 영상은 Google Drive 전달 대상에서 제외했습니다.\n")
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
    allowed_videos = {shorts_name}
    if include_main:
        allowed_videos.add(main_source.name)
    for path in sorted(output.iterdir()):
        if path.suffix == ".mp4" and path.name not in allowed_videos:
            raise ValueError("Only the final main video and final Shorts MP4s may be uploaded.")
        files.append({"name": path.name, "path": str(path), "bytes": path.stat().st_size,
                      "sha256": sha256_file(path)})
    manifest = {"project_id": project.name, "destination": policy["folder_url"],
                "remote_subfolder_name": project.name, "status": "prepared_not_uploaded",
                "longform_video_included": include_main, "external_caption_files_included": captions, "files": files}
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
