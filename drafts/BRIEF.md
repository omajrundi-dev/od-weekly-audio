# Deep-dive brief (shared by every research agent)

You are preparing one 7 to 10 minute podcast script for Omar, a UK intensive care and anaesthesia consultant in Leeds who also does PDOC and Court of Protection work. Two hosts, Kate and Tom (UK ICU and anaesthesia consultants), talk to a fellow ICU consultant. Pitch it at consultant level: skip the basics and lead with what changes decisions at the bedside. Your TOPIC, ANGLE and SLUG are in your task message. Work dir: /tmp/deepdive/SLUG/ (create it).

## Research
Use WebSearch, curl (browser User-Agent; HTTPS goes through a proxy, see /root/.ccr/README.md for TLS problems) and PubMed E-utilities (esearch/efetch abstracts). Cover:
- Landmark and recent trials: name, year, journal, population, size, intervention vs control, primary outcome with effect size, main caveats. Include practice-changing trials, important negative ones, anything from the last 2 to 3 years (today is 8 October 2026), and big ongoing or about-to-report trials (check registry status).
- The most recent credible systematic reviews and meta-analyses, and what they add or contradict.
- Guidelines: UK first (NICE, FICM/ICS including GPICS, BTS, RCoA, Association of Anaesthetists, Resuscitation Council UK, MHRA as relevant), then international. Give each one's year, check for updates published in 2025 or 2026, and say where they disagree with each other or with the newest trials.
- Treatment (first line, escalation, rescue, what to avoid; doses only where they matter and you've verified them), outcomes and prognosis, controversies and practice variation.
- Medicolegal or ethical angle only if real for the topic. If included it must be precise: check case citations and holdings against the judgment text (caselaw.nationalarchives.gov.uk, bailii).

Standards: verify every number against its primary source (at least the PubMed abstract); if you can't confirm a figure, leave it out. Label preprints, post-hoc/secondary analyses and consensus statements as such. Never invent a quote or attribute a view to a named person. No patient-identifiable information. Make sure each source URL really is the labelled paper (use https://doi.org/ DOIs from the PubMed record).

## Script: /tmp/deepdive/SLUG/script.txt
- One turn per line, each starting "Kate:" or "Tom:". Never two consecutive lines from the same speaker.
- A real conversation: short, uneven turns, sometimes a single word. One host leads and the other pushes back, asks the obvious clinical question or brings in prior evidence. Contractions, plain spoken British English. Hosts may give a clearly labelled personal opinion ("I'd...") but keep it separate from the evidence.
- Numbers as spoken words ("about one in five", "nought point eight", "thirty mils per kilo"). No digits, no symbols, no percent signs (say "percent"), no en-dash ranges, no "n=".
- Spell acronyms with spaces where they should be read as letters ("I C U", "R R T", "E C M O" or "ek-mo"); trial names that are words can stay as words. See /home/user/od-weekly-audio/script.txt for style.
- Shape: (1) quick hello and "Today's deep dive is TOPIC", plus why it matters to an ICU consultant now; (2) the evidence as a story: what we used to do, the trials that changed it, where it stands now; (3) what guidelines say and where they part company; (4) practical management; (5) outcomes and prognosis; (6) grey zones; (7) three to five take-home points for Monday, then goodbye.
- LENGTH: 1,200 to 1,380 words including speaker labels (check with wc -w). The hard cap is 10 minutes 30 seconds of audio and 1,480 words rendered at 10:15, so don't exceed 1,400. Under 800 is too thin. Choose depth over breadth.

## Notes: /tmp/deepdive/SLUG/notes.json
Keys: "title_topic" (the TOPIC exactly as given), "summary" (one paragraph), "takeaways" (3 to 5 strings matching the script's take-homes), "sources" (list of {"label", "url"} for every trial, review, guideline and case mentioned).

## Don'ts
Don't render audio, touch the git repo or send email. Finish by replying with the word count, the newest guideline or trial you found that the ANGLE didn't mention, and any figures you couldn't verify.
