# ICM & Anaesthesia Digest: notes for the weekly run

These override the generic steps in the scheduled prompt where they differ.

## Research
- The sandbox's egress policy blocks journal, government, legal and FOAMed sites, both for shell and WebFetch. WebSearch still returns results.
- Read the newest Critical Care Reviews subscriber newsletter from Omar's Gmail first (`from:rob@criticalcarereviews.com subject:Newsletter`). It arrives on Saturday or Sunday night and is the lead source. Its "Quick Takes" give CCR's own numbers. Say on air that figures come from CCR's summary if the paper itself couldn't be opened.
- Use WebSearch to corroborate details such as DOIs, trial design and court case pages. Never use an unconfirmed number.

## Audio
- Render with `python3 tools/render.py script.txt <out.mp3> "<D Month YYYY>"`.
- Use only `gemini-3.8-flash-tts`, with Kate as Kore and Tom as Charon. Never switch models partway through an episode: the accents change, and Omar finds that distracting. The script exits non-zero rather than mixing models.
- The Gemini key is meant to be on a paid tier. If you get 429 quota errors that mention the free tier, billing has lapsed. Re-run later (finished segments are cached), or fall back to Kokoro for the whole episode and say so in the email.
