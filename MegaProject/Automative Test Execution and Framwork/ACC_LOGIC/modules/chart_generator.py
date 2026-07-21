
import matplotlib
matplotlib.use("Agg")  # headless rendering, no display required
import matplotlib.pyplot as plt


POSITIVE_COLOR = "#2e7d32"   # green
NEGATIVE_COLOR = "#c62828"   # red
MISSING_COLOR = "#f9a825"    # yellow
INVALID_COLOR = "#a78bfa"    # purple


class ChartGenerator:

    @staticmethod
    def generate(pass_count, fail_count, missing_count, invalid_count, output_file,
                 title="Test Execution Result Distribution"):
        """
        Creates and saves a 3-slice pie chart (Positive / Negative /
        Missing-Invalid) to output_file. Slices with a zero count are
        left out entirely rather than drawn as empty wedges.
        """
        labels_all = ["Passed", "Failed", "Missing", "Invalid"]
        sizes_all = [pass_count, fail_count, missing_count, invalid_count]
        colors_all = [POSITIVE_COLOR, NEGATIVE_COLOR, MISSING_COLOR, INVALID_COLOR]

        labels = [l for l, s in zip(labels_all, sizes_all) if s > 0]
        sizes = [s for s in sizes_all if s > 0]
        colors = [c for c, s in zip(colors_all, sizes_all) if s > 0]

        if not sizes:
            print("[ChartGenerator] No data to chart - skipping.")
            return

        # Small per-slice labels: category name + count, placed just
        # outside the wedge, plus the percentage inside it.
        def slice_label(pct, all_vals):
            count = int(round(pct / 100.0 * sum(all_vals)))
            return f"{count}"

        fig, ax = plt.subplots(figsize=(5.2, 5.2))
        wedges, _texts, autotexts = ax.pie(
            sizes,
            colors=colors,
            autopct=lambda pct: slice_label(pct, sizes),
            pctdistance=0.72,
            startangle=90,
            explode=[0.03] * len(sizes),
            wedgeprops={"edgecolor": "white", "linewidth": 1.5},
            textprops={"fontsize": 10, "fontweight": "bold", "color": "white"},
        )

        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")
            autotext.set_color("white")

        # Small outside labels naming each slice (category + %)
        total = sum(sizes)
        for wedge, label, size in zip(wedges, labels, sizes):
            angle = (wedge.theta2 + wedge.theta1) / 2
            import math
            x = 1.18 * math.cos(math.radians(angle))
            y = 1.18 * math.sin(math.radians(angle))
            pct = size / total * 100
            ax.annotate(
                f"{label}\n{size} ({pct:.1f}%)",
                xy=(x, y),
                ha="center",
                va="center",
                fontsize=8.2,
                color="#333333",
            )

        ax.set_title(title, fontsize=12, fontweight="bold", pad=18)
        ax.axis("equal")
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches="tight", transparent=False, facecolor="white")
        plt.close(fig)

        print(f"[ChartGenerator] Pie chart saved to '{output_file}'")
