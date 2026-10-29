"""Check the published media contract without installing rendering dependencies."""
import hashlib
import json
from pathlib import Path
import struct
import unittest

MEDIA = Path(__file__).resolve().parents[1] / "media"


def movie_duration(data):
    def boxes(start, end):
        while start + 8 <= end:
            size, kind = struct.unpack_from(">I4s", data, start)
            header = 8
            if size == 1:
                size = struct.unpack_from(">Q", data, start + 8)[0]
                header = 16
            if size == 0:
                size = end - start
            if size < header or start + size > end:
                raise ValueError("Invalid MP4 box")
            payload = start + header
            if kind == b"moov":
                found = boxes(payload, start + size)
                if found is not None:
                    return found
            elif kind == b"mvhd":
                version = data[payload]
                if version == 0:
                    scale, duration = struct.unpack_from(">II", data, payload + 12)
                elif version == 1:
                    scale = struct.unpack_from(">I", data, payload + 20)[0]
                    duration = struct.unpack_from(">Q", data, payload + 24)[0]
                else:
                    raise ValueError("Unknown movie-header version")
                return duration / scale
            start += size
        return None
    return boxes(0, len(data))


class MediaTests(unittest.TestCase):
    def test_published_film_is_under_thirty_seconds_and_matches_manifest(self):
        manifest = json.loads((MEDIA / "manifest.json").read_text(encoding="utf-8"))
        for name, expected in manifest["sha256"].items():
            self.assertEqual(hashlib.sha256((MEDIA / name).read_bytes()).hexdigest(), expected, name)
        data = (MEDIA / "council-lab-26s.mp4").read_bytes()
        self.assertLess(len(data), 10_000_000)
        duration = movie_duration(data)
        self.assertIsNotNone(duration)
        self.assertGreater(duration, 0)
        self.assertLess(duration, 30)
        self.assertEqual(duration, manifest["duration_seconds"])


if __name__ == "__main__":
    unittest.main()
