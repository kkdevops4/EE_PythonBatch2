import tkinter as tk
from tkinter import messagebox


class GearStateMachine:

    def __init__(self, root):

        self.root = root
        self.root.title("Transmission Control Unit")
        self.root.geometry("500x500")

        self.current_gear = "P"

        # Title
        title = tk.Label(
            root,
            text="Transmission Control Unit",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # Current Gear Display
        self.gear_label = tk.Label(
            root,
            text=f"Current Gear : {self.current_gear}",
            font=("Arial", 16)
        )
        self.gear_label.pack(pady=10)

        # Speed Input
        speed_frame = tk.Frame(root)
        speed_frame.pack()

        tk.Label(
            speed_frame,
            text="Vehicle Speed (km/h):"
        ).pack(side=tk.LEFT)

        self.speed_entry = tk.Entry(speed_frame, width=10)
        self.speed_entry.insert(0, "0")
        self.speed_entry.pack(side=tk.LEFT)

        # Circular Gear Layout
        gear_frame = tk.Frame(root)
        gear_frame.pack(pady=30)

        self.n_btn = tk.Button(
            gear_frame,
            text="N",
            width=8,
            height=2,
            command=lambda: self.shift_gear("N")
        )
        self.n_btn.grid(row=0, column=1)

        self.p_btn = tk.Button(
            gear_frame,
            text="P",
            width=8,
            height=2,
            command=lambda: self.shift_gear("P")
        )
        self.p_btn.grid(row=1, column=0)

        self.center_label = tk.Label(
            gear_frame,
            text="⚙",
            font=("Arial", 24)
        )
        self.center_label.grid(row=1, column=1)

        self.d_btn = tk.Button(
            gear_frame,
            text="D",
            width=8,
            height=2,
            command=lambda: self.shift_gear("D")
        )
        self.d_btn.grid(row=1, column=2)

        self.r_btn = tk.Button(
            gear_frame,
            text="R",
            width=8,
            height=2,
            command=lambda: self.shift_gear("R")
        )
        self.r_btn.grid(row=2, column=1)

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Ready",
            fg="blue",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=20)

        # Allowed transitions
        self.allowed = {
            "P": ["R"],
            "R": ["P", "N"],
            "N": ["R", "D"],
            "D": ["N"]
        }

    def shift_gear(self, next_gear):

        try:
            speed = int(self.speed_entry.get())
        except ValueError:
            self.status_label.config(
                text="Enter valid speed",
                fg="red"
            )
            return

        # Rule 1
        if next_gear == "P" and speed > 5:
            self.status_label.config(
                text="Cannot shift to P when speed > 5 km/h",
                fg="red"
            )
            return

        # Rule 2
        if next_gear not in self.allowed[self.current_gear]:
            self.status_label.config(
                text=f"Invalid Shift: {self.current_gear} → {next_gear}",
                fg="red"
            )
            return

        # Valid shift
        self.current_gear = next_gear

        self.gear_label.config(
            text=f"Current Gear : {self.current_gear}"
        )

        self.status_label.config(
            text=f"Shifted to {self.current_gear}",
            fg="green"
        )


root = tk.Tk()
app = GearStateMachine(root)
root.mainloop()