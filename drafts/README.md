# Deep-dive drafts awaiting audio

Researched and reviewed scripts that couldn't be rendered on 8 Oct 2026 because
gemini-3.8-flash-tts hit its 100-requests-per-day project quota. Each folder has
script.txt and notes.json. To publish one: copy it to /tmp/deepdive/SLUG/, then
`python3 drafts/finish.py render SLUG` and `python3 drafts/finish.py publish SLUG`
(publish oldest request first), commit, push, and label the Gmail request
(thread id in QUEUE.tsv) deep-dive-done. Delete the folder once published.
