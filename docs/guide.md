# Council Lab guide

[Back to the README](../README.md)

Council Lab is a small, supervised workflow. You provide a case, bring responses from fresh Codex chats, inspect their reasoning, and choose the next step. The Python commands prepare packets, validate responses, and save a record.

## Explore the included example

The [fictional library case](../examples/library.json) asks whether to try a quiet hour on Tuesday afternoons. It includes requests for quieter study space, use of existing assistance, a room schedule, and explicit unknowns.

From the repository root:

```sh
python walkthrough.py my-walkthrough
python lab.py show my-walkthrough
```

Requires Python 3.9 or later. The walkthrough uses only the standard library and works offline after you obtain the repository. Its evidence and responses were written for the example; **no model is called**. It shows the evidence, supporting and challenging claims, judgment, uncertainty, and suggested next step.

Choose a new output directory each time. The commands create accepted records once rather than overwriting them.

The point is to inspect the reasoning. The fictional tallies do not establish attendance, accessibility, comparative priority, or a successful quiet-hour arrangement. A suggested next step is a check a librarian could choose to make.

## Inspect the recorded live example

The [recorded live example](../examples/recorded-live/README.md) contains saved responses from three fresh Codex runs on October 29, 2026. Its evidence is fictional. Viewing the record does not run a model:

```sh
python lab.py show examples/recorded-live/run
```

The supporting case, challenge, and judgment passed validation. The judgment addressed all eight claims, identified ambiguity about what a quiet hour would mean, and suggested checking demand, access, room suitability, and existing services before scheduling a trial.

The recording's [notes and provenance](../examples/recorded-live/README.md#provenance-and-verification) retain its configuration, fingerprints, verification, and prompt-wrapper boundary. One example does not measure reliability or decision quality across cases.

## Use your own question

1. Copy [examples/library.json](../examples/library.json) to a new file, such as `my-case.json`. Change the question, aim, evidence, sources, and unknowns. Keep the same field names and unique evidence IDs.
2. Create a run in a **new** directory:

   ```sh
   python lab.py start my-case.json my-run
   python lab.py show my-run
   ```

3. Print the first role's prompt:

   ```sh
   python lab.py prompt my-run champion
   ```

   Copy it into a **fresh Codex chat** and ask for the JSON response. Save the response, without code fences, as a UTF-8 file such as `response.json`.

4. Validate and save the response:

   ```sh
   python lab.py submit my-run champion response.json
   ```

   If validation fails, correct the response against the printed packet and submit again.

5. Repeat the prompt and submit commands for `skeptic`, using a **fresh chat**, then for `elder`, again using a fresh chat. The Skeptic receives the accepted supporting case; the Elder receives both cases.
6. Read the complete record, consider the uncertainty, and choose your own next step:

   ```sh
   python lab.py show my-run
   ```

Use fictional material or data you are authorized to share. A prompt contains the entire case. If you change the example or an earlier input, start a new run to preserve the previous record.

The commands read and write UTF-8, including when output is redirected to a file. They accept operator-supplied JSON; they do not launch Codex or verify which model produced a response. You can also write responses yourself. Obtaining new responses from Codex requires your own Codex access.

## What validation checks

The case is copied into a new run and receives a content fingerprint. Each role gets a packet for those exact inputs:

- The Champion sees the case.
- The Skeptic also sees the accepted Champion response.
- The Elder sees both accepted cases.

A response must match its role and packet fingerprint. Evidence citations must refer to IDs in the case, and the judgment must address each claim exactly once. Accepted files are created once by the commands. If an earlier input changes, later records no longer match.

Validation checks structure, input binding, citation IDs, and claim accounting. It cannot establish that a citation supports a claim or that the reasoning is sound. The `inference` field explains the step beyond the source; it is not itself a source.

## Boundaries

These are workflow checks. Fresh chats and prompt instructions ask Codex to restrict its context; the application does not enforce process isolation or control what Codex can access.

The operator controls the local files and can edit them. Fingerprints bind outputs to inputs, but are neither signatures nor proof of authenticity. Treat case content as untrusted, inspect model responses, and share only data appropriate for the chosen chat.

Council Lab provides no workspace enrollment, background observer, scheduler, live evidence collection, experiment execution, or automatic external action. It is not a security sandbox or durable audit system.

See [SOURCE.md](../SOURCE.md) for the relationship to the original private Council and the parts this edition omits.

## Development

Run the standard-library test suite from the repository root:

```sh
python -m unittest discover -s tests -v
```

The optional media renderer has its own [production notes and dependencies](../media/README.md#reproduction). They are separate from running Council Lab.
