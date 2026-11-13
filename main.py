"""Entry for the make.fun bounty ai-happy-01 ("Make the AI judge happy").

Writes one image to <output dir>/entry.png: the picture stored next to this
file, copied byte for byte. Standard library only, no network, no clock and
no randomness, so every run writes the same bytes.

The picture: a grandfather dancing in a sunny kitchen with his granddaughter,
who stands on his slippers, while the dog dances along on its hind legs and
the grandmother sings into a wooden spoon.

The output directory is /output, or $MAKEFUN_OUTPUT_DIR when that is set.
Exit code 0 on success, 1 when the stored picture breaks the bounty's limits.
"""

import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUTPUT_NAME = "entry.png"

MAX_BYTES = 1_048_576  # 1 MiB, the bounty's file limit
MAX_SIDE = 1024  # pixels, for both width and height
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_END = b"\x00\x00\x00\x00IEND\xaeB`\x82"  # the closing chunk with its checksum
JPEG_MAGIC = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"  # the end-of-image marker


def png_size(data: bytes) -> tuple[int, int] | None:
    """Width and height from the IHDR chunk, which must be a PNG's first chunk."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_size(data: bytes) -> tuple[int, int] | None:
    """Width and height from the first frame header (SOF segment) of a JPEG."""
    pos = 2  # skip the start-of-image marker
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker == 0xFF:  # a fill byte before the real marker
            pos += 1
            continue
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:  # markers with no length
            pos += 2
            continue
        (length,) = struct.unpack(">H", data[pos + 2:pos + 4])
        # C0..CF are frame headers, except C4 (Huffman tables), C8 and CC.
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            if pos + 9 > len(data):
                return None
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    return None


def fail(message: str) -> int:
    """Report a problem on stderr and give the exit code for it."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not SOURCE.is_file():
        return fail(f"image not found: {SOURCE}")
    data = SOURCE.read_bytes()
    if not data.startswith((PNG_MAGIC, JPEG_MAGIC)):
        return fail("image is neither a PNG nor a JPEG")
    if len(data) > MAX_BYTES:
        return fail(f"image is {len(data)} bytes, over the {MAX_BYTES} limit")
    is_png = data.startswith(PNG_MAGIC)
    # A whole image: a PNG closes with its IEND chunk, a JPEG with its end marker.
    if not data.endswith(PNG_END if is_png else JPEG_END):
        return fail("image is cut short, its end marker is missing")
    size = png_size(data) if is_png else jpeg_size(data)
    if size is None:
        return fail("cannot read the image size from its header")
    width, height = size
    if width < 1 or height < 1 or width > MAX_SIDE or height > MAX_SIDE:
        return fail(f"image is {width}x{height}, outside 1..{MAX_SIDE} pixels a side")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / OUTPUT_NAME
    # Write a side file and rename it, so a half-written entry.png never exists.
    partial = OUTPUT_DIR / (OUTPUT_NAME + ".part")
    partial.write_bytes(data)
    os.replace(partial, target)
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
