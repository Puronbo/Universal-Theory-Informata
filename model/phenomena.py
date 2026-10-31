"""Phenomena map: classify phenomena by canvas operation."""

from __future__ import annotations

PHENOMENA = {
    "light": {"operation": "fold", "face": "exterior", "scale": "all", "speed": "c"},
    "dark_energy": {"operation": "unfold", "face": "canvas", "scale": "cosmic", "speed": "cosmic"},
    "sound": {
        "operation": "vibration",
        "face": "exterior_matter",
        "scale": "macro",
        "speed": "sub-c",
    },
    "gravity": {
        "operation": "stretch",
        "face": "canvas_geometry",
        "scale": "all",
        "speed": "instantaneous",
    },
    "matter": {"operation": "contact", "face": "exterior", "scale": "all", "speed": "varies"},
    "consciousness": {
        "operation": "interior",
        "face": "interior",
        "scale": "biological",
        "speed": "neural_frame_rate",
    },
    "erosion": {"operation": "erode", "face": "canvas", "scale": "all", "speed": "scale_dependent"},
    "stroboscopic_now": {
        "operation": "sample",
        "face": "playhead",
        "scale": "neural",
        "speed": "frame_rate",
    },
}


def phenomenon_type(name: str) -> str:
    """Return the canvas operation for a phenomenon."""
    info = PHENOMENA.get(name.lower())
    if info is None:
        raise ValueError(f"unknown phenomenon: {name}")
    return info["operation"]


def phenomena_list() -> list[str]:
    """Return the list of known phenomena."""
    return list(PHENOMENA.keys())
