import matplotlib.pyplot as plot


STATUS_COLORS = {
    "GREEN": "#2ECC71",
    "YELLOW": "#F1C40F",
    "RED": "#E74C3C",
}


def prepare_status_summary(sensor_statuses):

    status_counts = {
        "GREEN": 0,
        "YELLOW": 0,
        "RED": 0
    }

    status_sensors = {
        "GREEN": [],
        "YELLOW": [],
        "RED": []
    }

    for sensor, status in sensor_statuses.items():

        if status in status_counts:

            status_counts[status] += 1

            status_sensors[status].append(sensor)

    return status_counts, status_sensors



def generate_pie_chart(
        status_counts,
        status_sensors):

    labels = [
        "HEALTHY",
        "WARNING",
        "CRITICAL"
    ]

    values = [
        status_counts["GREEN"],
        status_counts["YELLOW"],
        status_counts["RED"]
    ]

    colors = [
        STATUS_COLORS["GREEN"],
        STATUS_COLORS["YELLOW"],
        STATUS_COLORS["RED"]
    ]

    plot.figure(figsize=(12, 7))

    plot.pie(
        values,
        labels=[
            "HEALTHY",
            "WARNING",
            "CRITICAL"
        ],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90
    )

    legend_text = [

        "HEALTHY\n" +
        "\n".join(status_sensors["GREEN"]),

        "WARNING\n" +
        "\n".join(status_sensors["YELLOW"]),

        "CRITICAL\n" +
        "\n".join(status_sensors["RED"])

    ]

    plot.legend(
        legend_text,
        loc="center left",
        bbox_to_anchor=(1.25, 0.5)
    )

    plot.title(
        "Vehicle Health Distribution"
    )

    plot.savefig(
        "graphs/pie_chart.png",
        bbox_inches="tight"
    )

    plot.close()

    print("Pie Chart Generated Successfully!")







# Dont need the bar graph
'''
def generate_bar_graph(status_counts):

    labels = list(status_counts.keys())

    values = list(status_counts.values())

    colors = [STATUS_COLORS[label] for label in labels]

    plot.figure(figsize=(8, 6))

    # sea.barplot(x=labels, y=values, palette=colors)
    # This gives worning for the further version of the seaborn

    sea.barplot(x=labels, y=values, hue=labels, palette=colors, legend=False)
    
    plot.title("Vehicle Status Count")

    plot.xlabel("Status")

    plot.ylabel("Number of Vehicles")

    plot.savefig("graphs/bar_graph.png")

    plot.close()

    print("Bar Graph Generated Successfully!")

'''




# this below code without perfect code 
'''
import matplotlib.pyplot as plot
import seaborn as sea


def generate_pie_chart(status_counts):

    labels = status_counts.keys()

    values = status_counts.values()

    plot.figure(figsize=(8, 6))

    plot.pie(values,labels=labels,autopct="%1.1f%%")

    plot.title("Vehicle Health Distribution")

    plot.savefig("graphs/pie_chart.png")

    plot.close()

    print("Pie Chart Generated Successfully!")


def generate_bar_graph(status_counts):

    labels = list(status_counts.keys())

    values = list(status_counts.values())

    plot.figure(figsize=(8, 6))

    sea.barplot(x=labels,y=values)

    plot.title("Vehicle Status Count")

    plot.xlabel("Status")

    plot.ylabel("Number of Vehicles")

    plot.savefig("graphs/bar_graph.png")

    plot.close()

    print("Bar Graph Generated Successfully!")


'''
