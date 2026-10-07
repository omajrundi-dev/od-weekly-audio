"""Render script.txt to a finished MP3 with Gemini multi-speaker TTS.

Usage: python3 tools/render.py script.txt out.mp3 "7 October 2026"

The whole episode is rendered on one model (gemini-3.8-flash-tts) so the
voices and accents stay consistent. If any segment still fails after
retries the script exits non-zero and writes no MP3; it never mixes models.
Finished segments are cached in <out dir>/seg/, so re-running only renders
the missing ones.
"""
import base64, json, os, subprocess, sys, time, urllib.error, urllib.request

MODEL = "gemini-3.8-flash-tts"
VOICES = {"Kate": "Kore", "Tom": "Charon"}
SEGMENT_CHARS = 2500
NOTE = ("A relaxed, natural conversation between two British intensive care doctors who know each other well, "
        "recorded for a weekly podcast. Both speak with educated Southern English accents. Conversational pace, "
        "with natural pauses, small reactions and the occasional laugh where it fits. Not a news-reader delivery.")

script_path, out_path, date_label = sys.argv[1], sys.argv[2], sys.argv[3]
key = os.environ["GEMINI_API_KEY"]
work = os.path.join(os.path.dirname(os.path.abspath(out_path)), "seg")
os.makedirs(work, exist_ok=True)

# Split at turn boundaries into segments of about SEGMENT_CHARS.
lines = [l.strip() for l in open(script_path) if l.strip()]
segments, cur = [], []
for line in lines:
    if cur and sum(len(x) + 1 for x in cur) + len(line) > SEGMENT_CHARS:
        segments.append(cur)
        cur = []
    cur.append(line)
if cur:
    segments.append(cur)


def request(seg):
    # gemini-3.8-flash-tts takes one part per turn, tagged with its speaker;
    # it rejects systemInstruction, so the director's note goes in "style".
    parts = []
    for line in seg:
        speaker, _, text = line.partition(":")
        parts.append({"text": text.strip(), "speechMetadata": {"speaker": speaker.strip(), "style": NOTE}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"multiSpeakerVoiceConfig": {
                "speakerVoiceConfigs": [{"speaker": s, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}}
                                        for s, v in VOICES.items()]}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


wavs, failed = [], []
for i, seg in enumerate(segments):
    raw = os.path.join(work, f"s{i:02d}.pcm")
    wav = os.path.join(work, f"s{i:02d}.wav")
    if not os.path.exists(raw):
        pcm = None
        for attempt in range(5):
            try:
                cand = request(seg)["candidates"][0]
                if cand.get("finishReason") == "PROHIBITED_CONTENT":
                    print(f"segment {i}: PROHIBITED_CONTENT; soften the wording and re-run", flush=True)
                    break
                pcm = base64.b64decode(cand["content"]["parts"][0]["inlineData"]["data"])
                break
            except urllib.error.HTTPError as e:
                print(f"segment {i}: HTTP {e.code} {e.read()[:300]!r}", flush=True)
                if e.code not in (429, 500, 503):
                    break
            except Exception as e:
                print(f"segment {i}: {e!r}", flush=True)
            time.sleep(min(2 ** (attempt + 2), 60))
        if pcm is None:
            failed.append(i)
            continue
        open(raw, "wb").write(pcm)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1",
                    "-i", raw, wav], check=True)
    wavs.append(wav)
    print(f"segment {i}: ok", flush=True)

if failed:
    sys.exit(f"{len(failed)} of {len(segments)} segments failed: {failed}. No MP3 written.")

silence = os.path.join(work, "silence.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                "-t", "0.25", silence], check=True)
concat_list = os.path.join(work, "list.txt")
with open(concat_list, "w") as f:
    f.write(f"file '{silence}'\n".join(f"file '{w}'\n" for w in wavs))
joined = os.path.join(work, "joined.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", concat_list,
                "-c", "copy", joined], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", joined,
                "-af", "loudnorm=I=-16:TP=-1.5", "-ac", "1", "-ar", "44100", "-b:a", "48k",
                "-metadata", f"title=ICM & Anaesthesia Digest — {date_label}",
                "-metadata", "artist=ICM & Anaesthesia Digest", "-metadata", "album=ICM & Anaesthesia Digest",
                "-id3v2_version", "3", out_path], check=True)
print(f"wrote {out_path} ({MODEL}, {len(segments)} segments)")
