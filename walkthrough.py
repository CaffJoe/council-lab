#!/usr/bin/env python3
"""Create a fixed, scripted example. No AI or network is used."""
import argparse
import json
from pathlib import Path
import sys
import lab

HERE = Path(__file__).resolve().parent
EXPECTED_CASE_HASH = "b6cfbbe0110eaa5719b24245af1b1877af63860574dea7cb00bf4648e15dc3f4"
RESPONSES = {
    "champion": {
        "claims": [
            {"id": "champion-1", "statement": "There is a reason to explore quieter study space.", "evidence": ["E1"], "inference": "The requests suggest interest, but they do not count unique people or establish demand for a specific hour."},
            {"id": "champion-2", "statement": "A small, limited trial may be feasible.", "evidence": ["E3"], "inference": "An available room could contain a trial without changing the whole library, if it is accessible and suitable."}
        ],
        "unknowns": ["Actual attendance and access needs are unknown.", "The room is unavailable on one of the four dates."],
        "falsifier": "A check showing that the room is inaccessible or that few people want to use it would weaken this case."
    },
    "skeptic": {
        "claims": [
            {"id": "skeptic-1", "statement": "A building-wide quiet hour could interfere with help people already use.", "evidence": ["E2"], "inference": "The tally does not show that help requires noise, but a restriction might discourage questions."},
            {"id": "skeptic-2", "statement": "The room does not establish that the proposed hour is workable.", "evidence": ["E3"], "inference": "Capacity, accessibility and one unavailable date could limit the champion's suggested trial."}
        ],
        "unknowns": ["We do not know whether the same people made repeated requests.", "We do not know what assistance or access the room needs."],
        "falsifier": "A small accessible room trial that attracts users without reducing help would weaken these concerns."
    },
    "elder": {
        "resolutions": [
            {"claim_id": "champion-1", "disposition": "supported", "reason": "The tally supports interest in quieter space, not the size of demand.", "evidence": ["E1"]},
            {"claim_id": "champion-2", "disposition": "uncertain", "reason": "The room is often available, but suitability and access have not been checked.", "evidence": ["E3"]},
            {"claim_id": "skeptic-1", "disposition": "uncertain", "reason": "People use the desk, but the effect of a quiet policy is not measured.", "evidence": ["E2"]},
            {"claim_id": "skeptic-2", "disposition": "supported", "reason": "The room is small and unavailable on one date; suitability is unknown.", "evidence": ["E3"]}
        ],
        "crux": "Can a quiet space meet demand without making ordinary help less accessible?",
        "uncertainty": ["The counts are small and do not establish demand or the effect of a policy.", "Room accessibility and actual use are unknown."],
        "outcome": "more_observation",
        "next_step": "Ask a librarian to check the room's accessibility and speak with a few visitors and desk staff before deciding whether to try one quiet-room session.",
        "revisit_when": "The room check and visitor feedback are available."
    }
}


def main():
    lab.configure_utf8_output()
    parser = argparse.ArgumentParser(description="Create a scripted fictional walkthrough")
    parser.add_argument("run", help="A new directory for this walkthrough")
    args = parser.parse_args()
    try:
        case_path = HERE / "examples" / "library.json"
        if lab.digest(lab.read(case_path)) != EXPECTED_CASE_HASH:
            raise lab.LabError("The example has changed. The fixed walkthrough applies only to the original fixture; use start for a changed case.")
        lab.start(case_path, args.run, origin="scripted")
        for role in lab.ROLES:
            p = lab.packet(args.run, role)
            record = {"packet_hash": p["packet_hash"], "role": role, "result": RESPONSES[role]}
            lab.validate_result(p, record)
            lab.write_new(Path(args.run) / f"{role}.json", record)
        lab.show(args.run)
    except lab.LabError as exc:
        print(f"Council Lab: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
