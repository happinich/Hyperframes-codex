import hashlib
import json

import pytest

import prepare_drive_delivery as delivery


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content if isinstance(content, bytes) else content.encode())


def setup_project(tmp_path, monkeypatch, short_count):
    monkeypatch.setattr(delivery, "ROOT", tmp_path)
    policy = {
        "enabled": True,
        "include": ["longform_mp4"],
        "exclude": ["external_srt_vtt"],
        "folder_url": "https://drive.google.com/drive/folders/test-destination",
    }
    write(tmp_path / "config/success-rules.json", json.dumps({
        "publishing_rules": {"google_drive_delivery": policy},
    }))
    project = tmp_path / "projects/test-anthology"
    write(project / "06_delivery/profile.json", json.dumps({"external_caption_files_delivery": False}))
    main_name = f"{project.name}-youtube.mp4"
    write(project / "06_delivery/youtube" / main_name, b"final-main-original-bytes")
    publish = project / "07_publish"
    if short_count == 1:
        write(publish / "youtube/youtube-publish.html",
              f'<html><body><video src="../../06_delivery/youtube/{main_name}"></video></body></html>')
        write(publish / "youtube/youtube-publish.md", "Long-form publishing strategy")
        for name in ("thumbnail-a.png", "thumbnail-b.png"):
            write(publish / "youtube" / name, b"thumbnail")
        write(publish / "shorts/shorts-publish.html", "<html><body>Shorts</body></html>")
        write(publish / "shorts/shorts-publish.md", "Shorts publishing strategy")
        write(project / f"06_delivery/shorts/{project.name}-shorts.mp4", b"final-short")
        output = publish / "drive" / project.name
    else:
        shorts = [{"short_id": f"shorts-{i:02}"} for i in range(1, short_count + 1)]
        write(publish / "shorts/shorts-publish.json", json.dumps({"shorts": shorts}))
        output = publish / "drive-upload"
        for name in ("thumbnail-a.png", "thumbnail-b.png"):
            write(output / name, b"thumbnail")
        write(output / "README.md", "본편 MP4는 로컬 제작 폴더에 보관합니다.")
        write(output / "longform-publish.md", "Long-form publishing strategy")
        write(output / "longform-publish.html", f'<html><body><a href="{main_name}">Main</a></body></html>')
        for short in shorts:
            sid = short["short_id"]
            write(output / f"{project.name}-{sid}.mp4", b"final-short")
            write(output / f"{sid}-publish.md", "Shorts publishing strategy")
            write(output / f"{sid}-publish.html", "<html><body>Shorts</body></html>")
        entries = [{"filename": f.name, "bytes": f.stat().st_size,
                    "sha256": hashlib.sha256(f.read_bytes()).hexdigest()} for f in output.iterdir()]
        write(output / "delivery-manifest.json", json.dumps({"project_id": project.name, "files": entries}))
    return project, output, main_name


@pytest.mark.parametrize("short_count", [1, 3])
def test_main_master_is_packaged_with_portable_link_and_repeatable_manifest(tmp_path, monkeypatch, short_count):
    project, output, name = setup_project(tmp_path, monkeypatch, short_count)
    manifest = delivery.prepare(project)
    assert manifest["longform_video_included"] is True
    assert manifest["external_caption_files_included"] is False
    assert (output / name).read_bytes() == b"final-main-original-bytes"
    assert len([f for f in manifest["files"] if f["name"] == name]) == 1
    main_entry = next(f for f in manifest["files"] if f["name"] == name)
    assert main_entry["sha256"] == hashlib.sha256(b"final-main-original-bytes").hexdigest()
    html_name = "youtube-publish.html" if short_count == 1 else "longform-publish.html"
    html = (output / html_name).read_text()
    assert f'="{name}"' in html
    assert "../../06_delivery/youtube/" not in html
    assert not list(output.glob("*.srt")) and not list(output.glob("*.vtt"))
    assert delivery.prepare(project) == manifest


@pytest.mark.parametrize("short_count", [1, 3])
def test_missing_main_master_prevents_delivery_preparation(tmp_path, monkeypatch, short_count):
    project, output, name = setup_project(tmp_path, monkeypatch, short_count)
    (project / "06_delivery/youtube" / name).unlink()
    with pytest.raises(FileNotFoundError, match="long-form main video"):
        delivery.prepare(project)
    assert not (project / "07_publish/drive-delivery-manifest.json").exists()
    assert not (output / name).exists()


def test_multi_short_package_still_rejects_changed_approved_asset(tmp_path, monkeypatch):
    project, output, name = setup_project(tmp_path, monkeypatch, 3)
    (output / "thumbnail-a.png").write_bytes(b"changed-after-review")
    with pytest.raises(ValueError, match="changed after packaging"):
        delivery.prepare(project)
    assert not (output / name).exists()


def test_multi_short_package_rejects_unapproved_video_even_with_valid_hash(tmp_path, monkeypatch):
    project, output, name = setup_project(tmp_path, monkeypatch, 3)
    rogue = output / "unapproved-preview.mp4"
    rogue.write_bytes(b"not-a-final-deliverable")
    package_path = output / "delivery-manifest.json"
    package = json.loads(package_path.read_text())
    package["files"].append({"filename": rogue.name, "bytes": rogue.stat().st_size,
                             "sha256": hashlib.sha256(rogue.read_bytes()).hexdigest()})
    package_path.write_text(json.dumps(package))
    with pytest.raises(ValueError, match="Only the final main video"):
        delivery.prepare(project)
    assert not (output / name).exists()
