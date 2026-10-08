"""Render, tag and publish finished deep dives.

Usage: python3 finish.py render SLUG     (render + retag + print duration)
       python3 finish.py publish SLUG... (add to feed, oldest request first)
"""
import datetime, email.utils, html, json, os, re, shutil, subprocess, sys
import xml.etree.ElementTree as ET

REPO = "/home/user/od-weekly-audio"
DATE = "2026-10-07"
CAP = 40
MARKER = "<!-- EPISODES: newest first, max 40. New <item> elements are inserted directly below this line. -->"


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]))


def check_script(slug):
    lines = [l.rstrip("\n") for l in open(f"/tmp/deepdive/{slug}/script.txt") if l.strip()]
    problems = []
    prev = None
    for i, l in enumerate(lines, 1):
        sp = l.split(":", 1)[0]
        if sp not in ("Kate", "Tom"):
            problems.append(f"line {i}: bad speaker {sp!r}")
        if sp == prev:
            problems.append(f"line {i}: {sp} twice in a row")
        prev = sp
        if re.search(r"[0-9%=–—]", l):
            problems.append(f"line {i}: digit/symbol: {l[:80]}")
    words = sum(len(l.split()) for l in lines)
    return words, problems


def render(slug):
    d = f"/tmp/deepdive/{slug}"
    n = json.load(open(f"{d}/notes.json"))
    words, problems = check_script(slug)
    print(f"{slug}: {words} words; {len(problems)} script problems")
    for p in problems:
        print("  ", p)
    subprocess.run(["python3", "tools/render.py", f"{d}/script.txt", f"{d}/raw.mp3", "7 October 2026"],
                   cwd=REPO, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{d}/raw.mp3", "-c", "copy", "-id3v2_version", "3",
                    "-metadata", f"title=Deep dive: {n['title_topic']}",
                    "-metadata", "artist=ICM & Anaesthesia Digest",
                    "-metadata", "album=ICM & Anaesthesia Digest", f"{d}/final.mp3"], check=True)
    secs = duration(f"{d}/final.mp3")
    print(f"{slug}: {int(secs // 60)}:{int(secs % 60):02d} {'OVER CAP' if secs > 630 else 'ok'}")


def publish(slugs):
    os.chdir(REPO)
    f = open("feed.xml").read()
    assert MARKER in f
    now = datetime.datetime.now(datetime.timezone.utc)
    e = html.escape
    items = ""
    for i, slug in enumerate(slugs):
        d = f"/tmp/deepdive/{slug}"
        n = json.load(open(f"{d}/notes.json"))
        base = f"deep-dive-{DATE}-{slug}"
        fn, guid, k = f"{base}.mp3", f"od-deepdive-{DATE}-{slug}", 2
        while os.path.exists(f"episodes/{fn}"):
            fn, guid, k = f"{base}-{k}.mp3", f"od-deepdive-{DATE}-{slug}-{k}", k + 1
        shutil.copy(f"{d}/final.mp3", f"episodes/{fn}")
        size = os.path.getsize(f"episodes/{fn}")
        secs = round(duration(f"{d}/final.mp3"))
        desc = (f"<p>{e(n['summary'])}</p>\n<p><strong>Take-home points</strong></p>\n<ul>\n"
                + "".join(f"<li>{e(t)}</li>\n" for t in n["takeaways"])
                + "</ul>\n<p><strong>Key sources</strong></p>\n<ul>\n"
                + "".join(f'<li><a href="{e(s["url"])}">{e(s["label"])}</a></li>\n' for s in n["sources"])
                + "</ul>\n<p><em>AI-generated summary of the sources listed; check the primary sources before "
                  "changing practice.</em></p>")
        assert "]]>" not in desc
        items = f"""
    <item>
      <title>Deep dive: {e(n['title_topic'])}</title>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{email.utils.format_datetime(now + datetime.timedelta(seconds=i))}</pubDate>
      <enclosure url="https://omajrundi-dev.github.io/od-weekly-audio/episodes/{fn}" length="{size}" type="audio/mpeg"/>
      <itunes:duration>{secs}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
      <description><![CDATA[{desc}]]></description>
    </item>""" + items
        print(f"{fn} {size} bytes {secs}s")
    f = f.replace(MARKER, MARKER + items)
    f = re.sub(r"<lastBuildDate>.*?</lastBuildDate>",
               f"<lastBuildDate>{email.utils.format_datetime(now + datetime.timedelta(seconds=len(slugs)))}</lastBuildDate>", f)
    # Enforce the cap: drop the oldest items (at the bottom) and their MP3s.
    blocks = re.findall(r"\n    <item>.*?</item>", f, flags=re.S)
    for old in blocks[CAP:]:
        url = re.search(r'enclosure url="[^"]*/episodes/([^"]+)"', old).group(1)
        f = f.replace(old, "")
        if os.path.exists(f"episodes/{url}"):
            os.remove(f"episodes/{url}")
        print(f"removed oldest: {url}")
    open("feed.xml", "w").write(f)
    t = ET.parse("feed.xml")
    assert "<itunes:block>Yes</itunes:block>" in f
    print("items:", len(t.findall(".//item")))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "render":
        for s in args:
            render(s)
    elif cmd == "publish":
        publish(args)
