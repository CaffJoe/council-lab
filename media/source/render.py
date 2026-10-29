"""Render Council Lab's 26-second illustrated overview. Optional media tooling only."""
import argparse
from functools import lru_cache
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

MEDIA = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT, FPS, SECONDS = 1280, 720, 30, 26
INK = (27, 27, 19, 255)
PAPER = (237, 220, 169, 255)
OLIVE = (80, 87, 47, 255)


def smooth(value):
    value = min(1.0, max(0.0, value))
    return value * value * (3 - 2 * value)


def mix(a, b, value):
    return a + (b - a) * value


def font(size, serif=False):
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    choices = ([windows / "georgia.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")]
               if serif else [windows / "calibri.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")])
    for choice in choices:
        if choice.exists():
            return ImageFont.truetype(str(choice), size)
    raise RuntimeError("Install Georgia/Calibri or DejaVu Serif/Sans to render the film")


@lru_cache(maxsize=32)
def typeface(size, serif=False):
    return font(size, serif)


def asset(name, size):
    original = Image.open(MEDIA / "art" / name).convert("RGBA")
    bounds = original.getchannel("A").point(lambda value: 255 if value > 128 else 0).getbbox()
    return original.crop(bounds).resize(size, Image.Resampling.LANCZOS)


BACKGROUND = ImageOps.fit(Image.open(MEDIA / "art/library-stage.png").convert("RGBA"), (WIDTH, HEIGHT))
BODY = asset("librarian.png", (260, 396))
UPPER = asset("upper-arm.png", (56, 170))
FOREARM = asset("forearm-hand.png", (206, 46))


def line(draw, xy, text, size, fill=INK, serif=False):
    draw.text(xy, text, font=typeface(size, serif), fill=fill, stroke_width=0)


def limb(canvas, sprite, source_start, source_end, start, end):
    source_angle = math.atan2(source_end[1] - source_start[1], source_end[0] - source_start[0])
    angle = math.atan2(end[1] - start[1], end[0] - start[0]) - source_angle
    rotated = sprite.rotate(-math.degrees(angle), resample=Image.Resampling.BICUBIC, expand=True)
    dx, dy = source_start[0] - sprite.width / 2, source_start[1] - sprite.height / 2
    pivot = (rotated.width / 2 + math.cos(angle) * dx - math.sin(angle) * dy,
             rotated.height / 2 + math.sin(angle) * dx + math.cos(angle) * dy)
    canvas.alpha_composite(rotated, (round(start[0] - pivot[0]), round(start[1] - pivot[1])))


def arm(canvas, shoulder, hand):
    dx, dy = hand[0] - shoulder[0], hand[1] - shoulder[1]
    distance = math.hypot(dx, dy)
    upper, lower = 130.0, 186.0
    if not abs(upper - lower) < distance < upper + lower:
        raise ValueError("Hand target is outside the articulated arm's reach")
    along = (upper * upper - lower * lower + distance * distance) / (2 * distance)
    height = math.sqrt(max(0, upper * upper - along * along))
    elbow = (shoulder[0] + along * dx / distance + height * dy / distance,
             shoulder[1] + along * dy / distance - height * dx / distance)
    limb(canvas, UPPER, (28, 20), (28, 150), shoulder, elbow)
    limb(canvas, FOREARM, (196, 23), (10, 23), elbow, hand)


@lru_cache(maxsize=12)
def paper(kind, side):
    sheet = Image.new("RGBA", (192, 152), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    draw.polygon([(7, 7), (184, 3), (188, 143), (3, 147)], fill=PAPER, outline=INK, width=2)
    line(draw, (17, 15), {"evidence": "E1" if side == 0 else "E2", "argument": "A CASE FOR" if side == 0 else "A CHALLENGE", "unknown": "STILL UNKNOWN", "next": "A HUMAN CHECK"}[kind], 13, OLIVE)
    if kind == "evidence":
        line(draw, (17, 34), "12" if side == 0 else "20", 51, serif=True)
        line(draw, (18, 96), "requests for quiet" if side == 0 else "people needed help", 18)
    else:
        words = {
            ("argument", 0): ["Could one", "room help?"],
            ("argument", 1): ["Who might", "lose access?"],
            ("unknown", 0): ["Demand?", "Room access?"],
            ("unknown", 1): ["Can ordinary", "help continue?"],
            ("next", 0): ["Check", "access."],
            ("next", 1): ["Ask", "visitors."],
        }[(kind, side)]
        for index, text in enumerate(words):
            line(draw, (17, 48 + index * 31), text, 25, serif=True)
    return sheet


def card(canvas, center, kind, side, angle=0, paint=True, fold=1.0):
    sheet = paper(kind, side)
    sheet = sheet.resize((max(8, round(sheet.width * fold)), sheet.height), Image.Resampling.LANCZOS)
    theta = -math.radians(angle)
    # Turn around the held edge so the fingertip stays on the paper throughout a flip.
    hinge_shift = 86 * (1 - fold)
    center = (center[0] + math.cos(theta) * hinge_shift,
              center[1] + math.sin(theta) * hinge_shift)
    tilted = sheet.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    position = (round(center[0] - tilted.width / 2), round(center[1] - tilted.height / 2))
    # A fingertip remains attached to the upper-right paper edge during movement.
    grip_dx, grip_dy = 86 * fold, -35
    grip = (center[0] + math.cos(theta) * grip_dx - math.sin(theta) * grip_dy,
            center[1] + math.sin(theta) * grip_dx + math.cos(theta) * grip_dy)
    if not paint:
        return grip
    shadow = Image.new("RGBA", tilted.size, (0, 0, 0, 0))
    shadow.putalpha(tilted.getchannel("A").point(lambda value: value // 4))
    canvas.alpha_composite(shadow, (position[0] + 4, position[1] + 6))
    canvas.alpha_composite(tilted, position)
    return grip


def scene(time):
    canvas = BACKGROUND.copy()
    canvas.alpha_composite(BODY, (1000, 146))
    # The original counter occludes the waist; the sleeves and papers perform above it.
    foreground = BACKGROUND.crop((0, 544, WIDTH, HEIGHT))
    canvas.alpha_composite(foreground, (0, 544))
    left_lift = smooth((time - 3.7) / 2.1)
    right_lift = smooth((time - 6.2) / 1.8)
    kind = "evidence" if time < 9.35 else "argument" if time < 15.35 else "unknown" if time < 20.85 else "next"
    fold = 1.0
    for turn in (9, 15, 20.5):
        if turn <= time <= turn + 0.7:
            fold = max(0.04, abs(math.cos(math.pi * (time - turn) / 0.7)))
    compare = smooth((time - 9) / 1.4) * (1 - smooth((time - 15) / 1.4))
    place = smooth((time - 22) / 1.8)
    centers = [(mix(830, 695, left_lift), mix(552, 455, left_lift) + 38 * place),
               (mix(1020, 927, right_lift), mix(552, 455, right_lift) + 38 * place)]
    centers = [(centers[0][0] + 28 * compare, centers[0][1] - 10 * compare),
               (centers[1][0] - 10 * compare, centers[1][1] - 10 * compare)]
    left_hand, right_hand = (910, 517), (1110, 517)
    if time >= 3.7:
        left_hand = card(canvas, centers[0], kind, 0, 3 * left_lift, paint=False, fold=fold)
    if time >= 6.2:
        right_hand = card(canvas, centers[1], kind, 1, -3 * right_lift, paint=False, fold=fold)
    arm(canvas, (1028, 383), left_hand)
    arm(canvas, (1205, 383), right_hand)
    if time >= 3.7:
        card(canvas, centers[0], kind, 0, 3 * left_lift, fold=fold)
    if time >= 6.2:
        card(canvas, centers[1], kind, 1, -3 * right_lift, fold=fold)
    # Match cuts between the same actions keep the stage grounded.
    if 9 <= time < 20.5:
        canvas = canvas.crop((64, 36, WIDTH, HEIGHT)).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return canvas


def frame(time, poster=False):
    canvas = scene(time)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    line(draw, (350, 66), "COUNCIL LAB  /  A FICTIONAL LIBRARY EXAMPLE", 16, OLIVE)
    if poster:
        title, subtitle = ["Council Lab"], ["One question.", "More than one angle."]
    elif time < 4:
        title, subtitle = ["A quieter hour?"], ["How could a library help more people?"]
    elif time < 9:
        title, subtitle = ["Start with", "the evidence."], ["Two tallies. The same four Tuesdays."]
    elif time < 15:
        title, subtitle = ["Make a case.", "Challenge it."], ["Two angles on the same question."]
    elif time < 20.5:
        title, subtitle = ["Keep the unknowns", "visible."], ["Demand. Access. Existing help."]
    else:
        title, subtitle = ["Council Lab"], ["Check access. Ask visitors.", "Then choose what to try."]
    y = 105
    for text in title:
        line(draw, (348, y), text, 48 if len(text) < 19 else 41, serif=True)
        y += 57
    for text in subtitle:
        line(draw, (351, y + 10), text, 25)
        y += 31
    draw.rectangle((0, 642, WIDTH, HEIGHT), fill=(20, 23, 16, 247))
    footer = "ILLUSTRATED FICTIONAL EXAMPLE  /  NOT A LIVE CODEX RUN"
    line(draw, (38, 686), footer, 14, PAPER)
    if poster:
        draw.ellipse((1110, 560, 1182, 632), fill=PAPER, outline=INK, width=2)
        draw.polygon([(1140, 580), (1140, 611), (1162, 595)], fill=INK)
        line(draw, (38, 653), "WATCH THE 26-SECOND FILM", 20, PAPER)
    elif time >= 20.5:
        line(draw, (38, 653), "Try the example. Change the question.   github.com/CaffJoe/council-lab", 23, PAPER)
    else:
        caption = ("A practical question. More than one angle." if time < 4 else
                   "Keep sources attached to what is claimed." if time < 9 else
                   "The challenge responds to the actual supporting case." if time < 15 else
                   "A useful judgment says what remains uncertain.")
        line(draw, (38, 653), caption, 23, PAPER)
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    if time < 0.35:
        canvas = Image.blend(Image.new("RGB", canvas.size, (20, 23, 16)), canvas, smooth(time / 0.35))
    return canvas


def soundtrack(path):
    rate = 48000
    times = np.arange(rate * SECONDS, dtype=np.float64) / rate
    sound = np.zeros_like(times)
    for at, note in [(0.3, 146.83), (4, 196.0), (9, 174.61), (15, 130.81), (20.5, 196.0), (23, 293.66)]:
        age = np.maximum(0, times - at)
        envelope = (times >= at) * (1 - np.exp(-age * 9)) * np.exp(-age / 2.4)
        sound += envelope * (np.sin(2 * np.pi * note * age) + 0.18 * np.sin(2 * np.pi * note * 2 * age)) * 0.07
    sound *= np.minimum(1, np.maximum(0, (SECONDS - times) / 1.4))
    stereo = np.column_stack((sound, sound * 0.97))
    samples = np.clip(stereo * 32767, -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(rate)
        output.writeframes(samples.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stills-only", action="store_true")
    parser.add_argument("--ffmpeg", help="Path to ffmpeg, otherwise use PATH or imageio-ffmpeg")
    args = parser.parse_args()
    frame(11, poster=True).save(MEDIA / "council-lab-poster.jpg", quality=94)
    strip = Image.new("RGB", (1280, 240), (20, 23, 16))
    for index, at in enumerate((7.8, 12, 18)):
        still = frame(at).resize((426, 240), Image.Resampling.LANCZOS)
        strip.paste(still, (index * 427, 0))
    strip.save(MEDIA / "council-lab-storyboard.jpg", quality=94)
    for at in (0.6, 4.4, 6.2, 8, 12, 18, 23, 25.9):
        frame(at).save(MEDIA / f"review-{str(at).replace('.', '-')}.jpg", quality=88)
    if args.stills_only:
        return
    binary = args.ffmpeg or shutil.which("ffmpeg")
    if not binary:
        import imageio_ffmpeg
        binary = imageio_ffmpeg.get_ffmpeg_exe()
    with tempfile.TemporaryDirectory(dir=MEDIA, prefix=".render-") as temporary:
        audio = Path(temporary) / "original-score.wav"
        rendered = Path(temporary) / "film.mp4"
        soundtrack(audio)
        command = [binary, "-y", "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
                   "-framerate", str(FPS), "-i", "pipe:0", "-i", str(audio), "-c:v", "libx264", "-crf", "21",
                   "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", str(SECONDS),
                   "-movflags", "+faststart", str(rendered)]
        with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
            for number in range(FPS * SECONDS):
                process.stdin.write(frame(number / FPS).tobytes())
                if number % (FPS * 5) == 0:
                    print(f"Rendered {number // FPS}/{SECONDS} seconds", flush=True)
            process.stdin.close()
            if process.wait() != 0:
                raise RuntimeError("ffmpeg failed")
        rendered.replace(MEDIA / "council-lab-26s.mp4")


if __name__ == "__main__":
    main()
