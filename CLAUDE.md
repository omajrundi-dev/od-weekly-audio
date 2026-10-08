# ICM & Anaesthesia Digest: notes for the weekly run

These override the generic steps in the scheduled prompt where they differ.

## Research
- Network access was opened on 7 Oct 2026. Fetch with curl and a browser User-Agent. criticalcarereviews.com and 39essex.com still return 403 (site bot protection), so use Gmail for CCR and WebSearch for 39 Essex.
- Read these feeds every week (verified 7 Oct 2026) and keep items first published in the window:
  - Journals: Anaesthesia https://associationofanaesthetists-publications.onlinelibrary.wiley.com/feed/13652044/most-recent · BJA https://www.bjanaesthesia.org/current.rss · JAMA https://jamanetwork.com/rss/site_3/67.xml · NEJM https://www.nejm.org/action/showFeed?jc=nejm&type=etoc&feed=rss · Lancet Respir Med https://www.thelancet.com/rssfeed/lanres_online.xml
  - Safety: MHRA alerts https://www.gov.uk/drug-device-alerts.atom · Drug Safety Update https://www.gov.uk/drug-safety-update.atom
  - Medicolegal: PFD reports https://www.judiciary.uk/feed/?post_type=pfd · EWCOP https://caselaw.nationalarchives.gov.uk/atom.xml?court=ewcop · MCLP https://www.mentalcapacitylawandpolicy.org.uk/feed/
  - Discourse: The Bottom Line https://www.thebottomline.org.uk/feed/ · St Emlyn's https://www.stemlynsblog.org/feed/
  - No working feed found yet for ICM (Springer), Critical Care (BMC), AJRCCM, HSSIB, RCoA or PulmCCM. Use their journal pages or PubMed (now reachable), and update this list when a feed URL is confirmed.
- Read the newest Critical Care Reviews subscriber newsletter from Omar's Gmail first (`from:rob@criticalcarereviews.com subject:Newsletter`). It arrives on Saturday or Sunday night and is the lead source. Its "Quick Takes" give CCR's own numbers. Say on air that figures come from CCR's summary if the paper itself couldn't be opened.
- Use WebSearch to corroborate details such as DOIs, trial design and court case pages. Never use an unconfirmed number.
- Also search Gmail for the past 8 days for journal alerts, MHRA/Drug Safety Update, Mental Capacity Report, PFD, The Bottom Line and FOAMed newsletters. Omar may subscribe to more over time.
- Open primary sources (papers, judgments, PFD reports) directly and quote from them rather than from summaries.

## Discourse around each item
- For each major item, look for what clinicians are saying, not just what the paper found. Check the journal's own editorial and correspondence, CCR's critique, The Bottom Line, St Emlyn's, EMCrit, PulmCCM, REBEL EM, ICM-focused podcasts, and public posts by named clinicians and triallists (use WebSearch with site: filters where fetch is blocked).
- On air, attribute it ("the accompanying editorial argues…", "on The Bottom Line, they point out…"). Keep opinion clearly separate from the evidence. Never invent a quote or attribute a view to a named person unless you've seen it in their own words. If you can't find any discourse, say nothing rather than imply there is consensus.

## Audio
- Render with `python3 tools/render.py script.txt <out.mp3> "<D Month YYYY>"`.
- Use only `gemini-3.8-flash-tts`, with Kate as Kore and Tom as Charon. Never switch models partway through an episode: the accents change, and Omar finds that distracting. The script exits non-zero rather than mixing models.
- Each Gemini call re-samples the voices, so accents can shift at every segment join. render.py uses about 9,000-character segments: a 10-minute deep dive is one call and a weekly episode four or five. Don't shrink SEGMENT_CHARS, and don't set a low temperature (it makes the model babble). A seed is accepted but doesn't make the voices repeatable.
- Gemini returns a WAV with a C2PA chunk after the audio, not bare PCM. render.py keeps only the WAV data chunk; treating the whole payload as PCM put a burst of white noise at every join (fixed 8 Oct 2026).
- The Gemini key is meant to be on a paid tier. If you get 429 quota errors that mention the free tier, billing has lapsed. Re-run later (finished segments are cached), or fall back to Kokoro for the whole episode and say so in the email.

## Length and depth (Omar, 7 Oct 2026)
- Omar prefers longer, more in-depth episodes. This overrides the scheduled prompt's 4,000-4,500 words and 30-minute cap.
- On a full week, aim for about 5,500-7,000 words (roughly 35-45 minutes). Hard cap: 50 minutes.
- Spend the extra time on depth, not more items. Go further into methods, the trial's place in prior evidence, discourse and disagreement, and practical implications. A quiet week is still shorter: never pad.

## Publishing (Omar, 7 Oct 2026)
- Always add episodes; never replace or overwrite one that's already in the feed. Don't edit an existing `<item>` or overwrite its MP3.
- If there's already an episode for today's date (a re-run, an extended edition, or a correction), publish the new one alongside it. Use `episodes/YYYY-MM-DD-2.mp3` (then -3 and so on), a matching guid such as `od-digest-YYYY-MM-DD-2`, and a title that says how it differs ("extended", "correction" and so on).
