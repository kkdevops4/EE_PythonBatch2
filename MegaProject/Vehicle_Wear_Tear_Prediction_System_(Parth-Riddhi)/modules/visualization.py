

import matplotlib.pyplot as plot
import seaborn as sea


# Map each status to its real-world alert colour, instead of relying on
# with the GREEN/YELLOW/RED labels).
STATUS_COLORS = {
    "GREEN": "#2ECC71",
    "YELLOW": "#F1C40F",
    "RED": "#E74C3C",
}


def generate_pie_chart(status_counts):

    labels = list(status_counts.keys())

    values = list(status_counts.values())

    colors = [STATUS_COLORS[label] for label in labels]

    plot.figure(figsize=(8, 6))

    plot.pie(values, labels=labels, autopct="%1.1f%%", colors=colors)

    plot.title("Vehicle Health Distribution")

    plot.savefig("graphs/pie_chart.png")

    plot.close()

    print("Pie Chart Generated Successfully!")


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
