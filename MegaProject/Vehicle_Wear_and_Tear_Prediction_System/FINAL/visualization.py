import os
import matplotlib.pyplot as plt

def generate_pie_chart(results):

    os.makedirs("charts", exist_ok=True)

    green_sensors = []
    yellow_sensors = []
    red_sensors = []

    for sensor, detail in results.items():

        if detail["status"] == "GREEN":
            green_sensors.append(sensor)

        elif detail["status"] == "YELLOW":
            yellow_sensors.append(sensor)

        else:
            red_sensors.append(sensor)

    sizes_all = [
        len(green_sensors),
        len(yellow_sensors),
        len(red_sensors)
    ]
    colors_all = ["green", "gold", "red"]
    legend_labels_all = [
        "HEALTHY\n" + "\n".join(green_sensors),
        "WARNING\n" + "\n".join(yellow_sensors),
        "CRITICAL\n" + "\n".join(red_sensors),
    ]

    sizes = []
    pie_colors = []
    legend_labels = []
    for size, color, label in zip(sizes_all, colors_all, legend_labels_all):
        if size > 0:
            sizes.append(size)
            pie_colors.append(color)
            legend_labels.append(label)

    plt.figure(figsize=(9, 6))

    plt.pie(
        sizes,
        colors=pie_colors,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Vehicle Health Distribution")

    plt.legend(
        legend_labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout()

    plt.savefig(
        "charts/pie_chart.png",
        bbox_inches="tight"
    )

    plt.close()