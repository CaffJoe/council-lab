"""Render an editorial animation of saved output; never call an AI service."""
import argparse
from functools import lru_cache
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

MEDIA = Path(__file__).resolve().parents[1]
ROOT = MEDIA.parent
EDIT = json.loads((MEDIA / "source/edit.json").read_text(encoding="utf-8"))
DESIGN = json.loads((MEDIA / "source/design.json").read_text(encoding="utf-8"))
WIDTH, HEIGHT, FPS = 1280, 720, 30
SECONDS = EDIT["duration_seconds"]
PAPER = DESIGN["colors"]["paper"]
INK = DESIGN["colors"]["ink"]
SLATE = DESIGN["colors"]["slate"]
MUTED = DESIGN["colors"]["muted"]
RULE = DESIGN["colors"]["rule"]
GOLD = DESIGN["colors"]["gold"]
PALE_SLATE = DESIGN["colors"]["slate_surface"]


def record(role):
    path = ROOT / "examples/recorded-live/run" / (role + ".json")
    return json.loads(path.read_text(encoding="utf-8"))["result"]


CHAMPION, SKEPTIC, ELDER = (record(role) for role in ("champion", "skeptic", "elder"))


def ease(value):
    value = min(1, max(0, value))
    return 1 - (1 - value) ** 3


@lru_cache(maxsize=32)
def font(size, kind="sans"):
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    names = {
        "sans": [windows / "segoeui.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")],
        "display": [windows / "seguisb.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")],
        "serif": [windows / "georgia.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")],
        "mono": [windows / "consola.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")],
    }
    for path in names[kind]:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    raise RuntimeError("Install Segoe UI/Georgia/Consolas or DejaVu fonts")


def text(draw, xy, words, size, color=INK, kind="sans"):
    draw.text(xy, words, font=font(size, kind), fill=color)


def paragraph(draw, xy, words, width, size=32, color=INK, kind="sans", leading=1.35):
    x, y = xy
    line = ""
    for word in words.split():
        candidate = (line + " " + word).strip()
        if line and draw.textlength(candidate, font=font(size, kind)) > width:
            text(draw, (x, y), line, size, color, kind)
            y += round(size * leading)
            line = word
        else:
            line = candidate
    if line:
        text(draw, (x, y), line, size, color, kind)
        y += round(size * leading)
    return y


def source_label(draw, x, y, words, color=SLATE):
    text(draw, (x + 14, y + 5), words, 18, color, "mono")


def base(dark=False):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), INK if dark else PAPER)
    draw = ImageDraw.Draw(canvas)
    color = PAPER if dark else INK
    for index, height in enumerate((11, 19, 27)):
        x = 72 + index * 10
        draw.rectangle((x, 67 - height, x + 5, 67), fill=GOLD)
    text(draw, (116, 36), "Council Lab", 26, color, "serif")
    text(draw, (673, 46), "WORKFLOW EXPLAINER / FICTIONAL CASE", 16,
         RULE if dark else MUTED, "mono")
    draw.line((72, 91, 1208, 91), fill="#394752" if dark else RULE, width=1)
    return canvas, draw


def record_excerpt(canvas, x, y, role, tag, quote, evidence=None, color=SLATE):
    """Typeset verbatim saved fields, rather than simulate an application UI."""
    draw = ImageDraw.Draw(canvas)
    width, height = 588, 390
    text(draw, (x + 32, y + 25), role + ".json", 19, MUTED, "mono")
    draw.line((x + 32, y + 65, x + width - 32, y + 65), fill=RULE)
    source_label(draw, x + 18, y + 87, tag, color)
    bottom = paragraph(draw, (x + 32, y + 145), quote, width - 64, size=31)
    if bottom > y + height - 52:
        raise ValueError("Recorded excerpt does not fit its document panel")
    if evidence:
        text(draw, (x + 32, y + height - 42), "evidence: " + ", ".join(evidence), 18, color, "mono")


def question(local):
    canvas, draw = base()
    p = ease(local / 0.85)
    x = round(72 - 40 * (1 - p))
    text(draw, (x, 147), "Think it", 79, kind="display")
    text(draw, (x, 244), "through.", 91, SLATE, "display")
    text(draw, (76, 411), "Your question. Your evidence.", 29)
    text(draw, (76, 463), "WITH CODEX", 19, MUTED, "mono")
    x, y = 659, round(162 + 35 * (1 - p))
    text(draw, (x, y), "YOU BRING THE INPUT", 18, MUTED, "mono")
    text(draw, (x, y + 65), "Question", 37, SLATE, "display")
    text(draw, (x, y + 119), "What should we do next?", 27)
    draw.line((x, y + 180, 1208, y + 180), fill=RULE)
    text(draw, (x, y + 212), "Evidence", 37, SLATE, "display")
    text(draw, (x, y + 266), "What do we know?", 27)
    text(draw, (x, y + 363), "Example: a library considers a quiet hour.", 19, MUTED)
    return canvas


def argument(local, challenge=False):
    canvas, draw = base()
    p = ease(local / 0.7)
    role = "skeptic" if challenge else "champion"
    claim = (SKEPTIC if challenge else CHAMPION)["claims"][0]
    color = INK if challenge else SLATE
    text(draw, (72, 147), "02" if challenge else "01", 19, color, "mono")
    text(draw, (72, 209), "Challenge" if challenge else "Build", 75, kind="display")
    text(draw, (72, 296), "the case.", 66, color, "display")
    text(draw, (76, 454), "SKEPTIC" if challenge else "CHAMPION", 19, MUTED, "mono")
    draw.line((76, 500, 505, 500), fill=RULE, width=2)
    end = round(76 + 429 * ease((local - 0.25) / 0.8))
    draw.line((76, 500, end, 500), fill=color, width=3)
    record_excerpt(canvas, round(620 + 65 * (1 - p)), 170, role,
             claim["id"], claim["statement"], claim["evidence"], color)
    return canvas


def judgment(local):
    canvas, draw = base()
    text(draw, (72, 143), "03  /  ELDER", 19, SLATE, "mono")
    text(draw, (72, 206), "Weigh", 85, kind="display")
    text(draw, (72, 302), "both.", 94, SLATE, "display")
    text(draw, (76, 462), "Find a next step.", 29)
    x = round(672 + 45 * (1 - ease(local / 0.65)))
    text(draw, (x, 174), "elder.json", 19, MUTED, "mono")
    draw.line((x, 226, 1208, 226), fill=RULE)
    text(draw, (x, 258), "THE SAVED JUDGMENT", 18, MUTED, "mono")
    text(draw, (x, 312), "More", 61, kind="display")
    text(draw, (x, 386), "observation.", 61, SLATE, "display")
    source_label(draw, x - 14, 484, ELDER["outcome"])
    return canvas


def saved_record(local):
    canvas, draw = base()
    text(draw, (72, 143), "THE LAB CHECKS AND SAVES", 19, SLATE, "mono")
    text(draw, (72, 205), "Keep the", 75, kind="display")
    text(draw, (72, 294), "reasoning.", 75, SLATE, "display")
    paragraph(draw, (76, 439), "You move responses between fresh Codex chats.", 475, 29)
    x = round(647 + 45 * (1 - ease(local / 0.65)))
    text(draw, (x, 158), "A RECORD YOU CAN INSPECT", 19, MUTED, "mono")
    for index, heading in enumerate((
        "Question + evidence",
        "Case + challenge",
        "Judgment + next step",
    )):
        y = 230 + index * 110
        draw.line((x, y + 82, 1208, y + 82), fill=RULE)
        text(draw, (x, y), "0" + str(index + 1), 20, SLATE, "mono")
        text(draw, (x + 72, y - 8), heading, 34, kind="display")
    return canvas


def human(local):
    canvas, draw = base(dark=True)
    p = ease(local / 0.8)
    text(draw, (72, round(171 + 22 * (1 - p))), "You", 85, PAPER, "display")
    text(draw, (72, round(272 + 22 * (1 - p))), "decide.", 98, PALE_SLATE, "display")
    text(draw, (78, 480), "The final call stays with you.", 28, PAPER)
    # The source is a visible next_step excerpt, not a second narration track.
    x = 735
    text(draw, (x, 177), "elder.json", 18, RULE, "mono")
    draw.line((x, 220, 1208, 220), fill="#46535E")
    text(draw, (x, 248), "next_step", 20, PALE_SLATE, "mono")
    excerpt = EDIT["next_step_excerpt"]
    if excerpt not in ELDER["next_step"]:
        raise ValueError("Next-step excerpt must be verbatim saved output")
    paragraph(draw, (x, 300), excerpt, 473, 30, PAPER)
    return canvas


SCENES = (question, argument, lambda t: argument(t, True), judgment, saved_record, human)


def frame(time):
    for index, cut in enumerate(EDIT["cuts"]):
        if time < cut["end"] or index == len(SCENES) - 1:
            return SCENES[index](max(0, time - cut["start"]))
    raise ValueError("Timeline does not cover this frame")


def stills():
    canvas, draw = base()
    text(draw, (72, 149), "Think it", 79, kind="display")
    text(draw, (72, 244), "through.", 91, SLATE, "display")
    text(draw, (78, 409), "One question. Three angles.", 28)
    text(draw, (78, 456), "A short guide to Council Lab.", 25, MUTED)
    record_excerpt(canvas, 620, 170, "champion", CHAMPION["claims"][0]["id"],
             CHAMPION["claims"][0]["statement"], ["E1"])
    canvas.save(MEDIA / "council-lab-poster.jpg", quality=94, subsampling=0)
    sheet = Image.new("RGB", (WIDTH * 3, HEIGHT), PAPER)
    for index, time in enumerate(EDIT["storyboard_keyframes"]):
        sheet.paste(frame(time), (WIDTH * index, 0))
    sheet.resize((1920, 360), Image.Resampling.LANCZOS).save(
        MEDIA / "council-lab-storyboard.jpg", quality=92, subsampling=0)
    for time in EDIT["review_keyframes"]:
        frame(time).save(MEDIA / ("review-" + str(time).replace(".", "-") + ".jpg"), quality=92)


def audio_filter(ffmpeg):
    source = MEDIA / "audio/narration-original.mp3"
    measure = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(source), "-af",
         "loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    stats, _ = json.JSONDecoder().raw_decode(measure.stderr[measure.stderr.rfind("{"):])
    normalization = (
        "loudnorm=I=-16:TP=-1.5:LRA=7:"
        f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true"
    )
    return normalization + f",adelay={round(EDIT['narration_start_seconds'] * 1000)},apad"


def render(ffmpeg):
    voice = MEDIA / "audio/narration-original.mp3"
    filters = audio_filter(ffmpeg)
    with tempfile.TemporaryDirectory(prefix=".render-", dir=MEDIA) as folder:
        target = Path(folder) / "film.mp4"
        args = [
            ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-pixel_format",
            "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}", "-framerate", str(FPS),
            "-i", "pipe:0", "-i", str(voice), "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
            "-af", filters, "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "160k",
            "-t", str(SECONDS), "-map_metadata", "-1", "-movflags", "+faststart", str(target),
        ]
        process = subprocess.Popen(args, stdin=subprocess.PIPE)
        try:
            for number in range(round(FPS * SECONDS)):
                process.stdin.write(frame(number / FPS).tobytes())
                if number % 120 == 0:
                    print(f"Rendered {number}/{round(FPS * SECONDS)} frames", flush=True)
            process.stdin.close()
            if process.wait() != 0:
                raise RuntimeError("FFmpeg did not encode the film successfully")
            os.replace(target, MEDIA / EDIT["movie"])
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg")
    parser.add_argument("--stills-only", action="store_true")
    args = parser.parse_args()
    stills()
    if not args.stills_only:
        ffmpeg = args.ffmpeg or shutil.which("ffmpeg")
        if not ffmpeg:
            import imageio_ffmpeg
            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        render(ffmpeg)


if __name__ == "__main__":
    main()
