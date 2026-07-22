from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class VelocityGraphManager:
    def __init__(self, parent):
        self.time_history, self.velocity_history = [0.0], [0.0]
        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor="#0D1B2A")
        self.axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=14, pady=(0, 10))
        self.draw()

    def reset(self):
        self.time_history, self.velocity_history = [0.0], [0.0]
        self.draw()

    def add_sample(self, elapsed_time, speed):
        self.time_history.append(elapsed_time)
        self.velocity_history.append(speed)

    def add_final_zero(self, elapsed_time):
        if self.velocity_history[-1] != 0:
            self.add_sample(elapsed_time, 0.0)
        self.draw()

    def draw(self):
        self.axis.clear()
        self.axis.set_facecolor("#0B1622")
        self.axis.plot(self.time_history, self.velocity_history, color="#22C55E", linewidth=2.2)
        self.axis.fill_between(self.time_history, self.velocity_history, color="#22C55E", alpha=0.08)
        self.axis.set_title("Vehicle Velocity vs Time", color="#E2E8F0", fontweight="bold")
        self.axis.set_xlabel("Time (s)", color="#94A3B8")
        self.axis.set_ylabel("Velocity (km/h)", color="#94A3B8")
        self.axis.grid(True, color="#334155", alpha=0.45)
        self.axis.tick_params(colors="#94A3B8")
        for spine in self.axis.spines.values():
            spine.set_color("#334155")
        self.axis.set_xlim(left=0)
        self.axis.set_ylim(bottom=0, top=max(20, max(self.velocity_history) * 1.15))
        self.figure.tight_layout()
        self.canvas.draw_idle()
