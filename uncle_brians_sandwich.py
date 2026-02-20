"""
Uncle Brian's Sandwich - A stick figure dancing and eating animation.
Run: python uncle_brians_sandwich.py
Saves to: uncle_brians_sandwich.gif
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


def draw_stick_figure(ax, frame, total_frames):
    """Draw a stick figure that dances and eats a sandwich."""
    ax.clear()
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 4)
    ax.set_aspect("equal")
    ax.set_facecolor("#87CEEB")
    ax.set_title("Uncle Brian's Sandwich", fontsize=18, fontweight="bold",
                 color="#8B4513", pad=15)

    # Ground
    ax.fill_between([-3, 3], [-3, -3], [-1.8, -1.8], color="#228B22")
    ax.plot([-3, 3], [-1.8, -1.8], color="#006400", linewidth=2)

    # Dance cycle phase
    t = (frame / total_frames) * 2 * np.pi * 3  # 3 full dance cycles
    dance_phase = frame % 20  # for discrete pose switching

    # Body sway
    sway = 0.3 * np.sin(t)
    bounce = 0.15 * abs(np.sin(t * 2))

    # Base positions
    body_x = sway
    body_base_y = -0.5 + bounce
    head_y = body_base_y + 1.8
    shoulder_y = body_base_y + 1.2
    hip_y = body_base_y

    # --- HEAD ---
    head = plt.Circle((body_x, head_y), 0.4, fill=True,
                       facecolor="#FFDAB9", edgecolor="black", linewidth=2)
    ax.add_patch(head)

    # Eyes
    eye_offset = 0.12
    ax.plot(body_x - eye_offset, head_y + 0.05, "ko", markersize=4)
    ax.plot(body_x + eye_offset, head_y + 0.05, "ko", markersize=4)

    # Mouth - opens and closes for eating
    eat_cycle = frame % 16
    if eat_cycle < 8:
        # Mouth open (eating!)
        mouth_open = 0.06 * (eat_cycle if eat_cycle < 4 else 8 - eat_cycle)
        mouth = patches.Arc((body_x, head_y - 0.1), 0.2, 0.1 + mouth_open,
                            angle=0, theta1=200, theta2=340,
                            linewidth=2, color="black")
        ax.add_patch(mouth)
        # Open mouth fill
        if mouth_open > 0.02:
            ax.plot(body_x, head_y - 0.15, "o", color="#8B0000",
                    markersize=2 + mouth_open * 20)
    else:
        # Smile
        mouth = patches.Arc((body_x, head_y - 0.1), 0.2, 0.12,
                            angle=0, theta1=200, theta2=340,
                            linewidth=2, color="black")
        ax.add_patch(mouth)

    # --- BODY ---
    ax.plot([body_x, body_x], [shoulder_y, hip_y],
            color="black", linewidth=3)

    # --- LEGS --- (dancing!)
    leg_angle = 0.4 * np.sin(t)
    # Left leg
    left_knee_x = body_x - 0.3 + 0.2 * np.sin(t)
    left_knee_y = hip_y - 0.6
    left_foot_x = body_x - 0.4 + 0.3 * np.sin(t + 0.5)
    left_foot_y = -1.8
    ax.plot([body_x, left_knee_x], [hip_y, left_knee_y],
            color="black", linewidth=3)
    ax.plot([left_knee_x, left_foot_x], [left_knee_y, left_foot_y],
            color="black", linewidth=3)

    # Right leg
    right_knee_x = body_x + 0.3 - 0.2 * np.sin(t)
    right_knee_y = hip_y - 0.6
    right_foot_x = body_x + 0.4 - 0.3 * np.sin(t + 0.5)
    right_foot_y = -1.8
    ax.plot([body_x, right_knee_x], [hip_y, right_knee_y],
            color="black", linewidth=3)
    ax.plot([right_knee_x, right_foot_x], [right_knee_y, right_foot_y],
            color="black", linewidth=3)

    # Shoes
    ax.plot(left_foot_x, left_foot_y, "s", color="#4A2800", markersize=8)
    ax.plot(right_foot_x, right_foot_y, "s", color="#4A2800", markersize=8)

    # --- ARMS ---
    # Left arm waves in the air while dancing
    left_arm_angle = 0.8 + 0.5 * np.sin(t * 1.5)
    left_elbow_x = body_x - 0.5 * np.cos(left_arm_angle)
    left_elbow_y = shoulder_y + 0.4 * np.sin(left_arm_angle)
    left_hand_x = left_elbow_x - 0.3 * np.cos(left_arm_angle + 0.5)
    left_hand_y = left_elbow_y + 0.4 * np.sin(left_arm_angle + 0.5)
    ax.plot([body_x, left_elbow_x], [shoulder_y, left_elbow_y],
            color="black", linewidth=3)
    ax.plot([left_elbow_x, left_hand_x], [left_elbow_y, left_hand_y],
            color="black", linewidth=3)

    # Right arm holds sandwich up to mouth
    sandwich_bob = 0.08 * np.sin(t * 2)
    right_elbow_x = body_x + 0.35
    right_elbow_y = shoulder_y + 0.1
    right_hand_x = body_x + 0.2
    right_hand_y = head_y - 0.25 + sandwich_bob
    ax.plot([body_x, right_elbow_x], [shoulder_y, right_elbow_y],
            color="black", linewidth=3)
    ax.plot([right_elbow_x, right_hand_x], [right_elbow_y, right_hand_y],
            color="black", linewidth=3)

    # --- SANDWICH ---
    sw_x = right_hand_x + 0.05
    sw_y = right_hand_y + 0.05

    # Bite animation - sandwich gets smaller periodically
    bite_phase = (frame // 30) % 4
    sw_width = 0.55 - 0.05 * bite_phase
    sw_height = 0.28

    # Bottom bread
    bread_bottom = patches.FancyBboxPatch(
        (sw_x - sw_width / 2, sw_y - sw_height / 2),
        sw_width, sw_height * 0.35,
        boxstyle="round,pad=0.02",
        facecolor="#D2691E", edgecolor="#8B4513", linewidth=1.5
    )
    ax.add_patch(bread_bottom)

    # Lettuce
    lettuce_y = sw_y - sw_height / 2 + sw_height * 0.3
    for i in range(5):
        lx = sw_x - sw_width / 2 + (sw_width / 4) * i
        lettuce = patches.Ellipse((lx, lettuce_y), 0.15, 0.06,
                                   facecolor="#32CD32", edgecolor="#228B22",
                                   linewidth=0.5)
        ax.add_patch(lettuce)

    # Filling (ham/cheese layers)
    filling = patches.FancyBboxPatch(
        (sw_x - sw_width / 2 + 0.02, sw_y - 0.02),
        sw_width - 0.04, sw_height * 0.25,
        boxstyle="round,pad=0.01",
        facecolor="#FFB6C1", edgecolor="#CD5C5C", linewidth=1
    )
    ax.add_patch(filling)

    cheese = patches.FancyBboxPatch(
        (sw_x - sw_width / 2 + 0.01, sw_y + 0.02),
        sw_width - 0.02, sw_height * 0.15,
        boxstyle="round,pad=0.01",
        facecolor="#FFD700", edgecolor="#DAA520", linewidth=1
    )
    ax.add_patch(cheese)

    # Top bread
    bread_top = patches.FancyBboxPatch(
        (sw_x - sw_width / 2, sw_y + sw_height * 0.15),
        sw_width, sw_height * 0.35,
        boxstyle="round,pad=0.03",
        facecolor="#DEB887", edgecolor="#8B4513", linewidth=1.5
    )
    ax.add_patch(bread_top)

    # --- CRUMBS falling ---
    np.random.seed(frame // 4)
    if eat_cycle < 8:
        for _ in range(3):
            cx = sw_x + np.random.uniform(-0.3, 0.3)
            cy = sw_y - 0.3 - np.random.uniform(0, 1.5) * ((frame % 8) / 8)
            ax.plot(cx, cy, ".", color="#D2691E",
                    markersize=np.random.randint(2, 5))

    # --- MUSIC NOTES floating around ---
    for i in range(3):
        note_t = t + i * 2.1
        nx = body_x - 1.2 + 0.5 * np.sin(note_t * 0.7 + i)
        ny = 1.5 + 0.8 * np.sin(note_t * 0.4 + i * 1.5) + i * 0.5
        note_size = 12 + 3 * np.sin(note_t + i)
        alpha = 0.4 + 0.3 * abs(np.sin(note_t * 0.5 + i))
        ax.text(nx, ny, "\u266B", fontsize=note_size, color="#FF1493",
                alpha=alpha, ha="center", va="center", fontweight="bold")

    # --- SPEECH BUBBLE ---
    bubble_cycle = (frame // 40) % 3
    messages = ["Mmm!", "Yum!", "Tasty!"]
    if eat_cycle < 6:
        bubble_x = body_x - 0.8
        bubble_y = head_y + 0.7
        bubble = patches.FancyBboxPatch(
            (bubble_x - 0.4, bubble_y - 0.15), 0.8, 0.35,
            boxstyle="round,pad=0.08",
            facecolor="white", edgecolor="black", linewidth=1.5
        )
        ax.add_patch(bubble)
        ax.text(bubble_x, bubble_y, messages[bubble_cycle],
                fontsize=10, ha="center", va="center",
                fontweight="bold", color="#8B0000")

    # Floor shadow
    shadow_width = 0.8 + 0.1 * np.sin(t)
    shadow = patches.Ellipse((body_x, -1.85), shadow_width, 0.1,
                              facecolor="black", alpha=0.2)
    ax.add_patch(shadow)

    ax.axis("off")


def main():
    total_frames = 120
    fig, ax = plt.subplots(figsize=(6, 7))
    fig.patch.set_facecolor("#87CEEB")

    def animate(frame):
        draw_stick_figure(ax, frame, total_frames)

    anim = FuncAnimation(fig, animate, frames=total_frames, interval=80)

    output_path = "uncle_brians_sandwich.gif"
    print(f"Rendering animation to {output_path}...")
    anim.save(output_path, writer=PillowWriter(fps=12))
    print(f"Done! Saved to {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
