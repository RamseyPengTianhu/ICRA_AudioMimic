"""Generate the paper's codec factorization evidence figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

navy = "#174EA6"
coral = "#E85D3F"
green = "#16834A"
gray = "#5F6368"

fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.35), gridspec_kw={"width_ratios": [1.08, 1]})

# Panel (a): paired intervention evidence for the accepted codec.
ax = axes[0]
seed_means = np.array([1.417, 1.412])
lower = np.array([1.390, 1.384])
upper = np.array([1.446, 1.441])
yerr = np.vstack([seed_means - lower, upper - seed_means])
x = np.arange(2)
ax.axhline(1.0, color=gray, lw=1.1, ls="--", zorder=1)
ax.errorbar(
    x,
    seed_means,
    yerr=yerr,
    fmt="o",
    markersize=7,
    capsize=5,
    color=navy,
    ecolor=navy,
    lw=2,
    zorder=3,
)
for xi, mean in zip(x, seed_means):
    ax.text(xi, mean + 0.045, f"{mean:.3f}", ha="center", va="bottom", color=navy, weight="bold")
ax.text(1.48, 1.012, "equal influence", ha="right", va="bottom", color=gray, fontsize=8)
ax.set_xticks(x, ["Training seed 1", "Training seed 2"])
ax.set_ylim(0.94, 1.52)
ax.set_ylabel("Structure-effect ratio")
ax.set_title("(a) Structural control", loc="left", weight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#DADCE0", lw=0.6, alpha=0.7)

# Panel (b): complementary residual evidence for the same accepted codec.
ax = axes[1]
labels = ["Detail\ngain", "Within-token\nvariation", "Effective\nrank"]
values = np.array([45.44, 76.57, 15.15 / 16.0 * 100.0])
bars = ax.bar(np.arange(3), values, width=0.62, color=[coral, coral, green], edgecolor="white")
for bar, value, display in zip(bars, values, ["45.4%", "76.6%", "15.15 / 16"]):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 3, display, ha="center", va="bottom", weight="bold")
ax.set_xticks(np.arange(3), labels)
ax.set_ylim(0, 110)
ax.set_ylabel("Measured value (%)")
ax.set_title("(b) Complementary residual", loc="left", weight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#DADCE0", lw=0.6, alpha=0.7)

fig.tight_layout(pad=0.6, w_pad=1.3)
fig.savefig(OUT / "codec-factorization-evidence.pdf", bbox_inches="tight", pad_inches=0.12)
fig.savefig(OUT / "codec-factorization-evidence.png", dpi=300, bbox_inches="tight", pad_inches=0.12)
