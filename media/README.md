# Council Lab: one question, three angles

[Watch the 24-second film](https://github.com/user-attachments/assets/03b54ea1-a928-4901-b60c-4f5b30677313) or [download the MP4](council-lab-24s.mp4).

This is an editorial animation of the [recorded live Codex example](../examples/recorded-live/README.md). The supporting claim, challenge, eight dispositions, outcome and next-step excerpt come from the actual saved JSON records. They are typeset for the film, rather than shown in a screen recording. The library question and its evidence are fictional. Viewing the film runs no model.

## Spoken script

> Should a library try a quiet hour? Council Lab keeps the evidence visible while a supporting case meets a challenge. This saved Codex run addresses all eight claims. The outcome is more observation: check demand, access, and existing help. The case is fictional. A person chooses what happens next.

The voiceover is AI-generated with ElevenLabs, using Alice – Gentle Storyteller and Eleven Multilingual v2. A new take was made for this film. It is the only soundtrack: there is no music, subtitle track or promotional footer. The original source export is [audio/narration-original.mp3](audio/narration-original.mp3). Production settings and the source fingerprint are in [audio/provenance.json](audio/provenance.json).

## Editorial sequence

| Film time | Picture |
| --- | --- |
| 0–3.4 seconds | The quiet-hour question and the fictional evidence tallies: 12 requests for quieter space and 20 people helped, over the same four Tuesdays. The counts do not rank competing needs. |
| 3.4–6.9 seconds | Verbatim `champion-1` statement with its E1 reference. |
| 6.9–9.45 seconds | Verbatim `skeptic-1` statement challenging what those requests establish. |
| 9.45–12.2 seconds | All eight saved claim IDs and their actual dispositions. “Supported” is the recorded judgment, not independent proof that a claim is true. |
| 12.2–17.6 seconds | The saved `more_observation` outcome. Demand, access and existing help summarize checks in the saved next step. |
| 17.6–24 seconds | The person keeps the decision, beside a verbatim excerpt from the saved next step. |

This example does not establish that the workflow improves decisions. The [recorded-example notes](../examples/recorded-live/README.md) retain the execution date, prompt-wrapper boundary, saved responses and validation results.

## Reproduction

The optional [renderer](source/render.py) draws the typography, output excerpts and animated highlights directly from the saved records. The [edit](source/edit.json) contains the spoken script, timing and excerpt. The [design reference](source/design.json) adapts Yrael System Lab's warm paper, charcoal, slate and restrained typography. Excerpts sit openly on the canvas, with no card borders or shadows. Segoe UI is used for body and display lettering, Georgia only for the wordmark, and Consolas for identifiers; font files are not redistributed. There are no generated illustration assets. The renderer can use DejaVu fonts on Linux, with different metrics.

The application retains its standard-library-only setup. Re-rendering this media uses Python 3.13 and two optional packages:

```text
python -m pip install -r media/source/requirements.txt
python media/source/render.py
```

Pass `--ffmpeg /path/to/ffmpeg` to use an installed encoder, or `--stills-only` to render just the poster, storyboard and local review frames. Reproduction uses the checked-in voice recording and makes no network request, AI call or credential lookup. Review stills and temporary rendering directories are ignored by Git.

The film is H.264/AAC, 1280×720, 30 fps and 24.0 seconds. The narration starts 0.65 seconds into the film, is normalized before encoding, and finishes before the final hold. No speech is cut to meet the limit. The [manifest](manifest.json) fingerprints the film, source audio, renderer and original recorded inputs.
