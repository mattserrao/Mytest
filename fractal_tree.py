"""
Recursive Fractal Tree using Python's turtle library.

Draws a binary tree fractal where each branch splits into two smaller branches
at a given angle, recursively, until a minimum branch length is reached.
"""

import turtle


def draw_branch(t, length, angle, depth):
    """
    Recursively draw a fractal tree branch.

    Args:
        t:      turtle object
        length: length of the current branch
        angle:  angle (in degrees) between parent and child branches
        depth:  remaining recursion depth
    """
    if depth == 0 or length < 2:
        return

    # Color shifts from brown (trunk) to green (leaves) as depth decreases
    green = min(255, int((1 - depth / MAX_DEPTH) * 200 + 55))
    red   = max(0,   int(depth / MAX_DEPTH * 139))
    t.pencolor(red, green, 0)
    t.pensize(max(1, depth))

    # Draw this branch
    t.forward(length)

    # -- Right sub-branch --
    t.right(angle)
    draw_branch(t, length * SHRINK, angle, depth - 1)

    # -- Left sub-branch (swing back past centre then return) --
    t.left(angle * 2)
    draw_branch(t, length * SHRINK, angle, depth - 1)

    # Return to the base of this branch
    t.right(angle)
    t.backward(length)


# ── Configuration ────────────────────────────────────────────────────────────
TRUNK_LENGTH = 120   # pixels for the first branch
ANGLE        = 25    # degrees each branch splits by
MAX_DEPTH    = 10    # recursion depth  (increase for more detail)
SHRINK       = 0.7   # each child branch is this fraction of its parent
# ─────────────────────────────────────────────────────────────────────────────


def main():
    screen = turtle.Screen()
    screen.title("Recursive Fractal Tree")
    screen.bgcolor("black")
    screen.colormode(255)
    screen.tracer(0)          # turn off animation for speed

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.left(90)                # point upward
    t.penup()
    t.goto(0, -screen.window_height() // 2 + 20)   # start near bottom centre
    t.pendown()

    draw_branch(t, TRUNK_LENGTH, ANGLE, MAX_DEPTH)

    screen.update()           # render everything at once
    screen.mainloop()


if __name__ == "__main__":
    main()
