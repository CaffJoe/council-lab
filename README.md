# Council Lab

## Would you try a quiet hour at this library?

Over four Tuesday afternoons, staff at a fictional library logged **12 requests for quieter study space**. During those same hours, the service desk helped **20 people** with printing or computer questions. A meeting room seats eight and is free on three of the next four Tuesday afternoons.

**What would you check before scheduling a trial?**

<details>
<summary>See how the three roles answered in the recorded Codex run</summary>

- The **Champion** suggests trying the quiet hour in the meeting room so the service desk can keep helping visitors.
- The **Skeptic** asks whether the people who requested quiet would come at the proposed hour.
- The **Elder** suggests asking visitors which times work for them and checking whether the room meets their access needs.

</details>

You can use Council Lab the same way with your own question. Give each role a fresh Codex chat and bring its reply back to the lab. The lab saves the replies and checks that each piece of evidence they cite is in your case. You decide what to do next.

[See the saved run](examples/recorded-live/README.md) · [Run the example with Python](#quick-start) · [Try your own question with Codex](docs/guide.md#use-your-own-question)

## Watch the 24-second overview

https://github.com/user-attachments/assets/267d38c0-75c8-4569-b96b-7e73aa14832b

The film pairs AI narration with excerpts from the saved library run.

[Watch with narration](https://github.com/user-attachments/assets/267d38c0-75c8-4569-b96b-7e73aa14832b) · [Read the transcript](media/README.md#spoken-script) · [Download the MP4](media/council-lab-24s.mp4)

## Quick start

Clone this repository or [download and unzip it](https://github.com/CaffJoe/council-lab/archive/refs/heads/main.zip). Open a terminal in the folder that contains `walkthrough.py` and run the scripted example with **Python 3.9 or newer**.

```sh
python walkthrough.py my-walkthrough
```

The walkthrough works offline with replies written for the example. It prints the case and all three replies and saves them in `my-walkthrough/`. Near the end, look for `more_observation` and the suggestion to check room access and speak with visitors and desk staff.

To run it again, choose a new output folder name.

## How it works

The Champion gets your question and evidence. The Skeptic also gets the Champion’s argument. The Elder reads both arguments, addresses each claim, and suggests a next step. You can trace a claim back to the item it cites and judge whether the evidence supports it.

![Animated preview of the question, three roles, saved record, and human next step.](https://github.com/user-attachments/assets/7f70ac23-3320-44aa-8dc7-1e8238cf79e3)

*Animated preview · Silent.* [Watch with narration](https://github.com/user-attachments/assets/267d38c0-75c8-4569-b96b-7e73aa14832b).

## Recorded live example

Three fresh Codex runs examined the fictional library case on **October 29, 2026**. The Champion made four claims, the Skeptic made four, and the Elder answered all eight. [Read the responses and how they were recorded](examples/recorded-live/README.md).

To read the full saved record in your terminal, run this from the repository folder.

```sh
python lab.py show examples/recorded-live/run
```

## Go further

- [Read the full guide](docs/guide.md)
- [See what the lab checks in each reply](docs/guide.md#what-validation-checks)
- [Run the tests](docs/guide.md#development)
- [Read the source notes](SOURCE.md)

[MIT](LICENSE) · [Test results](https://github.com/CaffJoe/council-lab/actions/workflows/tests.yml)
