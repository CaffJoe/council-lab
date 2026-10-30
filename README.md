# Council Lab

A hands-on Codex lab for examining evidence, challenging an argument, and choosing a human next step.

[Quick start](#quick-start) · [Recorded example](#recorded-live-example) · [Guide](docs/guide.md) · [MIT license](LICENSE)

## Watch the 24-second overview

https://github.com/user-attachments/assets/a07e0353-ddbc-42cd-9edc-abfbded9f765

**24 seconds · Sound on for narration.** [Transcript](media/README.md) · [Download MP4](media/council-lab-24s.mp4)

A high-level introduction to the workflow, illustrated with actual saved Codex responses to a **fictional library case**. The narration is AI-generated; the graphics animate the records rather than show a screen recording.

## Quick start

Requires **Python 3.9+**. Clone with Git, or [download the repository](https://github.com/CaffJoe/council-lab/archive/refs/heads/main.zip).

```sh
git clone https://github.com/CaffJoe/council-lab.git
cd council-lab
python walkthrough.py my-walkthrough
```

This **scripted walkthrough** runs locally, with no packages, model call, account, or API key. It creates a complete example you can inspect:

```sh
python lab.py show my-walkthrough
```

Use a new directory name each time. To work through your own question with fresh Codex responses, follow the [guide](docs/guide.md#use-your-own-question).

## How it works

A library is considering a quiet hour. Some visitors want a quieter place to study; others need help at the service desk. Each role examines the same supplied evidence:

| Role | Job |
| --- | --- |
| **Champion** | Make a supporting case, citing the evidence and stating the inference. |
| **Skeptic** | Challenge that case and identify what the evidence leaves unresolved. |
| **Elder** | Address every claim, name the uncertainty, and suggest a human next step. |

![Saved supporting claim, skeptical challenge, and judgment to gather more observations.](media/council-lab-storyboard.jpg)

Each response is bound to its input packet. Citation IDs and claim accounting are checked before a response is accepted. You review the reasoning and choose what happens next.

## Recorded live example

Three fresh Codex runs examined the fictional case on **October 29, 2026**. The saved judgment addressed all eight claims and chose **more observation**: check demand, access, room suitability, and existing assistance before a trial.

[Read the supporting case, challenge, judgment, and provenance](examples/recorded-live/README.md), or inspect the complete record:

```sh
python lab.py show examples/recorded-live/run
```

Viewing this recording starts no model. It demonstrates this one workflow; it does not establish improved decision quality.

## Go further

- [Use your own question with Codex](docs/guide.md#use-your-own-question)
- [Understand validation and its limits](docs/guide.md#what-validation-checks)
- [Inspect the recorded execution](examples/recorded-live/README.md)
- [Read the film script and production notes](media/README.md)
- [Run the checks](docs/guide.md#development)

Council Lab is a supervised learning example. You supply responses from fresh Codex chats; the program validates and saves them. Reasoning quality, source support, and the final decision require human review. See the [guide](docs/guide.md#boundaries) and [source notes](SOURCE.md) for the full boundary.

[MIT](LICENSE) · [Test results](https://github.com/CaffJoe/council-lab/actions/workflows/tests.yml)
