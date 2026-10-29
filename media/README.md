# The Council Lab short film

[Watch the 26-second MP4](council-lab-26s.mp4).

This is an illustrated fictional overview, not a screen recording or a fresh model run. The evidence and questions come from the [library fixture](../examples/library.json). The separately [recorded live example](../examples/recorded-live/README.md) contains the actual saved Codex responses.

The visual direction adapts our Shadow Theatre production style: ink cutouts, parchment texture, muted olive-gold light, articulated sleeves and hands, and paper props that remain attached to their hand targets. The librarian raises two evidence sheets, compares the supporting and challenging questions, then lowers two concrete next checks. There is no voiceover. On-screen words carry the meaning, accompanied by a short original synthesized score.

## Text transcript

| Time | On-screen explanation and action |
| --- | --- |
| 0–4 seconds | **A quieter hour?** How could a library help more people? A librarian considers the question at a service desk. |
| 4–9 seconds | **Start with the evidence.** Two tallies, the same four Tuesdays: 12 requests for quiet; 20 people needed help. The librarian lifts the two sheets. |
| 9–15 seconds | **Make a case. Challenge it.** Could one room help? Who might lose access? The challenge responds to the actual supporting case. |
| 15–20.5 seconds | **Keep the unknowns visible.** Demand, room access, and whether ordinary help can continue. A useful judgment says what remains uncertain. |
| 20.5–26 seconds | **Council Lab.** Check access. Ask visitors. Then choose what to try. Try the example; change the question. |

The film continuously identifies itself as an illustrated fictional example. No model is run by viewing it. The introductory fade lasts 0.35 seconds; there are no flashing effects.

## Artwork and reproduction

Four new raster assets were generated with built-in ImageGen for this public edition. The original private film's artwork, characters, audio and project data are not redistributed. The exact generation prompts are in [source/image-prompts.json](source/image-prompts.json). The editable [renderer](source/render.py) composes the generated layers, captions, paper actions and original score. Microsoft Georgia and Calibri were used for the rendered lettering; font files are not included. DejaVu Serif and Sans can be used by the renderer on Linux, with slightly different metrics.

The application retains its standard-library-only setup. Re-rendering this optional media uses Python 3.13, Pillow, NumPy and imageio-ffmpeg:

```text
python -m pip install -r media/source/requirements.txt
python media/source/render.py
```

You can pass `--ffmpeg /path/to/ffmpeg` to use an installed encoder, or `--stills-only` to produce only the poster, storyboard and local review frames. Review stills are ignored by Git. The script does not call a model or require an API key; regenerating the source artwork is a separate creative action.

The checked-in film is H.264 with AAC audio, 1280×720, 30 fps, 780 frames, and 26.0 seconds. Full video and audio decoding passed. The [media manifest](manifest.json) records file fingerprints and production facts. The repository's MIT license covers the newly authored media and renderer; optional tooling and fonts retain their own licenses.
