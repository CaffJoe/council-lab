# Council Lab: think through a decision

[Watch the 24-second film](https://github.com/user-attachments/assets/a07e0353-ddbc-42cd-9edc-abfbded9f765) or [download the MP4](council-lab-24s.mp4).

This short explainer introduces Council Lab's purpose and supervised workflow: bring a question and evidence, examine a supporting case and challenge, consider a judgment, and choose the next step. The graphics include actual saved output from the [recorded live Codex example](../examples/recorded-live/README.md). Its library case is fictional. Viewing the film runs no model.

## Spoken script

> Council Lab helps you think through a decision with Codex. You bring the question and the evidence. A Champion builds the case. A Skeptic challenges it. An Elder weighs both and suggests a next step. You move responses between fresh chats; the lab checks and saves the record. The final call stays with you.

The AI-generated voiceover uses [Kokoro-82M v1.0](https://huggingface.co/hexgrad/Kokoro-82M), with the `af_heart` American English female [preset](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md). This replacement take was generated locally at normal speed using [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx). It is the only soundtrack: there is no music, subtitle track or promotional footer. The MP3 source export is [audio/narration-original.mp3](audio/narration-original.mp3). Production settings, model fingerprints and the source fingerprint are in [audio/provenance.json](audio/provenance.json).

## Editorial sequence

| Film time | Picture |
| --- | --- |
| 0–6.25 seconds | “Think it through.” The operator supplies the question and evidence. |
| 6.25–8.3 seconds | Champion: build the case, beside the verbatim `champion-1` statement and E1 reference. |
| 8.3–10.1 seconds | Skeptic: challenge the case, beside the verbatim `skeptic-1` statement. |
| 10.1–13.15 seconds | Elder: weigh both and suggest a next step. The saved example chose `more_observation`. |
| 13.15–18.1 seconds | The operator moves responses between fresh Codex chats; the lab checks and saves the record. |
| 18.1–24 seconds | “You decide,” beside a verbatim excerpt from the saved next step. |

This example does not establish that the workflow improves decisions. The [recorded-example notes](../examples/recorded-live/README.md) retain the execution date, prompt-wrapper boundary, saved responses and validation results.

## Animated preview

The README also includes a [silent animated preview](council-lab-preview.gif), using the film's pictures at 960×540 and 10 fps. It replaces the static storyboard so readers have an inline motion preview when their GitHub app does not display the video player. It has no audio; tap the preview or **Watch with narration** to open the full film. The bare attachment URL retains the native player on GitHub's web README.

Mobile-app rendering has not been verified on a device. Reports of [different video behavior in GitHub mobile](https://github.com/orgs/community/discussions/188443) corroborate the reported limitation; web player markup alone does not verify app playback.

## Reproduction

The optional [renderer](source/render.py) draws the explanatory typography and typesets output excerpts directly from the saved records. The [edit](source/edit.json) contains the spoken script, timing and excerpt. The [design reference](source/design.json) adapts Yrael System Lab's warm paper, charcoal, slate and restrained typography. Excerpts sit openly on the canvas, with no card borders or shadows. Segoe UI is used for body and display lettering, Georgia only for the wordmark, and Consolas for identifiers; font files are not redistributed. There are no generated illustration assets. The renderer can use DejaVu fonts on Linux, with different metrics.

The application retains its standard-library-only setup. Re-rendering this media uses Python 3.13 and two optional packages:

```text
python -m pip install -r media/source/requirements.txt
python media/source/render.py --preview-gif
```

Pass `--ffmpeg /path/to/ffmpeg` to use an installed encoder, or `--stills-only` to render just the poster, storyboard and local review frames. Omit `--preview-gif` if you do not need the animated image. Reproduction uses the checked-in voice recording and makes no network request, AI call or credential lookup. Review stills and temporary rendering directories are ignored by Git.

The film is H.264/AAC, 1280×720, 30 fps and 24.0 seconds. The narration starts 0.65 seconds into the film, is normalized before encoding, and finishes before the final hold. No speech is cut to meet the limit. The [manifest](manifest.json) fingerprints the film, source audio, renderer and original recorded inputs.
