"""
Recursive Fractal Tree using matplotlib (headless-capable).

Draws a binary tree fractal where each branch splits into two smaller
branches at a given angle, recursively, until a minimum branch length
is reached. Saves the result to fractal_tree.png.
"""

import math
import matplotlib
matplotlib.use("Agg")          # headless backend — no display required
import matplotlib.pyplot as plt
import matplotlib.collections as mc

# ── Configuration ────────────────────────────────────────────────────────────
TRUNK_LENGTH = 150   # pixels for the first branch
ANGLE        = 25    # degrees each branch splits by
MAX_DEPTH    = 11    # recursion depth (increase for more detail)
SHRINK       = 0.68  # each child branch is this fraction of its parent
OUTPUT_FILE  = "fractal_tree.png"
# ─────────────────────────────────────────────────────────────────────────────


def draw_branch(segments, x, y, angle_deg, length, depth):
    """
    Recursively collect line segments for the fractal tree.

    Args:
        segments:  list to append (x0, y0, x1, y1, depth) tuples
        x, y:      start point of this branch
        angle_deg: current heading in degrees (90 = straight up)
        length:    length of this branch
        depth:     remaining recursion depth
    """
    if depth == 0 or length < 1:
        return

    angle_rad = math.radians(angle_deg)
    x2 = x + length * math.cos(angle_rad)
    y2 = y + length * math.sin(angle_rad)

    segments.append(((x, y), (x2, y2), depth))

    draw_branch(segments, x2, y2, angle_deg - ANGLE, length * SHRINK, depth - 1)
    draw_branch(segments, x2, y2, angle_deg + ANGLE, length * SHRINK, depth - 1)


def depth_to_color(depth):
    """Map recursion depth to an RGB colour (brown trunk → green leaves)."""
    t = depth / MAX_DEPTH          # 1.0 at trunk, 0.0 at tips
    r = t * (139 / 255)
    g = (1 - t) * (200 / 255) + t * (55 / 255)
    b = 0.0
    return (r, g, b)


def main():
    segments = []
    draw_branch(segments, 0, 0, 90, TRUNK_LENGTH, MAX_DEPTH)

    fig, ax = plt.subplots(figsize=(10, 12), facecolor="black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")

    # Group segments by depth for efficient batch rendering
    from collections import defaultdict
    by_depth = defaultdict(list)
    for (x0, y0), (x1, y1), depth in segments:
        by_depth[depth].append([(x0, y0), (x1, y1)])

    for depth, lines in by_depth.items():
        lc = mc.LineCollection(
            lines,
            colors=[depth_to_color(depth)],
            linewidths=max(0.5, depth * 0.5),
        )
        ax.add_collection(lc)

    ax.autoscale()
    plt.tight_layout(pad=0)
    plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight",
                facecolor="black", format="PNG")
    plt.close()
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
