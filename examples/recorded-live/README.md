# Recorded live example

The fictional library case was examined by three fresh Codex runs on October 29, 2026. These are their **saved responses**. Viewing them does not start a fresh model run. All of the supplied evidence is fictional.

The [supporting case](run/champion.json) found a reason to explore quieter study space while preserving assistance at the service desk. The [challenge](run/skeptic.json) asked whether a quiet hour means an optional room or a library-wide rule, and whether the room is suitable and accessible. The [judgment](run/elder.json) accounted for all eight claims and chose to gather more information before a trial.

The next step was for a person to check demand, access needs, room suitability, and how existing help would be preserved. No real library action or experiment occurred.

From the repository root, inspect the evidence and responses with:

```text
python lab.py show examples/recorded-live/run
```

## Provenance and verification

Each `codex exec` invocation received one role's packet. The Skeptic received the accepted Champion response; the Elder received both accepted cases. The observed runtime identified Codex CLI 0.157.0, model `gpt-6-astra`, OpenAI provider, and a read-only sandbox. The invocations used an empty working directory, ephemeral session mode, and instructions to work only from the packet without tools or outside material. No tool execution was observed in the CLI logs. These settings do not establish complete isolation from other context.

All three responses passed Council Lab's validation on the first attempt. Their citations and reasoning were reviewed against the fictional source text. After the UTF-8 byte-order-mark fix, the recorded responses were also replayed through the public `start`, `prompt`, `submit`, and `show` commands in a new run. A single smoke test demonstrates this workflow on this fixture; it does not measure reliability or decision quality across cases.

An initial launch failed because the surrounding sandbox denied the CLI access to its local state; the successful runs followed granted access. An MCP connection returned HTTP 403 during startup, but the model calls completed and no MCP capability was needed. Session logs, credentials, and machine-specific data are excluded from this recording.

The [provenance manifest](provenance.json) records the observed configuration and SHA-256 fingerprints of the published case and responses. These fingerprints help detect accidental changes; they are not cryptographic authentication of a model run. The `recorded_live` label records the example's origin and does not alter the evidence, claims, or packet identities.
