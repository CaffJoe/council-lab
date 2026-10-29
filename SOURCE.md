# Source and boundaries

Council Lab is a small independent adaptation of ideas in the private Council project's supervised Stage 1 design. It is not a copy of that project, its runtime, its history, or a complete implementation of its Stage 1 specification. The source inspected was GitHub `CaffJoe/Council`, observed `main` commit `b25abc706b2269039f1bae796416fe5c9b1bfa85`. The original local checkout was unavailable. At that revision the terminology file was `CONTEXT.md`; the frozen Stage 1 reference and current design record were also inspected. The source remains private, so a public reader may not be able to access it.

The retained concepts are: a human aim; bounded, attributable evidence; separate affirmative and contrary cases; the contrary case seeing the affirmative case; judgment of individual claims rather than a vote; a crux, uncertainty, revisit condition, and human next step; and packet identity tied to inputs. This edition does not implement the original five-seat workflow, its private ordering, admission control, trusted durable store, recovery, workspace authorization, observer, external experiment handoff, or native process adapter. It does not claim the original Stage 1 acceptance scenarios pass. Fresh Codex chats are a supervised manual method, not independent process isolation. The built-in walkthrough contains no live model output.

The upstream source's packet and native modules were inspected before deciding the boundary. They depend on the private project's control and process machinery; this edition uses newly written standard-library code instead. There are no third-party runtime dependencies or copied upstream source files. Python itself is separately licensed by its distributors.

## License

This newly authored public edition is released under the included [MIT license](LICENSE), copyright Joe Caffrey. The private source repository did not declare a license at the inspected revision, and no upstream source files are redistributed here. This edition's license applies to this repository's code, documentation, and fictional examples; it does not grant rights to the private source repository.
