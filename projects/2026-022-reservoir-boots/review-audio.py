"""Review generated audio and derive scene boundaries without rewriting narration."""

import json
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent


def read(name):
    return json.loads((P / name).read_text(encoding="utf-8"))


def write(name, payload):
    (P / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def probe(name):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(P / name)
    ], text=True))


def main():
    script = (P / "01_script/narration.txt").read_text(encoding="utf-8").strip()
    words = read("03_sync/captions.words.json")["words"]
    sync = read("03_sync/sync_report.json")
    pacing = read("03_sync/pacing_report.json")
    plan = read("01_script/scene-plan.json")
    estimates = read("01_script/pre-tts-scene-plan.json")
    assert script.split() == [w["text"] for w in words], "Captions must retain all approved words"
    assert sync["matched_character_ratio"] >= 0.92, "ASR coverage below threshold"
    media = probe("02_audio/working/voice.wav")
    duration = float(media["format"]["duration"])
    original_duration = float(probe("02_audio/inbox/2026-022-reservoir-boots-narration.mp3")["format"]["duration"])
    assert words[-1]["end"] <= duration + 0.1, "Words exceed audio"
    assert all(w["end"] >= w["start"] for w in words), "Negative word duration"
    offset = 0
    for i, scene in enumerate(plan["scenes"]):
        spoken = scene["narration_text"].split()
        assert scene["caption_text"] == scene["narration_text"]
        assert spoken == [w["text"] for w in words[offset:offset + len(spoken)]]
        scene["estimated_start_seconds"] = estimates["scenes"][i]["start_seconds"]
        scene["estimated_end_seconds"] = estimates["scenes"][i]["end_seconds"]
        scene["word_offset"] = offset
        scene["speech_start_seconds"] = words[offset]["start"]
        scene["speech_end_seconds"] = words[offset + len(spoken) - 1]["end"]
        scene["start_seconds"] = max(0, words[offset]["start"] - 0.35) if i else 0
        scene["audio"]["narration"] = "Bin jB1Cifc2UQbq1gR3wnb0, eleven_v3"
        offset += len(spoken)
    assert offset == len(words)
    for i, scene in enumerate(plan["scenes"]):
        end = plan["scenes"][i + 1]["start_seconds"] if i + 1 < len(plan["scenes"]) else duration + 4
        scene["end_seconds"] = round(end, 3)
        scene["duration_seconds"] = round(end - scene["start_seconds"], 3)
        scene["motion_beats"] = []
        time = scene["start_seconds"] + 1.2
        actions = ["단서 방향의 패닝", "전경/수면 반사 변화", "조명 또는 초점 이동"]
        j = 0
        while time < end:
            scene["motion_beats"].append({"time": round(time, 3), "action": actions[j % len(actions)]})
            j += 1
            time += 2.4
    plan.update({
        "status": "audio_aligned_awaiting_bgm_approval",
        "production_profile_status": "approved",
        "visual_style_status": "approved_recommended_direction",
        "voice_status": "generated_automated_review",
        "voice_duration_seconds": duration,
        "duration_seconds": duration + 4,
        "timing_source": "mlx-community/whisper-large-v3-turbo aligned to paced voice; images not composed yet",
    })
    write("01_script/scene-plan.json", plan)
    boundaries = [s["speech_start_seconds"] for s in plan["scenes"]]
    reviewed_gaps = []
    for gap in pacing.get("long_word_gaps", []):
        boundary = min(boundaries, key=lambda b: abs(b - gap["end"]))
        is_boundary = abs(boundary - gap["end"]) < 0.1
        reviewed_gaps.append({**gap, "scene_boundary": is_boundary,
                              "decision": "retain source; ASR boundary gap is not a detected waveform silence" if is_boundary and gap["duration"] < 1 else "needs_review"})
    tail_windows = []
    for window in pacing.get("slow_windows", []):
        actual_span = window["end"] - window["start"]
        corrected = round(window["word_count"] * 60 / actual_span, 1)
        tail_windows.append({**window, "actual_span_wpm": corrected,
                             "decision": "tail-window denominator artifact" if actual_span < 15 and corrected >= 58 else "needs_review"})
    gaps_clear = all(g["decision"] != "needs_review" for g in reviewed_gaps)
    slow_clear = all(w["decision"] != "needs_review" for w in tail_windows)
    report = {
        "status": "automated_review_pass" if not pacing.get("long_silence_count", 0) and gaps_clear and slow_clear else "needs_gap_review",
        "review_scope": "ASR alignment, approved-text preservation, waveform silence, timing and container checks; not full human listening",
        "voice_id": "jB1Cifc2UQbq1gR3wnb0",
        "model_id": "eleven_v3",
        "chunk_characters": [1052, 1063, 1048, 1068, 1045],
        "original_duration_seconds": original_duration,
        "voice_duration_seconds": duration,
        "planned_bgm_outro_seconds": 4,
        "planned_total_seconds": duration + 4,
        "pitch_preserving_speed_multiplier": 1.05,
        "matched_character_ratio": sync["matched_character_ratio"],
        "caption_word_count": len(words),
        "source_word_count": len(script.split()),
        "first_anomaly_seconds": plan["scenes"][2]["speech_start_seconds"],
        "first_anomaly_in_target_window": 40 <= plan["scenes"][2]["speech_start_seconds"] <= 60,
        "pacing": pacing,
        "reviewed_word_gaps": reviewed_gaps,
        "reviewed_slow_windows": tail_windows,
        "audio_media": media,
        "full_human_listening_claimed": False,
        "pronunciation_listening_checks": [
            {"start": 248, "text": "낮은 턱", "reason": "ASR variation; cannot determine whether pronunciation or recognition error"},
            {"start": 323, "text": "내려놨어요", "reason": "ASR variation; cannot determine whether pronunciation or recognition error"},
        ],
        "final_voice_approved": False,
        "bgm_approved": False,
        "render_approved": False,
    }
    write("05_review/audio-review.json", report)
    def stamp(t):
        return f"{int(t) // 60:02}:{int(t) % 60:02}.{round((t % 1) * 1000):03}"
    rows = ["# 실제 음성 기준 씬 타임라인", "", "Whisper turbo 정렬값으로 계산했다. 이미지 전환은 관련 발화 최대 0.35초 선행하며, 최종 이미지별 컷과 렌더 검수는 아직 남아 있다.", "", "| 구간 | 목적 | 이미지 계획 |", "| --- | --- | --- |"]
    rows += [f"| {stamp(s['start_seconds'])}~{stamp(s['end_seconds'])} | {s['purpose']} | {s['planned_image_count']} |" for s in plan["scenes"]]
    rows += ["", f"음성 {duration:.3f}초, 예정 BGM 여운 4초, 예상 완성 {duration + 4:.3f}초. 첫 이상 징후 실제 발화 {report['first_anomaly_seconds']:.3f}초.", "", "녹음 전 추정 원본은 pre-tts-scene-plan.json에 보존했다. BGM/이미지/렌더 승인과 완료를 뜻하지 않는다."]
    (P / "01_script/scene-plan.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["status", "voice_duration_seconds", "planned_total_seconds", "matched_character_ratio", "first_anomaly_seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
