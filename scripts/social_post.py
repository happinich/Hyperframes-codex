#!/usr/bin/env python3
"""Dry-run or publish social posts for a rendered video project."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "social-posting.example.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def post_form(url: str, data: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    return request_json(request)


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    return request_json(request)


def request_json(request: urllib.request.Request) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {body}") from error


def fill_template(text: str, youtube_url: str) -> str:
    return text.replace("{youtube_url}", youtube_url)


def env_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing environment variable: {name}")
    return value


def dry_run(platform: str, payload: dict[str, Any]) -> None:
    print(f"\n[{platform.upper()} DRY RUN]")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def parse_publish_at(value: str, timezone: str) -> datetime:
    text = value.strip()
    normalized = text.replace(" ", "T", 1) if " " in text and "T" not in text else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise RuntimeError(
            "--publish-at must be ISO-like, e.g. 2026-06-30T20:30 or 2026-06-30 20:30"
        ) from error
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo(timezone))
    return parsed


def wait_until_publish_time(args: argparse.Namespace) -> None:
    if not args.publish_at:
        return
    target = parse_publish_at(args.publish_at, args.timezone)
    if args.publish_delay_minutes:
        target += timedelta(minutes=args.publish_delay_minutes)
    now = datetime.now(target.tzinfo)
    wait_seconds = (target - now).total_seconds()
    print(f"Scheduled publish time: {target.isoformat(timespec='minutes')}")
    if not args.live:
        print("Dry-run mode: schedule was parsed, but the script will not wait or publish.")
        return
    if wait_seconds <= 0:
        print("Scheduled time is already past. Publishing now.")
        return
    if args.no_wait:
        raise RuntimeError(
            f"scheduled time is {int(wait_seconds)} seconds in the future; "
            "remove --no-wait to wait in this process"
        )
    print(f"Waiting {int(wait_seconds)} seconds until scheduled social publish...")
    time.sleep(wait_seconds)


def publish_threads(config: dict[str, Any], text: str, live: bool) -> None:
    platform = config["threads"]
    token_env = platform.get("access_token_env", "THREADS_ACCESS_TOKEN")
    user_env = platform.get("user_id_env", "THREADS_USER_ID")
    base_url = platform.get("graph_base_url", "https://graph.threads.net/v1.0").rstrip("/")
    payload = {"media_type": "TEXT", "text": text}
    if not live:
        dry_run("threads", payload)
        return
    token = env_required(token_env)
    user_id = env_required(user_env)
    create = post_form(f"{base_url}/{user_id}/threads", {**payload, "access_token": token})
    creation_id = create.get("id")
    if not creation_id:
        raise RuntimeError(f"Threads container response missing id: {create}")
    published = post_form(
        f"{base_url}/{user_id}/threads_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    print(json.dumps({"threads": published}, ensure_ascii=False, indent=2))


def publish_instagram(config: dict[str, Any], post: dict[str, Any], live: bool, media_url: str | None) -> None:
    platform = config["instagram"]
    token_env = platform.get("access_token_env", "INSTAGRAM_ACCESS_TOKEN")
    user_env = platform.get("user_id_env", "INSTAGRAM_USER_ID")
    base_url = platform.get("graph_base_url", "https://graph.facebook.com/v20.0").rstrip("/")
    caption = post.get("reels_caption") or post.get("caption") or ""
    payload: dict[str, str] = {"caption": caption}
    if media_url:
        payload.update({"media_type": "REELS", "video_url": media_url, "share_to_feed": "true"})
    else:
        payload["note"] = "Instagram auto-publish needs a public video_url or image_url. Local MP4 files cannot be uploaded directly by this script."
    if not live:
        dry_run("instagram", payload)
        return
    if not media_url:
        raise RuntimeError("Instagram live publish requires --instagram-media-url with a public HTTPS video URL")
    token = env_required(token_env)
    user_id = env_required(user_env)
    create = post_form(f"{base_url}/{user_id}/media", {**payload, "access_token": token})
    creation_id = create.get("id")
    if not creation_id:
        raise RuntimeError(f"Instagram container response missing id: {create}")
    print("Instagram media container created. Waiting before publish...")
    time.sleep(20)
    published = post_form(
        f"{base_url}/{user_id}/media_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    print(json.dumps({"instagram": published}, ensure_ascii=False, indent=2))


def publish_x(config: dict[str, Any], text: str, live: bool) -> None:
    platform = config["x"]
    token_env = platform.get("access_token_env", platform.get("bearer_token_env", "X_ACCESS_TOKEN"))
    url = platform.get("create_post_url", "https://api.x.com/2/tweets")
    payload = {"text": text}
    if not live:
        dry_run("x", payload)
        return
    token = env_required(token_env)
    published = post_json(url, payload, {"Authorization": f"Bearer {token}"})
    print(json.dumps({"x": published}, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path, help="Project directory")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--posts", type=Path, help="Defaults to project/07_publish/social/social-posts.json")
    parser.add_argument("--youtube-url", required=True, help="Published YouTube URL to include in social posts")
    parser.add_argument("--platform", choices=("all", "instagram", "threads", "x"), default="all")
    parser.add_argument("--instagram-media-url", help="Public HTTPS video URL for Instagram Reels publishing")
    parser.add_argument(
        "--publish-at",
        help="Wait until this YouTube scheduled publish time before posting, e.g. '2026-06-30 20:30'",
    )
    parser.add_argument("--timezone", default="Asia/Seoul", help="Timezone for --publish-at when no offset is included")
    parser.add_argument(
        "--publish-delay-minutes",
        type=float,
        default=0,
        help="Post this many minutes after --publish-at. Use 5-15 minutes if YouTube processing needs a buffer.",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="With --live and a future --publish-at, fail instead of keeping the process open.",
    )
    parser.add_argument("--live", action="store_true", help="Actually call platform APIs. Omit for dry-run.")
    args = parser.parse_args()

    project = args.project.resolve()
    posts_path = (args.posts or project / "07_publish" / "social" / "social-posts.json").resolve()
    if not posts_path.exists():
        parser.error(f"missing social posts file: {posts_path}")
    if not args.config.exists():
        parser.error(f"missing config: {args.config}")

    config = load_json(args.config)
    posts = load_json(posts_path)
    youtube_url = args.youtube_url.strip()

    try:
        wait_until_publish_time(args)
        if args.platform in ("all", "threads") and config.get("threads", {}).get("enabled", True):
            publish_threads(config, fill_template(posts["threads"]["text"], youtube_url), args.live)
        if args.platform in ("all", "x") and config.get("x", {}).get("enabled", True):
            publish_x(config, fill_template(posts["x"]["text"], youtube_url), args.live)
        if args.platform in ("all", "instagram") and config.get("instagram", {}).get("enabled", True):
            instagram_post = dict(posts["instagram"])
            for key, value in list(instagram_post.items()):
                if isinstance(value, str):
                    instagram_post[key] = fill_template(value, youtube_url)
            publish_instagram(config, instagram_post, args.live, args.instagram_media_url)
    except RuntimeError as error:
        print(f"social publish failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
