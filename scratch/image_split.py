"""Quad-tree splitting: one image -> 4**depth tiles.

Pure image math and no HTTP. app.py owns the wire format, the same way
rag_service owns answering and app.py owns the /ask contract.
"""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass

from PIL import Image, UnidentifiedImageError

# depth 4 is 256 tiles. Past that a single request turns into a
# denial-of-service against our own process, so the API refuses.
MAX_DEPTH = 4

# A quadrant cannot be split below 1px, so recursion stops here
# regardless of the depth asked for.
MIN_SPLITTABLE = 2

Box = tuple[int, int, int, int]  # left, top, right, bottom


class UnreadableImage(Exception):
    """Upload was not an image we can decode."""


@dataclass(frozen=True)
class Tile:
    # "nw/se" reads as: north-west quadrant, then its south-east quadrant.
    # The path is the reassembly key — depth is len(path.split("/")).
    path: str
    x: int
    y: int
    width: int
    height: int
    png_b64: str


def _quadrants(box: Box) -> tuple[tuple[str, Box], ...]:
    left, top, right, bottom = box
    # Floor division, with the right/bottom halves absorbing the odd pixel.
    # Tiles stay gapless and non-overlapping on odd dimensions.
    mid_x = left + (right - left) // 2
    mid_y = top + (bottom - top) // 2
    return (
        ("nw", (left, top, mid_x, mid_y)),
        ("ne", (mid_x, top, right, mid_y)),
        ("sw", (left, mid_y, mid_x, bottom)),
        ("se", (mid_x, mid_y, right, bottom)),
    )


def _leaves(box: Box, depth: int, path: str):
    left, top, right, bottom = box
    too_small = (right - left) < MIN_SPLITTABLE or (bottom - top) < MIN_SPLITTABLE
    if depth == 0 or too_small:
        yield path, box
        return
    for name, sub in _quadrants(box):
        yield from _leaves(sub, depth - 1, f"{path}/{name}" if path else name)


def _as_png_b64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def split_image(data: bytes, depth: int) -> tuple[list[Tile], int, int]:
    """Split raw image bytes into quad-tree tiles.

    Returns the tiles plus the source width and height.
    """
    try:
        image = Image.open(io.BytesIO(data))
        image.load()  # force the decode now, so corrupt files fail here
    except UnidentifiedImageError as exc:
        raise UnreadableImage("not a recognised image format") from exc
    except Image.DecompressionBombError as exc:
        raise UnreadableImage("image dimensions exceed the safety limit") from exc
    except OSError as exc:
        raise UnreadableImage("image data is truncated or corrupt") from exc

    # PNG cannot store CMYK or YCbCr; normalise those before encoding.
    if image.mode not in ("RGB", "RGBA", "L", "LA", "P"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

    width, height = image.size
    tiles = [
        Tile(
            path=path,
            x=box[0],
            y=box[1],
            width=box[2] - box[0],
            height=box[3] - box[1],
            png_b64=_as_png_b64(image.crop(box)),
        )
        for path, box in _leaves((0, 0, width, height), depth, "")
    ]
    return tiles, width, height
